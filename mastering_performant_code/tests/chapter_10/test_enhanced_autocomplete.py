"""
Enhanced Tests for Production Autocomplete System

This module provides comprehensive tests for the enhanced autocomplete system,
including fuzzy matching, learning capabilities, and property-based testing.
"""

import unittest
import time
from typing import List, Set
from unittest.mock import patch

from chapter_10.autocomplete import ProductionAutocomplete, FuzzyMatcher, Suggestion

class TestFuzzyMatcher(unittest.TestCase):
    """Test cases for the FuzzyMatcher class."""
    
    def test_levenshtein_distance(self):
        """Test Levenshtein distance calculation."""
        # Test basic cases
        self.assertEqual(FuzzyMatcher.levenshtein_distance("", ""), 0)
        self.assertEqual(FuzzyMatcher.levenshtein_distance("", "abc"), 3)
        self.assertEqual(FuzzyMatcher.levenshtein_distance("abc", ""), 3)
        
        # Test identical strings
        self.assertEqual(FuzzyMatcher.levenshtein_distance("hello", "hello"), 0)
        
        # Test single character differences
        self.assertEqual(FuzzyMatcher.levenshtein_distance("hello", "helo"), 1)  # deletion
        self.assertEqual(FuzzyMatcher.levenshtein_distance("hello", "helloo"), 1)  # insertion
        self.assertEqual(FuzzyMatcher.levenshtein_distance("hello", "helpo"), 1)  # substitution
        
        # Test multiple differences
        self.assertEqual(FuzzyMatcher.levenshtein_distance("hello", "world"), 4)
        self.assertEqual(FuzzyMatcher.levenshtein_distance("kitten", "sitting"), 3)
        
        # Test case insensitivity (should be case sensitive by default)
        self.assertEqual(FuzzyMatcher.levenshtein_distance("Hello", "hello"), 1)
    
    def test_get_fuzzy_matches(self):
        """Test fuzzy matching functionality."""
        words = ["hello", "world", "python", "programming", "data", "structure"]
        
        # Test exact matches
        matches = FuzzyMatcher.get_fuzzy_matches("hello", words, max_distance=0)
        self.assertEqual(matches, [("hello", 0)])
        
        # Test close matches
        matches = FuzzyMatcher.get_fuzzy_matches("helo", words, max_distance=1)
        self.assertEqual(matches, [("hello", 1)])
        
        # Test no matches
        matches = FuzzyMatcher.get_fuzzy_matches("xyz", words, max_distance=1)
        self.assertEqual(matches, [])
        
        # Test multiple matches
        matches = FuzzyMatcher.get_fuzzy_matches("prog", words, max_distance=2)
        self.assertIn(("programming", 0), matches)  # prefix match
        
        # Test sorting by distance
        matches = FuzzyMatcher.get_fuzzy_matches("pythn", words, max_distance=2)
        self.assertEqual(matches[0][0], "python")  # distance 1 should come first

class TestProductionAutocomplete(unittest.TestCase):
    """Test cases for the ProductionAutocomplete class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.autocomplete = ProductionAutocomplete(enable_fuzzy=True, enable_learning=True)
        
        # Add test data
        test_words = [
            ("python", 100, "programming"),
            ("programming", 80, "programming"),
            ("data", 90, "computer_science"),
            ("structure", 70, "computer_science"),
            ("algorithm", 85, "computer_science"),
            ("computer", 75, "hardware"),
            ("science", 95, "academic"),
            ("software", 88, "programming"),
            ("development", 92, "programming"),
            ("database", 78, "computer_science"),
            ("network", 82, "computer_science"),
            ("system", 87, "computer_science")
        ]
        
        for word, freq, category in test_words:
            self.autocomplete.add_word(word, freq, category)
    
    def test_initialization(self):
        """Test autocomplete system initialization."""
        autocomplete = ProductionAutocomplete()
        self.assertEqual(len(autocomplete), 0)
        self.assertTrue(autocomplete._enable_fuzzy)
        self.assertTrue(autocomplete._enable_learning)
        
        # Test with features disabled
        autocomplete = ProductionAutocomplete(enable_fuzzy=False, enable_learning=False)
        self.assertFalse(autocomplete._enable_fuzzy)
        self.assertFalse(autocomplete._enable_learning)
    
    def test_add_word_with_metadata(self):
        """Test adding words with categories and metadata."""
        autocomplete = ProductionAutocomplete()
        
        # Add word with category
        autocomplete.add_word("test", 10, category="testing")
        self.assertIn("testing", autocomplete._word_categories["test"])
        
        # Add word with metadata
        metadata = {"source": "user_input", "confidence": 0.9}
        autocomplete.add_word("example", 5, metadata=metadata)
        self.assertEqual(autocomplete._word_metadata["example"]["source"], "user_input")
        
        # Add word with both
        autocomplete.add_word("sample", 15, category="testing", metadata={"priority": "high"})
        self.assertIn("testing", autocomplete._word_categories["sample"])
        self.assertEqual(autocomplete._word_metadata["sample"]["priority"], "high")
    
    def test_fuzzy_suggestions(self):
        """Test fuzzy suggestion functionality."""
        # Test exact prefix matches
        suggestions = self.autocomplete.get_fuzzy_suggestions("prog", max_distance=2)
        self.assertGreater(len(suggestions), 0)
        
        # Test fuzzy matches for typos
        suggestions = self.autocomplete.get_fuzzy_suggestions("pythn", max_distance=2)
        self.assertGreater(len(suggestions), 0)
        self.assertEqual(suggestions[0].word, "python")
        self.assertEqual(suggestions[0].edit_distance, 1)
        
        # Test no matches
        suggestions = self.autocomplete.get_fuzzy_suggestions("xyzabc", max_distance=1)
        self.assertEqual(len(suggestions), 0)
        
        # Test confidence scoring
        suggestions = self.autocomplete.get_fuzzy_suggestions("prog", max_distance=2)
        for suggestion in suggestions:
            self.assertGreaterEqual(suggestion.confidence, 0.0)
            self.assertLessEqual(suggestion.confidence, 1.0)
    
    def test_learning_functionality(self):
        """Test learning from user selections."""
        # Get initial suggestions
        initial_suggestions = self.autocomplete.get_suggestions("prog", 5)
        initial_frequencies = [s.frequency for s in initial_suggestions]
        
        # Simulate user selection
        self.autocomplete.update_learning("programming", increment=5)
        
        # Get suggestions again
        updated_suggestions = self.autocomplete.get_suggestions("prog", 5)
        updated_frequencies = [s.frequency for s in updated_suggestions]
        
        # Programming should have higher frequency now
        programming_initial = next((s.frequency for s in initial_suggestions if s.word == "programming"), 0)
        programming_updated = next((s.frequency for s in updated_suggestions if s.word == "programming"), 0)
        self.assertGreater(programming_updated, programming_initial)
    
    def test_category_filtering(self):
        """Test category-based filtering."""
        # Get all suggestions
        all_suggestions = self.autocomplete.get_suggestions("prog", 10)
        
        # Get programming category suggestions
        programming_suggestions = self.autocomplete.get_suggestions_by_category("prog", "programming", 10)
        
        # All programming suggestions should have the programming category
        for suggestion in programming_suggestions:
            self.assertEqual(suggestion.category, "programming")
        
        # Programming suggestions should be a subset of all suggestions
        programming_words = {s.word for s in programming_suggestions}
        all_words = {s.word for s in all_suggestions}
        self.assertTrue(programming_words.issubset(all_words))
    
    def test_category_management(self):
        """Test category management functions."""
        autocomplete = ProductionAutocomplete()
        autocomplete.add_word("test", 10, category="category1")
        
        # Test adding category
        autocomplete.add_category("test", "category2")
        self.assertIn("category1", autocomplete._word_categories["test"])
        self.assertIn("category2", autocomplete._word_categories["test"])
        
        # Test removing category
        autocomplete.remove_category("test", "category1")
        self.assertNotIn("category1", autocomplete._word_categories["test"])
        self.assertIn("category2", autocomplete._word_categories["test"])
        
        # Test getting categories
        categories = autocomplete.get_categories()
        self.assertIn("category2", categories)
        
        # Test getting words by category
        words = autocomplete.get_words_by_category("category2")
        self.assertIn("test", words)
    
    def test_cache_functionality(self):
        """Test fuzzy matching cache."""
        # First call should populate cache
        suggestions1 = self.autocomplete.get_fuzzy_suggestions("prog", max_distance=2)
        initial_cache_size = len(self.autocomplete._fuzzy_cache)
        
        # Second call should use cache
        suggestions2 = self.autocomplete.get_fuzzy_suggestions("prog", max_distance=2)
        self.assertEqual(len(self.autocomplete._fuzzy_cache), initial_cache_size)
        
        # Results should be identical
        self.assertEqual([s.word for s in suggestions1], [s.word for s in suggestions2])
        
        # Test cache clearing
        self.autocomplete.clear_cache()
        self.assertEqual(len(self.autocomplete._fuzzy_cache), 0)
    
    def test_decay_functionality(self):
        """Test decay of old selections."""
        # Add some user selections
        self.autocomplete.update_learning("python", increment=10)
        self.autocomplete.update_learning("programming", increment=5)
        
        # Get initial frequencies
        initial_python_freq = self.autocomplete._get_adjusted_frequency("python")
        initial_prog_freq = self.autocomplete._get_adjusted_frequency("programming")
        
        # Apply decay
        self.autocomplete.decay_old_selections()
        
        # Get updated frequencies
        updated_python_freq = self.autocomplete._get_adjusted_frequency("python")
        updated_prog_freq = self.autocomplete._get_adjusted_frequency("programming")
        
        # Frequencies should be reduced
        self.assertLess(updated_python_freq, initial_python_freq)
        self.assertLess(updated_prog_freq, initial_prog_freq)
    
    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        # Test exact match confidence
        suggestions = self.autocomplete.get_fuzzy_suggestions("python", max_distance=2)
        exact_match = next((s for s in suggestions if s.word == "python"), None)
        self.assertIsNotNone(exact_match)
        self.assertEqual(exact_match.confidence, 1.0)
        
        # Test fuzzy match confidence
        suggestions = self.autocomplete.get_fuzzy_suggestions("pythn", max_distance=2)
        fuzzy_match = next((s for s in suggestions if s.word == "python"), None)
        self.assertIsNotNone(fuzzy_match)
        self.assertLess(fuzzy_match.confidence, 1.0)
        self.assertGreater(fuzzy_match.confidence, 0.0)
    
    def test_statistics(self):
        """Test comprehensive statistics."""
        stats = self.autocomplete.get_statistics()
        
        # Check basic statistics
        self.assertIn('total_words', stats)
        self.assertIn('total_frequency', stats)
        self.assertIn('learning_enabled', stats)
        self.assertIn('fuzzy_enabled', stats)
        self.assertIn('categories', stats)
        self.assertIn('cache_size', stats)
        
        # Check learning statistics
        self.assertIn('total_user_selections', stats)
        self.assertIn('most_selected_words', stats)
        
        # Verify values
        self.assertTrue(stats['learning_enabled'])
        self.assertTrue(stats['fuzzy_enabled'])
        self.assertGreater(stats['total_words'], 0)
    
    def test_edge_cases(self):
        """Test edge cases and error handling."""
        autocomplete = ProductionAutocomplete()
        
        # Test empty prefix
        suggestions = autocomplete.get_suggestions("", 5)
        self.assertEqual(len(suggestions), 0)
        
        # Test very long prefix
        long_prefix = "a" * 1000
        suggestions = autocomplete.get_fuzzy_suggestions(long_prefix, max_distance=2)
        self.assertEqual(len(suggestions), 0)
        
        # Test special characters
        autocomplete.add_word("test-word", 10, category="special")
        suggestions = autocomplete.get_fuzzy_suggestions("test", max_distance=2)
        self.assertGreater(len(suggestions), 0)
    
    def test_performance(self):
        """Test performance characteristics."""
        autocomplete = ProductionAutocomplete()
        
        # Add many words
        for i in range(1000):
            autocomplete.add_word(f"word{i}", i % 100)
        
        # Test suggestion performance
        start_time = time.time()
        suggestions = autocomplete.get_fuzzy_suggestions("word", max_distance=2, max_results=50)
        end_time = time.time()
        
        # Should complete within reasonable time
        self.assertLess(end_time - start_time, 1.0)  # Less than 1 second
        self.assertGreater(len(suggestions), 0)

class TestPropertyBasedTesting(unittest.TestCase):
    """Property-based tests for autocomplete system."""
    
    def test_fuzzy_matching_properties(self):
        """Test properties that should always hold for fuzzy matching."""
        autocomplete = ProductionAutocomplete()
        
        # Add test words
        test_words = ["hello", "world", "python", "programming", "data", "structure"]
        for word in test_words:
            autocomplete.add_word(word, 10)
        
        # Property 1: Exact matches should have edit distance 0
        for word in test_words:
            suggestions = autocomplete.get_fuzzy_suggestions(word, max_distance=2)
            exact_matches = [s for s in suggestions if s.word == word]
            if exact_matches:
                self.assertEqual(exact_matches[0].edit_distance, 0)
        
        # Property 2: Edit distance should be symmetric
        for word1 in test_words:
            for word2 in test_words:
                dist1 = FuzzyMatcher.levenshtein_distance(word1, word2)
                dist2 = FuzzyMatcher.levenshtein_distance(word2, word1)
                self.assertEqual(dist1, dist2)
        
        # Property 3: Triangle inequality
        for word1 in test_words:
            for word2 in test_words:
                for word3 in test_words:
                    dist12 = FuzzyMatcher.levenshtein_distance(word1, word2)
                    dist23 = FuzzyMatcher.levenshtein_distance(word2, word3)
                    dist13 = FuzzyMatcher.levenshtein_distance(word1, word3)
                    self.assertLessEqual(dist13, dist12 + dist23)
    
    def test_learning_properties(self):
        """Test properties that should always hold for learning."""
        autocomplete = ProductionAutocomplete()
        autocomplete.add_word("test", 10)
        
        # Property 1: Learning should increase frequency
        initial_freq = autocomplete._get_adjusted_frequency("test")
        autocomplete.update_learning("test", increment=5)
        updated_freq = autocomplete._get_adjusted_frequency("test")
        self.assertGreater(updated_freq, initial_freq)
        
        # Property 2: Decay should decrease frequency
        autocomplete.decay_old_selections()
        decayed_freq = autocomplete._get_adjusted_frequency("test")
        self.assertLess(decayed_freq, updated_freq)
        
        # Property 3: Multiple decays should eventually reduce to base frequency
        for _ in range(100):
            autocomplete.decay_old_selections()
        final_freq = autocomplete._get_adjusted_frequency("test")
        self.assertGreaterEqual(final_freq, 10)  # Should not go below base frequency
    
    def test_category_properties(self):
        """Test properties that should always hold for categories."""
        autocomplete = ProductionAutocomplete()
        
        # Property 1: Adding a word to a category should make it appear in category queries
        autocomplete.add_word("test", 10, category="category1")
        category_words = autocomplete.get_words_by_category("category1")
        self.assertIn("test", category_words)
        
        # Property 2: Removing a category should remove the word from category queries
        autocomplete.remove_category("test", "category1")
        category_words = autocomplete.get_words_by_category("category1")
        self.assertNotIn("test", category_words)
        
        # Property 3: A word can belong to multiple categories
        autocomplete.add_category("test", "category1")
        autocomplete.add_category("test", "category2")
        self.assertIn("category1", autocomplete._word_categories["test"])
        self.assertIn("category2", autocomplete._word_categories["test"])

if __name__ == '__main__':
    unittest.main() 