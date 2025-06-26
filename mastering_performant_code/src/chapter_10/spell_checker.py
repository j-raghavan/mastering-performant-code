"""
Spell Checker Implementation

This module provides a spell checker using trie for dictionary lookup
with basic suggestion capabilities.
"""

from typing import List, Optional, Tuple
from src.chapter_10.trie import Trie

class SpellChecker:
    """
    A spell checker using trie for dictionary lookup.
    
    This spell checker demonstrates how to use tries for
    efficient dictionary-based spell checking.
    """
    
    def __init__(self, dictionary: Optional[List[str]] = None) -> None:
        """
        Initialize the spell checker.
        
        Args:
            dictionary: List of correctly spelled words
        """
        self._trie = Trie[bool]()
        if dictionary:
            self.add_dictionary(dictionary)
    
    def add_dictionary(self, words: List[str]) -> None:
        """Add words to the dictionary."""
        for word in words:
            if word:  # Skip empty strings
                self._trie.insert(word.lower(), True)
    
    def add_word(self, word: str) -> None:
        """Add a single word to the dictionary."""
        if word:
            self._trie.insert(word.lower(), True)
    
    def is_correct(self, word: str) -> bool:
        """Check if a word is spelled correctly."""
        if not word:
            return False
        return self._trie.search(word.lower()) is not None
    
    def get_suggestions(self, misspelled_word: str, max_suggestions: int = 5) -> List[str]:
        """
        Get spelling suggestions for a misspelled word.
        
        This is a simplified implementation. In practice, you'd use
        edit distance algorithms like Levenshtein distance.
        """
        suggestions = []
        word = misspelled_word.lower()
        
        if not word:
            return suggestions
        
        # Check for common prefixes
        for i in range(1, len(word) + 1):
            prefix = word[:i]
            if self._trie.starts_with(prefix):
                # Get words with this prefix
                prefix_words = self._trie.get_all_with_prefix(prefix)
                for suggestion, _ in prefix_words:
                    if suggestion not in suggestions:
                        suggestions.append(suggestion)
                        if len(suggestions) >= max_suggestions:
                            break
        
        return suggestions[:max_suggestions]
    
    def check_text(self, text: str) -> List[Tuple[str, int, List[str]]]:
        """
        Check spelling in a text.
        
        Returns:
            List of (word, position, suggestions) tuples
        """
        import re
        
        # Split text into words, preserving punctuation
        words = re.findall(r'\b\w+\b', text)
        errors = []
        
        for i, word in enumerate(words):
            # Remove punctuation for checking
            clean_word = ''.join(c for c in word if c.isalpha())
            if clean_word and not self.is_correct(clean_word):
                suggestions = self.get_suggestions(clean_word)
                errors.append((word, i, suggestions))
        
        return errors
    
    def remove_word(self, word: str) -> bool:
        """Remove a word from the dictionary."""
        if word:
            return self._trie.delete(word.lower())
        return False
    
    def get_dictionary_size(self) -> int:
        """Get the number of words in the dictionary."""
        return len(self._trie)
    
    def get_all_words(self) -> List[str]:
        """Get all words in the dictionary."""
        return [word for word, _ in self._trie.get_all_strings()]
    
    def __contains__(self, word: str) -> bool:
        """Check if a word is in the dictionary."""
        return self.is_correct(word) 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running spell_checker demonstration...")
    print("=" * 50)

    # Create instance of SpellChecker
    try:
        instance = SpellChecker()
        print(f"✓ Created SpellChecker instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating SpellChecker instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
