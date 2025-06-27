"""
Unit tests for SpellChecker implementation.

This module provides comprehensive test coverage for the SpellChecker class,
including dictionary lookup, suggestion generation, and text checking.
"""

import unittest
from typing import List

from mastering_performant_code.chapter_10.spell_checker import SpellChecker

class TestSpellChecker(unittest.TestCase):
    """Test cases for SpellChecker implementation."""
    
    def setUp(self):
        self.spell_checker = SpellChecker()
    
    def test_initialization_empty(self):
        """Test initialization without dictionary."""
        self.assertEqual(self.spell_checker.get_dictionary_size(), 0)
    
    def test_initialization_with_dictionary(self):
        """Test initialization with dictionary."""
        dictionary = ["hello", "world", "python", "programming"]
        spell_checker = SpellChecker(dictionary)
        
        self.assertEqual(spell_checker.get_dictionary_size(), 4)
        for word in dictionary:
            self.assertTrue(spell_checker.is_correct(word))
    
    def test_add_dictionary(self):
        """Test adding dictionary."""
        dictionary = ["hello", "world", "python", "programming"]
        self.spell_checker.add_dictionary(dictionary)
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 4)
        for word in dictionary:
            self.assertTrue(self.spell_checker.is_correct(word))
    
    def test_add_word(self):
        """Test adding a single word."""
        self.spell_checker.add_word("hello")
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 1)
        self.assertTrue(self.spell_checker.is_correct("hello"))
        self.assertFalse(self.spell_checker.is_correct("world"))
    
    def test_is_correct(self):
        """Test spell checking."""
        dictionary = ["hello", "world", "python", "programming"]
        self.spell_checker.add_dictionary(dictionary)
        
        # Correct words
        for word in dictionary:
            self.assertTrue(self.spell_checker.is_correct(word))
        
        # Incorrect words
        incorrect_words = ["helo", "wold", "pythn", "progrmming"]
        for word in incorrect_words:
            self.assertFalse(self.spell_checker.is_correct(word))
    
    def test_is_correct_case_sensitive(self):
        """Test case sensitivity in spell checking."""
        # Add words in lowercase
        self.spell_checker.add_word("hello")
        self.spell_checker.add_word("world")
        
        # Should be case-insensitive
        self.assertTrue(self.spell_checker.is_correct("Hello"))
        self.assertTrue(self.spell_checker.is_correct("WORLD"))
        self.assertTrue(self.spell_checker.is_correct("hello"))
        self.assertTrue(self.spell_checker.is_correct("world"))
        
        # Misspelled words should be incorrect regardless of case
        self.assertFalse(self.spell_checker.is_correct("helo"))
        self.assertFalse(self.spell_checker.is_correct("HELO"))
    
    def test_get_suggestions(self):
        """Test getting spelling suggestions."""
        dictionary = ["hello", "help", "here", "hero", "herb", "world"]
        self.spell_checker.add_dictionary(dictionary)
        
        # Test suggestions for misspelled word
        suggestions = self.spell_checker.get_suggestions("helo", max_suggestions=3)
        self.assertGreater(len(suggestions), 0)
        self.assertLessEqual(len(suggestions), 3)
        
        # Should suggest words with similar prefixes
        for suggestion in suggestions:
            self.assertIn(suggestion, dictionary)
    
    def test_get_suggestions_no_matches(self):
        """Test getting suggestions when no matches exist."""
        self.spell_checker.add_word("hello")
        
        suggestions = self.spell_checker.get_suggestions("xyz", max_suggestions=5)
        self.assertEqual(len(suggestions), 0)
    
    def test_get_suggestions_max_suggestions(self):
        """Test that max_suggestions is respected."""
        dictionary = ["hello", "help", "here", "hero", "herb", "world"]
        self.spell_checker.add_dictionary(dictionary)
        
        suggestions = self.spell_checker.get_suggestions("helo", max_suggestions=2)
        self.assertLessEqual(len(suggestions), 2)
    
    def test_check_text(self):
        """Test checking spelling in text."""
        dictionary = ["hello", "world", "python", "programming"]
        self.spell_checker.add_dictionary(dictionary)
        
        text = "hello world pythn programing"
        errors = self.spell_checker.check_text(text)
        
        self.assertEqual(len(errors), 2)  # "pythn" and "programing" are misspelled
        
        # Check error details
        misspelled_words = [error[0] for error in errors]
        self.assertIn("pythn", misspelled_words)
        self.assertIn("programing", misspelled_words)
    
    def test_check_text_with_punctuation(self):
        """Test spell checking text with punctuation."""
        text = "How are you? I am fine."
        errors = self.spell_checker.check_text(text)
        
        # Should find misspelled words
        self.assertGreater(len(errors), 0)
        
        # Check that we get word, position, and suggestions for each error
        for word, position, suggestions in errors:
            self.assertIsInstance(word, str)
            self.assertIsInstance(position, int)
            self.assertIsInstance(suggestions, list)
    
    def test_check_text_empty(self):
        """Test checking empty text."""
        self.spell_checker.add_word("hello")
        
        errors = self.spell_checker.check_text("")
        self.assertEqual(len(errors), 0)
    
    def test_get_dictionary_size(self):
        """Test getting dictionary size."""
        self.assertEqual(self.spell_checker.get_dictionary_size(), 0)
        
        self.spell_checker.add_word("hello")
        self.assertEqual(self.spell_checker.get_dictionary_size(), 1)
        
        self.spell_checker.add_word("world")
        self.assertEqual(self.spell_checker.get_dictionary_size(), 2)
    
    def test_contains(self):
        """Test contains operation."""
        self.spell_checker.add_word("hello")
        
        self.assertIn("hello", self.spell_checker)
        self.assertNotIn("world", self.spell_checker)
    
    def test_duplicate_words(self):
        """Test adding duplicate words."""
        self.spell_checker.add_word("hello")
        self.spell_checker.add_word("hello")
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 1)
        self.assertTrue(self.spell_checker.is_correct("hello"))

class TestSpellCheckerEdgeCases(unittest.TestCase):
    """Edge case tests for SpellChecker implementation."""
    
    def setUp(self):
        self.spell_checker = SpellChecker()
    
    def test_empty_strings(self):
        """Test handling of empty strings."""
        # Empty string should not be considered correct
        self.assertFalse(self.spell_checker.is_correct(""))
        
        # Adding empty string should be ignored
        self.spell_checker.add_word("")
        self.assertFalse(self.spell_checker.is_correct(""))
        
        # Empty string should not be in dictionary
        self.assertEqual(self.spell_checker.get_dictionary_size(), 0)
    
    def test_unicode_strings(self):
        """Test with Unicode strings."""
        unicode_words = ["café", "naïve", "résumé", "你好", "こんにちは"]
        self.spell_checker.add_dictionary(unicode_words)
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 5)
        
        for word in unicode_words:
            self.assertTrue(self.spell_checker.is_correct(word))
        
        # Test suggestions for misspelled Unicode word
        suggestions = self.spell_checker.get_suggestions("cafe", max_suggestions=1)
        self.assertGreater(len(suggestions), 0)
    
    def test_special_characters(self):
        """Test with special characters."""
        special_words = ["hello@world", "test#123", "user.name", "file/path"]
        self.spell_checker.add_dictionary(special_words)
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 4)
        
        for word in special_words:
            self.assertTrue(self.spell_checker.is_correct(word))
    
    def test_very_long_words(self):
        """Test with very long words."""
        long_word = "a" * 1000
        self.spell_checker.add_word(long_word)
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 1)
        self.assertTrue(self.spell_checker.is_correct(long_word))
    
    def test_numbers_and_symbols(self):
        """Test with numbers and symbols."""
        mixed_words = ["hello123", "test@email.com", "user_name", "file-path"]
        self.spell_checker.add_dictionary(mixed_words)
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 4)
        
        for word in mixed_words:
            self.assertTrue(self.spell_checker.is_correct(word))
    
    def test_max_suggestions_zero(self):
        """Test with max_suggestions set to zero."""
        self.spell_checker.add_word("hello")
        
        suggestions = self.spell_checker.get_suggestions("helo", max_suggestions=0)
        self.assertEqual(len(suggestions), 0)
    
    def test_max_suggestions_negative(self):
        """Test with negative max_suggestions."""
        self.spell_checker.add_word("hello")
        
        suggestions = self.spell_checker.get_suggestions("helo", max_suggestions=-1)
        self.assertEqual(len(suggestions), 0)
    
    def test_large_dictionary(self):
        """Test with large dictionary."""
        large_dictionary = [f"word_{i}" for i in range(10000)]
        self.spell_checker.add_dictionary(large_dictionary)
        
        self.assertEqual(self.spell_checker.get_dictionary_size(), 10000)
        
        # Test some words
        self.assertTrue(self.spell_checker.is_correct("word_0"))
        self.assertTrue(self.spell_checker.is_correct("word_9999"))
        self.assertFalse(self.spell_checker.is_correct("nonexistent"))

class TestSpellCheckerPerformance(unittest.TestCase):
    """Performance tests for SpellChecker implementation."""
    
    def setUp(self):
        self.spell_checker = SpellChecker()
    
    def test_large_dictionary_performance(self):
        """Test performance with large dictionary."""
        import timeit
        
        # Add many words
        words = [f"word_{i}" for i in range(10000)]
        self.spell_checker.add_dictionary(words)
        
        # Test spell checking performance
        start_time = timeit.default_timer()
        for i in range(1000):
            word = f"word_{i}"
            is_correct = self.spell_checker.is_correct(word)
            self.assertTrue(is_correct)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
    
    def test_suggestion_performance(self):
        """Test suggestion generation performance."""
        import timeit
        
        # Add words
        words = [f"word_{i}" for i in range(1000)]
        self.spell_checker.add_dictionary(words)
        
        # Test suggestion performance
        start_time = timeit.default_timer()
        for i in range(100):
            misspelled = f"word_{i}x"  # Add extra character
            suggestions = self.spell_checker.get_suggestions(misspelled, max_suggestions=5)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
    
    def test_text_checking_performance(self):
        """Test text checking performance."""
        import timeit
        
        # Add words
        words = [f"word_{i}" for i in range(1000)]
        self.spell_checker.add_dictionary(words)
        
        # Create test text
        text = " ".join([f"word_{i}" if i % 2 == 0 else f"misspelled_{i}" for i in range(100)])
        
        # Test text checking performance
        start_time = timeit.default_timer()
        errors = self.spell_checker.check_text(text)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)

if __name__ == '__main__':
    unittest.main() 