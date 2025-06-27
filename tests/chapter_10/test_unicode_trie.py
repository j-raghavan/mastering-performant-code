"""
Unit tests for UnicodeTrie implementation.

This module provides comprehensive test coverage for the UnicodeTrie class,
including Unicode normalization, case folding, and international text handling.
"""

import unittest
import unicodedata

from mastering_performant_code.chapter_10.unicode_trie import UnicodeTrie

class TestUnicodeTrie(unittest.TestCase):
    """Test cases for UnicodeTrie implementation."""
    
    def setUp(self):
        self.trie = UnicodeTrie()
    
    def test_initialization(self):
        """Test trie initialization with different options."""
        # Default settings
        trie = UnicodeTrie()
        self.assertTrue(trie._normalize)
        self.assertTrue(trie._case_sensitive)
        
        # Custom settings
        trie = UnicodeTrie(normalize=False, case_sensitive=False)
        self.assertFalse(trie._normalize)
        self.assertFalse(trie._case_sensitive)
    
    def test_normalization(self):
        """Test Unicode normalization."""
        trie = UnicodeTrie(normalize=True, case_sensitive=True)
        
        # Test NFC normalization
        trie.insert("café", "coffee")
        trie.insert("cafe\u0301", "coffee2")  # Decomposed form
        
        # Both should be normalized to the same form
        self.assertEqual(trie.search("café"), "coffee2")  # Last inserted wins
        self.assertEqual(trie.search("cafe\u0301"), "coffee2")
    
    def test_case_insensitive(self):
        """Test case-insensitive behavior."""
        trie = UnicodeTrie(normalize=True, case_sensitive=False)
        
        trie.insert("Hello", "world")
        
        # All case variations should match
        self.assertEqual(trie.search("hello"), "world")
        self.assertEqual(trie.search("HELLO"), "world")
        self.assertEqual(trie.search("Hello"), "world")
        self.assertEqual(trie.search("hElLo"), "world")
    
    def test_case_sensitive(self):
        """Test case-sensitive behavior."""
        trie = UnicodeTrie(normalize=True, case_sensitive=True)
        
        trie.insert("Hello", "world")
        trie.insert("hello", "world2")
        
        # Different cases should be treated as different
        self.assertEqual(trie.search("Hello"), "world")
        self.assertEqual(trie.search("hello"), "world2")
        self.assertIsNone(trie.search("HELLO"))
    
    def test_unicode_strings(self):
        """Test with various Unicode strings."""
        trie = UnicodeTrie()
        
        unicode_strings = [
            "café", "naïve", "résumé", "façade",
            "你好", "こんにちは", "안녕하세요", "مرحبا",
            "Привет", "Hola", "Bonjour", "Ciao"
        ]
        
        for i, s in enumerate(unicode_strings):
            trie.insert(s, f"value_{i}")
        
        for i, s in enumerate(unicode_strings):
            self.assertEqual(trie.search(s), f"value_{i}")
    
    def test_combining_characters(self):
        """Test combining characters."""
        trie = UnicodeTrie(normalize=True)
        
        # Test with combining characters
        trie.insert("e\u0301", "e with acute")  # e + combining acute
        trie.insert("é", "e acute")  # precomposed e acute
        
        # Both should be normalized to the same form
        self.assertEqual(trie.search("e\u0301"), "e acute")
        self.assertEqual(trie.search("é"), "e acute")
    
    def test_prefix_search_unicode(self):
        """Test prefix search with Unicode."""
        trie = UnicodeTrie()
        
        trie.insert("café", "coffee")
        trie.insert("cafeteria", "dining hall")
        trie.insert("caffeine", "stimulant")
        
        results = trie.get_all_with_prefix("café")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "café")
        
        results = trie.get_all_with_prefix("caf")
        self.assertEqual(len(results), 3)
    
    def test_autocomplete_unicode(self):
        """Test autocomplete with Unicode strings."""
        self.trie.insert("café", "coffee")
        self.trie.insert("cafeteria", "dining hall")
        self.trie.insert("naïve", "innocent")
        
        suggestions = self.trie.autocomplete("café", 5)
        expected = ["café"]  # Only "café" starts with "café" (with accent)
        self.assertEqual(set(suggestions), set(expected))
        
        # Test with partial Unicode prefix
        suggestions = self.trie.autocomplete("caf", 5)
        expected = ["café", "cafeteria"]  # Both start with "caf"
        self.assertEqual(set(suggestions), set(expected))
    
    def test_case_folding_edge_cases(self):
        """Test case folding with edge cases."""
        # Test with Turkish i
        self.trie.insert("i", "lowercase i")
        self.trie.insert("I", "uppercase I")
        
        # In case-insensitive mode, both should be the same
        if not self.trie._case_sensitive:
            self.assertEqual(self.trie.search("i"), self.trie.search("I"))
        else:
            self.assertNotEqual(self.trie.search("i"), self.trie.search("I"))
    
    def test_normalization_edge_cases(self):
        """Test edge cases in normalization."""
        trie = UnicodeTrie(normalize=True)
        
        # Test with various normalization scenarios
        trie.insert("Å", "a with ring")  # A with ring above
        trie.insert("A\u030A", "a with ring decomposed")  # A + combining ring
        
        # Both should be normalized to the same form
        self.assertEqual(trie.search("Å"), "a with ring decomposed")
        self.assertEqual(trie.search("A\u030A"), "a with ring decomposed")
    
    def test_mixed_unicode_ascii(self):
        """Test mixing Unicode and ASCII strings."""
        trie = UnicodeTrie()
        
        trie.insert("hello", "english")
        trie.insert("café", "french")
        trie.insert("你好", "chinese")
        trie.insert("こんにちは", "japanese")
        
        self.assertEqual(trie.search("hello"), "english")
        self.assertEqual(trie.search("café"), "french")
        self.assertEqual(trie.search("你好"), "chinese")
        self.assertEqual(trie.search("こんにちは"), "japanese")
    
    def test_delete_unicode(self):
        """Test delete operation with Unicode."""
        trie = UnicodeTrie()
        
        trie.insert("café", "coffee")
        trie.insert("你好", "hello")
        
        self.assertTrue(trie.delete("café"))
        self.assertIsNone(trie.search("café"))
        self.assertEqual(trie.search("你好"), "hello")
        
        self.assertTrue(trie.delete("你好"))
        self.assertIsNone(trie.search("你好"))
    
    def test_contains_unicode(self):
        """Test contains operation with Unicode."""
        trie = UnicodeTrie()
        
        trie.insert("café", "coffee")
        
        self.assertIn("café", trie)
        self.assertNotIn("cafe", trie)  # Without accent
        self.assertNotIn("你好", trie)
    
    def test_dictionary_access_unicode(self):
        """Test dictionary-style access with Unicode."""
        trie = UnicodeTrie()
        
        trie["café"] = "coffee"
        trie["你好"] = "hello"
        
        self.assertEqual(trie["café"], "coffee")
        self.assertEqual(trie["你好"], "hello")
        
        with self.assertRaises(KeyError):
            _ = trie["nonexistent"]
    
    def test_starts_with_unicode(self):
        """Test starts_with with Unicode strings."""
        self.trie.insert("café", "coffee")
        self.trie.insert("naïve", "innocent")
        
        # Test with Unicode prefix
        self.assertTrue(self.trie.starts_with("caf"))
        self.assertTrue(self.trie.starts_with("naï"))
        
        # Test with non-existent Unicode prefix
        self.assertFalse(self.trie.starts_with("xyz"))
        self.assertFalse(self.trie.starts_with("caféx"))
    
    def test_get_all_strings_unicode(self):
        """Test get_all_strings with Unicode."""
        trie = UnicodeTrie()
        
        unicode_strings = ["café", "你好", "こんにちは"]
        for s in unicode_strings:
            trie.insert(s, s)
        
        all_strings = trie.get_all_strings()
        self.assertEqual(len(all_strings), 3)
        
        for s, value in all_strings:
            self.assertIn(s, unicode_strings)
            self.assertEqual(s, value)

class TestUnicodeTriePerformance(unittest.TestCase):
    """Performance tests for UnicodeTrie implementation."""
    
    def setUp(self):
        self.trie = UnicodeTrie()
    
    def test_unicode_insert_performance(self):
        """Test insert performance with Unicode strings."""
        unicode_strings = [
            "café", "naïve", "résumé", "façade",
            "你好", "こんにちは", "안녕하세요", "مرحبا"
        ] * 100  # Repeat to get more strings
        
        import timeit
        start_time = timeit.default_timer()
        for s in unicode_strings:
            self.trie.insert(s, s)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
    
    def test_unicode_search_performance(self):
        """Test search performance with Unicode strings."""
        unicode_strings = [
            "café", "naïve", "résumé", "façade",
            "你好", "こんにちは", "안녕하세요", "مرحبا"
        ] * 100
        
        for s in unicode_strings:
            self.trie.insert(s, s)
        
        import timeit
        start_time = timeit.default_timer()
        for s in unicode_strings:
            result = self.trie.search(s)
            self.assertEqual(result, s)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)

if __name__ == '__main__':
    unittest.main() 