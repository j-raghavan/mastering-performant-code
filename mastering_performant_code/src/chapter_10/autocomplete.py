"""
Enhanced Autocomplete System Implementation

This module provides a production-ready autocomplete system using tries
with frequency tracking, fuzzy matching, learning capabilities, and advanced ranking.
"""

import re
from typing import List, Dict, Tuple, Any, Optional, Set
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from chapter_10.trie import Trie

@dataclass
class Suggestion:
    """Container for autocomplete suggestions with metadata."""
    word: str
    frequency: int
    edit_distance: int = 0
    category: Optional[str] = None
    last_used: Optional[float] = None
    confidence: float = 1.0

class FuzzyMatcher:
    """Fuzzy matching implementation using edit distance."""
    
    @staticmethod
    def levenshtein_distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings."""
        if len(s1) < len(s2):
            return FuzzyMatcher.levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    @staticmethod
    def get_fuzzy_matches(query: str, words: List[str], max_distance: int = 2) -> List[Tuple[str, int]]:
        """Get fuzzy matches for a query."""
        matches = []
        query_lower = query.lower()
        
        for word in words:
            word_lower = word.lower()
            
            # Check for exact prefix match first (distance 0)
            if word_lower.startswith(query_lower):
                matches.append((word, 0))
            else:
                # Calculate edit distance for non-prefix matches
                distance = FuzzyMatcher.levenshtein_distance(query_lower, word_lower)
                if distance <= max_distance:
                    matches.append((word, distance))
        
        # Sort by distance, then alphabetically
        return sorted(matches, key=lambda x: (x[1], x[0]))

class ProductionAutocomplete:
    """
    Production-ready autocomplete system with advanced features.
    
    Features:
    - Fuzzy matching for typos and misspellings
    - Learning from user selections
    - Category-based filtering
    - Confidence scoring
    - Real-time adaptation
    """
    
    def __init__(self, enable_fuzzy: bool = True, enable_learning: bool = True):
        """
        Initialize the autocomplete system.
        
        Args:
            enable_fuzzy: Enable fuzzy matching capabilities
            enable_learning: Enable learning from user selections
        """
        self._trie = Trie[int]()  # Store frequency as value
        self._word_frequencies = defaultdict(int)
        self._word_categories = defaultdict(set)
        self._user_selections = Counter()
        self._word_metadata = defaultdict(dict)
        self._enable_fuzzy = enable_fuzzy
        self._enable_learning = enable_learning
        self._fuzzy_cache = {}
        
        # Learning parameters
        self._selection_weight = 2.0  # Weight for user selections
        self._decay_factor = 0.95  # Decay factor for old selections
        self._max_cache_size = 1000
    
    def add_word(self, word: str, frequency: int = 1, 
                category: Optional[str] = None, metadata: Optional[Dict] = None) -> None:
        """
        Add a word to the autocomplete system.
        
        Args:
            word: The word to add
            frequency: Frequency/weight of the word
            category: Optional category for the word
            metadata: Optional metadata dictionary
        """
        self._word_frequencies[word] += frequency
        if category:
            self._word_categories[word].add(category)
        if metadata:
            self._word_metadata[word].update(metadata)
        
        # Update trie with current frequency
        self._update_trie_frequency(word)
    
    def add_words(self, words: List[str], category: Optional[str] = None) -> None:
        """Add multiple words to the system."""
        for word in words:
            self.add_word(word, category=category)
    
    def get_fuzzy_suggestions(self, query: str, max_distance: int = 2, 
                            max_results: int = 10) -> List[Suggestion]:
        """
        Get fuzzy suggestions for a query with edit distance.
        
        Args:
            query: The query to autocomplete
            max_distance: Maximum edit distance for fuzzy matching
            max_results: Maximum number of suggestions
            
        Returns:
            List of Suggestion objects with edit distance information
        """
        if not self._enable_fuzzy:
            return self.get_suggestions(query, max_results)
        
        # Check cache first
        cache_key = (query, max_distance, max_results)
        if cache_key in self._fuzzy_cache:
            return self._fuzzy_cache[cache_key]
        
        # Get exact prefix matches first
        exact_matches = self._trie.get_all_with_prefix(query)
        exact_words = {word for word, _ in exact_matches}
        
        # Get all words for fuzzy matching
        all_words = list(self._word_frequencies.keys())
        
        # Get fuzzy matches
        fuzzy_matches = FuzzyMatcher.get_fuzzy_matches(query, all_words, max_distance)
        
        # Combine and rank suggestions
        suggestions = []
        seen_words = set()
        
        # Add exact matches first (edit distance 0)
        for word, freq in exact_matches:
            if word not in seen_words:
                suggestions.append(Suggestion(
                    word=word,
                    frequency=self._get_adjusted_frequency(word),
                    edit_distance=0,
                    category=self._get_primary_category(word),
                    confidence=1.0
                ))
                seen_words.add(word)
        
        # Add fuzzy matches
        for word, distance in fuzzy_matches:
            if word not in seen_words and len(suggestions) < max_results:
                suggestions.append(Suggestion(
                    word=word,
                    frequency=self._get_adjusted_frequency(word),
                    edit_distance=distance,
                    category=self._get_primary_category(word),
                    confidence=self._calculate_confidence(word, distance)
                ))
                seen_words.add(word)
        
        # Sort by confidence, then frequency, then alphabetically
        suggestions.sort(key=lambda x: (-x.confidence, -x.frequency, x.word))
        
        # Cache result
        if len(self._fuzzy_cache) < self._max_cache_size:
            self._fuzzy_cache[cache_key] = suggestions[:max_results]
        
        return suggestions[:max_results]
    
    def get_suggestions(self, prefix: str, max_results: int = 10, 
                       category: Optional[str] = None) -> List[Suggestion]:
        """
        Get autocomplete suggestions with category filtering.
        
        Args:
            prefix: The prefix to autocomplete
            max_results: Maximum number of suggestions
            category: Optional category filter
            
        Returns:
            List of Suggestion objects
        """
        suggestions = self._trie.get_all_with_prefix(prefix)
        
        # Convert to Suggestion objects
        suggestion_objects = []
        for word, freq in suggestions:
            if category is None or category in self._word_categories[word]:
                suggestion_objects.append(Suggestion(
                    word=word,
                    frequency=self._get_adjusted_frequency(word),
                    category=self._get_primary_category(word),
                    confidence=self._calculate_confidence(word, 0)
                ))
        
        # Sort by frequency (descending) and then alphabetically
        suggestion_objects.sort(key=lambda x: (-x.frequency, x.word))
        return suggestion_objects[:max_results]
    
    def get_top_suggestions(self, prefix: str, max_results: int = 10) -> List[str]:
        """Get top autocomplete suggestions as strings only."""
        return [s.word for s in self.get_suggestions(prefix, max_results)]
    
    def update_learning(self, selected_query: str, increment: int = 1) -> None:
        """
        Learn from user selections to improve future suggestions.
        
        Args:
            selected_query: The query that was selected by the user
            increment: How much to increment the selection count
        """
        if not self._enable_learning:
            return
        
        self._user_selections[selected_query] += increment
        self._update_trie_frequency(selected_query)
        
        # Clear cache to reflect new learning
        self._fuzzy_cache.clear()
    
    def _get_adjusted_frequency(self, word: str) -> int:
        """Get frequency adjusted for user selections."""
        base_freq = self._word_frequencies[word]
        selection_boost = self._user_selections[word] * self._selection_weight
        return int(base_freq + selection_boost)
    
    def _update_trie_frequency(self, word: str) -> None:
        """Update the trie with current adjusted frequency."""
        adjusted_freq = self._get_adjusted_frequency(word)
        self._trie.insert(word, adjusted_freq)
    
    def _get_primary_category(self, word: str) -> Optional[str]:
        """Get the primary category for a word."""
        categories = self._word_categories[word]
        return next(iter(categories)) if categories else None
    
    def _calculate_confidence(self, word: str, edit_distance: int) -> float:
        """Calculate confidence score for a suggestion."""
        base_confidence = 1.0 / (1 + edit_distance)  # Lower distance = higher confidence
        
        # Boost confidence based on user selections
        selection_boost = min(self._user_selections[word] * 0.1, 0.5)
        
        # Boost confidence based on frequency
        freq_boost = min(self._word_frequencies[word] / 1000, 0.3)
        
        return min(base_confidence + selection_boost + freq_boost, 1.0)
    
    def get_suggestions_by_category(self, prefix: str, category: str, 
                                  max_results: int = 10) -> List[Suggestion]:
        """Get suggestions filtered by category."""
        return self.get_suggestions(prefix, max_results, category)
    
    def add_category(self, word: str, category: str) -> None:
        """Add a category to a word."""
        self._word_categories[word].add(category)
    
    def remove_category(self, word: str, category: str) -> None:
        """Remove a category from a word."""
        self._word_categories[word].discard(category)
    
    def get_categories(self) -> Set[str]:
        """Get all available categories."""
        categories = set()
        for word_categories in self._word_categories.values():
            categories.update(word_categories)
        return categories
    
    def get_words_by_category(self, category: str) -> List[str]:
        """Get all words in a specific category."""
        return [word for word, categories in self._word_categories.items() 
                if category in categories]
    
    def update_frequency(self, word: str, increment: int = 1) -> None:
        """Update the frequency of a word."""
        if word in self._word_frequencies:
            self._word_frequencies[word] += increment
            self._update_trie_frequency(word)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the autocomplete system."""
        total_words = len(self._word_frequencies)
        total_frequency = sum(self._word_frequencies.values())
        avg_frequency = total_frequency / total_words if total_words > 0 else 0
        
        # Learning statistics
        total_selections = sum(self._user_selections.values())
        most_selected = self._user_selections.most_common(5) if self._user_selections else []
        
        # Category statistics
        category_counts = defaultdict(int)
        for categories in self._word_categories.values():
            for category in categories:
                category_counts[category] += 1
        
        return {
            'total_words': total_words,
            'total_frequency': total_frequency,
            'average_frequency': avg_frequency,
            'trie_size': len(self._trie),
            'most_frequent': max(self._word_frequencies.items(), key=lambda x: x[1]) if self._word_frequencies else None,
            'learning_enabled': self._enable_learning,
            'fuzzy_enabled': self._enable_fuzzy,
            'total_user_selections': total_selections,
            'most_selected_words': most_selected,
            'categories': dict(category_counts),
            'cache_size': len(self._fuzzy_cache)
        }
    
    def clear_cache(self) -> None:
        """Clear the fuzzy matching cache."""
        self._fuzzy_cache.clear()
    
    def decay_old_selections(self) -> None:
        """Apply decay to old user selections."""
        if not self._enable_learning:
            return
        
        for word in list(self._user_selections.keys()):
            self._user_selections[word] = int(self._user_selections[word] * self._decay_factor)
            if self._user_selections[word] == 0:
                del self._user_selections[word]
        
        # Update trie frequencies
        for word in self._word_frequencies:
            self._update_trie_frequency(word)
    
    def __len__(self) -> int:
        """Return the number of words in the system."""
        return len(self._word_frequencies)
    
    def __contains__(self, word: str) -> bool:
        """Check if a word is in the system."""
        return word in self._word_frequencies

# Backward compatibility
class AutocompleteSystem(ProductionAutocomplete):
    """
    Legacy autocomplete system for backward compatibility.
    
    This class maintains the original API while inheriting from
    the enhanced ProductionAutocomplete.
    """
    
    def __init__(self):
        """Initialize with basic features enabled."""
        super().__init__(enable_fuzzy=False, enable_learning=False)
    
    def get_suggestions(self, prefix: str, max_results: int = 10) -> List[Tuple[str, int]]:
        """Get suggestions in the original format."""
        suggestions = super().get_suggestions(prefix, max_results)
        return [(s.word, s.frequency) for s in suggestions]
    
    def get_top_suggestions(self, prefix: str, max_results: int = 10) -> List[str]:
        """Get top autocomplete suggestions as strings only."""
        suggestions = self.get_suggestions(prefix, max_results)
        return [word for word, _ in suggestions] 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running autocomplete demonstration...")
    print("=" * 50)

    # Create instance of Suggestion
    try:
        instance = Suggestion()
        print(f"✓ Created Suggestion instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating Suggestion instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
