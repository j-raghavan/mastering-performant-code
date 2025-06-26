"""
Unit tests for AutocompleteSystem implementation.

This module provides comprehensive test coverage for the AutocompleteSystem class,
including frequency tracking, ranking, and suggestion generation.
"""

import unittest
from typing import List

from chapter_10.autocomplete import AutocompleteSystem

class TestAutocompleteSystem(unittest.TestCase):
    """Test cases for AutocompleteSystem implementation."""
    
    def setUp(self):
        self.autocomplete = AutocompleteSystem()
    
    def test_initialization(self):
        """Test system initialization."""
        self.assertEqual(len(self.autocomplete), 0)
        self.assertEqual(len(self.autocomplete._word_frequencies), 0)
    
    def test_add_word(self):
        """Test adding a single word."""
        self.autocomplete.add_word("hello", 5)
        
        self.assertEqual(len(self.autocomplete), 1)
        self.assertEqual(self.autocomplete._word_frequencies["hello"], 5)
        self.assertEqual(self.autocomplete._trie.search("hello"), 5)
    
    def test_add_word_default_frequency(self):
        """Test adding a word with default frequency."""
        self.autocomplete.add_word("hello")
        
        self.assertEqual(len(self.autocomplete), 1)
        self.assertEqual(self.autocomplete._word_frequencies["hello"], 1)
        self.assertEqual(self.autocomplete._trie.search("hello"), 1)
    
    def test_add_word_multiple_times(self):
        """Test adding the same word multiple times."""
        self.autocomplete.add_word("hello", 5)
        self.autocomplete.add_word("hello", 3)
        
        self.assertEqual(len(self.autocomplete), 1)
        self.assertEqual(self.autocomplete._word_frequencies["hello"], 8)
        self.assertEqual(self.autocomplete._trie.search("hello"), 8)
    
    def test_add_words(self):
        """Test adding multiple words at once."""
        words = ["hello", "world", "python", "programming"]
        self.autocomplete.add_words(words)
        
        self.assertEqual(len(self.autocomplete), 4)
        for word in words:
            self.assertEqual(self.autocomplete._word_frequencies[word], 1)
            self.assertEqual(self.autocomplete._trie.search(word), 1)
    
    def test_get_suggestions(self):
        """Test getting suggestions for a prefix."""
        words_with_freq = [
            ("python", 100), ("programming", 80), ("data", 90),
            ("structure", 70), ("algorithm", 85), ("computer", 75)
        ]
        
        for word, freq in words_with_freq:
            self.autocomplete.add_word(word, freq)
        
        # Test suggestions for "pro"
        suggestions = self.autocomplete.get_suggestions("pro", max_results=3)
        self.assertEqual(len(suggestions), 1)  # Only "programming" matches
        
        # Check that suggestions are sorted by frequency (descending)
        self.assertEqual(suggestions[0][0], "programming")
        self.assertEqual(suggestions[0][1], 80)
    
    def test_get_suggestions_empty_prefix(self):
        """Test getting suggestions for empty prefix."""
        words = ["hello", "world", "python"]
        for word in words:
            self.autocomplete.add_word(word)
        
        suggestions = self.autocomplete.get_suggestions("", max_results=2)
        self.assertEqual(len(suggestions), 2)
    
    def test_get_suggestions_no_matches(self):
        """Test getting suggestions when no matches exist."""
        self.autocomplete.add_word("hello", 10)
        
        suggestions = self.autocomplete.get_suggestions("xyz", max_results=5)
        self.assertEqual(len(suggestions), 0)
    
    def test_get_suggestions_max_results(self):
        """Test that max_results is respected."""
        words = ["hello", "help", "here", "hero", "herb"]
        for word in words:
            self.autocomplete.add_word(word)
        
        suggestions = self.autocomplete.get_suggestions("he", max_results=3)
        self.assertEqual(len(suggestions), 3)
    
    def test_get_top_suggestions(self):
        """Test getting top suggestions as strings only."""
        words_with_freq = [
            ("python", 100), ("programming", 80), ("data", 90)
        ]
        
        for word, freq in words_with_freq:
            self.autocomplete.add_word(word, freq)
        
        suggestions = self.autocomplete.get_top_suggestions("p", max_results=2)
        self.assertEqual(len(suggestions), 2)
        self.assertIsInstance(suggestions[0], str)
        self.assertIn("python", suggestions)
        self.assertIn("programming", suggestions)
    
    def test_update_frequency(self):
        """Test updating word frequency."""
        self.autocomplete.add_word("hello", 10)
        
        self.autocomplete.update_frequency("hello", 5)
        self.assertEqual(self.autocomplete._word_frequencies["hello"], 15)
        self.assertEqual(self.autocomplete._trie.search("hello"), 15)
    
    def test_update_frequency_nonexistent_word(self):
        """Test updating frequency of non-existent word."""
        self.autocomplete.update_frequency("nonexistent", 5)
        
        # Should not add the word
        self.assertEqual(len(self.autocomplete), 0)
        self.assertNotIn("nonexistent", self.autocomplete._word_frequencies)
    
    def test_get_statistics(self):
        """Test getting system statistics."""
        words_with_freq = [
            ("python", 100), ("programming", 80), ("data", 90)
        ]
        
        for word, freq in words_with_freq:
            self.autocomplete.add_word(word, freq)
        
        stats = self.autocomplete.get_statistics()
        
        self.assertEqual(stats['total_words'], 3)
        self.assertEqual(stats['total_frequency'], 270)
        self.assertEqual(stats['average_frequency'], 90.0)
        self.assertEqual(stats['trie_size'], 3)
        self.assertEqual(stats['most_frequent'], ("python", 100))
    
    def test_get_statistics_empty_system(self):
        """Test getting statistics for empty system."""
        stats = self.autocomplete.get_statistics()
        
        self.assertEqual(stats['total_words'], 0)
        self.assertEqual(stats['total_frequency'], 0)
        self.assertEqual(stats['average_frequency'], 0)
        self.assertEqual(stats['trie_size'], 0)
        self.assertIsNone(stats['most_frequent'])
    
    def test_contains(self):
        """Test contains operation."""
        self.autocomplete.add_word("hello", 10)
        
        self.assertIn("hello", self.autocomplete)
        self.assertNotIn("world", self.autocomplete)
    
    def test_len(self):
        """Test length operation."""
        self.assertEqual(len(self.autocomplete), 0)
        
        self.autocomplete.add_word("hello")
        self.assertEqual(len(self.autocomplete), 1)
        
        self.autocomplete.add_word("world")
        self.assertEqual(len(self.autocomplete), 2)

if __name__ == '__main__':
    unittest.main() 