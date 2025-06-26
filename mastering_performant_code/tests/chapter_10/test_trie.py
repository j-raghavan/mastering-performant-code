"""
Unit tests for Trie implementation.

This module provides comprehensive test coverage for the Trie class,
including edge cases, performance tests, and memory analysis.
"""

import unittest
import timeit
from typing import List

# Add the project root to the path for imports
from chapter_10.trie import Trie, TrieNode

class TestTrieNode(unittest.TestCase):
    """Test cases for TrieNode implementation."""
    
    def test_initialization(self):
        """Test node initialization."""
        node = TrieNode()
        self.assertIsNone(node.char)
        self.assertFalse(node.is_end)
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children), 0)
        
        # Test with parameters
        node = TrieNode(char='a', is_end=True, value=42)
        self.assertEqual(node.char, 'a')
        self.assertTrue(node.is_end)
        self.assertEqual(node.value, 42)
    
    def test_post_init(self):
        """Test post-initialization behavior."""
        node = TrieNode(children=None)
        self.assertEqual(len(node.children), 0)

class TestTrie(unittest.TestCase):
    """Test cases for Trie implementation."""
    
    def setUp(self):
        self.trie = Trie[str]()
    
    def test_initialization(self):
        """Test trie initialization."""
        self.assertEqual(len(self.trie), 0)
        self.assertIsInstance(self.trie._root, TrieNode)
        self.assertFalse(self.trie._root.is_end)
    
    def test_insert(self):
        """Test insert operation."""
        self.trie.insert("hello", "world")
        self.assertEqual(len(self.trie), 1)
        self.assertEqual(self.trie.search("hello"), "world")
        
        # Test inserting same key again
        self.trie.insert("hello", "new_value")
        self.assertEqual(len(self.trie), 1)  # Size shouldn't change
        self.assertEqual(self.trie.search("hello"), "new_value")
        
        # Test inserting multiple strings
        self.trie.insert("hi", "there")
        self.trie.insert("help", "me")
        self.assertEqual(len(self.trie), 3)
    
    def test_insert_empty_string(self):
        """Test inserting empty string raises error."""
        with self.assertRaises(ValueError):
            self.trie.insert("")
    
    def test_search(self):
        """Test search operation."""
        self.trie.insert("hello", "world")
        self.trie.insert("hi", "there")
        
        self.assertEqual(self.trie.search("hello"), "world")
        self.assertEqual(self.trie.search("hi"), "there")
        self.assertIsNone(self.trie.search("nonexistent"))
        self.assertIsNone(self.trie.search("hel"))  # Prefix but not complete word
    
    def test_starts_with(self):
        """Test prefix search."""
        self.trie.insert("hello", "world")
        self.trie.insert("hi", "there")
        self.trie.insert("help", "me")
        
        self.assertTrue(self.trie.starts_with("hel"))
        self.assertTrue(self.trie.starts_with("hi"))
        self.assertFalse(self.trie.starts_with("xyz"))
        self.assertTrue(self.trie.starts_with(""))  # Empty prefix should match all
    
    def test_get_all_with_prefix(self):
        """Test getting all strings with prefix."""
        self.trie.insert("hello", "world")
        self.trie.insert("hi", "there")
        self.trie.insert("help", "me")
        self.trie.insert("goodbye", "friend")
        
        results = self.trie.get_all_with_prefix("hel")
        expected = [("hello", "world"), ("help", "me")]
        self.assertEqual(set(results), set(expected))
        
        # Test empty prefix
        all_results = self.trie.get_all_with_prefix("")
        self.assertEqual(len(all_results), 4)
    
    def test_autocomplete(self):
        """Test autocomplete functionality."""
        self.trie.insert("hello", "world")
        self.trie.insert("help", "me")
        self.trie.insert("hero", "zero")
        
        suggestions = self.trie.autocomplete("he", 5)
        expected = ["hello", "help", "hero"]
        self.assertEqual(set(suggestions), set(expected))
        
        # Test with limit
        suggestions = self.trie.autocomplete("he", 2)
        self.assertLessEqual(len(suggestions), 2)
        
        # Test with non-existent prefix
        suggestions = self.trie.autocomplete("xyz", 5)
        self.assertEqual(suggestions, [])
    
    def test_delete(self):
        """Test delete operation."""
        self.trie.insert("hello", "world")
        self.trie.insert("hi", "there")
        self.trie.insert("help", "me")
        
        # Delete existing word
        self.assertTrue(self.trie.delete("hello"))
        self.assertEqual(len(self.trie), 2)
        self.assertIsNone(self.trie.search("hello"))
        
        # Delete non-existent word
        self.assertFalse(self.trie.delete("nonexistent"))
        self.assertEqual(len(self.trie), 2)
        
        # Delete empty string
        self.assertFalse(self.trie.delete(""))
    
    def test_longest_common_prefix(self):
        """Test longest common prefix."""
        self.trie.insert("hello", "world")
        self.trie.insert("help", "me")
        self.trie.insert("hi", "there")
        
        self.assertEqual(self.trie.longest_common_prefix(), "h")
        
        # Test with no common prefix
        trie2 = Trie()
        trie2.insert("hello", "world")
        trie2.insert("world", "hello")
        self.assertEqual(trie2.longest_common_prefix(), "")
        
        # Test empty trie
        empty_trie = Trie()
        self.assertEqual(empty_trie.longest_common_prefix(), "")
    
    def test_get_all_strings(self):
        """Test getting all strings."""
        self.trie.insert("hello", "world")
        self.trie.insert("hi", "there")
        self.trie.insert("help", "me")
        
        all_strings = self.trie.get_all_strings()
        expected = [("hello", "world"), ("hi", "there"), ("help", "me")]
        self.assertEqual(set(all_strings), set(expected))
    
    def test_contains(self):
        """Test contains functionality."""
        self.trie.insert("hello", "world")
        self.trie.insert("help", "me")
        
        self.assertIn("hello", self.trie)
        self.assertIn("help", self.trie)
        self.assertNotIn("hel", self.trie)  # Not a complete word
        self.assertNotIn("world", self.trie)
    
    def test_getitem_setitem(self):
        """Test dictionary-style access."""
        self.trie["hello"] = "world"
        self.assertEqual(self.trie["hello"], "world")
        
        with self.assertRaises(KeyError):
            _ = self.trie["nonexistent"]
    
    def test_delitem(self):
        """Test dictionary-style deletion."""
        self.trie.insert("hello", "world")
        del self.trie["hello"]
        self.assertEqual(len(self.trie), 0)
        self.assertNotIn("hello", self.trie)
    
    def test_repr(self):
        """Test string representation."""
        self.assertEqual(repr(self.trie), "Trie()")
        
        self.trie.insert("hello", "world")
        self.trie.insert("hi", "there")
        self.assertIn("hello", repr(self.trie))
        self.assertIn("hi", repr(self.trie))

class TestTriePerformance(unittest.TestCase):
    """Performance tests for Trie implementation."""
    
    def setUp(self):
        self.trie = Trie[str]()
    
    def test_insert_performance(self):
        """Test insert performance."""
        words = [f"word_{i}" for i in range(1000)]
        
        start_time = timeit.default_timer()
        for word in words:
            self.trie.insert(word, word)
        end_time = timeit.default_timer()
        
        self.assertEqual(len(self.trie), 1000)
        self.assertLess(end_time - start_time, 1.0)  # Should complete in under 1 second
    
    def test_search_performance(self):
        """Test search performance."""
        words = [f"word_{i}" for i in range(1000)]
        for word in words:
            self.trie.insert(word, word)
        
        start_time = timeit.default_timer()
        for word in words:
            result = self.trie.search(word)
            self.assertEqual(result, word)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
    
    def test_prefix_search_performance(self):
        """Test prefix search performance."""
        words = [f"word_{i}" for i in range(1000)]
        for word in words:
            self.trie.insert(word, word)
        
        start_time = timeit.default_timer()
        for i in range(100):
            prefix = f"word_{i}"
            results = self.trie.get_all_with_prefix(prefix)
            self.assertGreater(len(results), 0)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)

class TestTrieEdgeCases(unittest.TestCase):
    """Edge case tests for Trie implementation."""
    
    def setUp(self):
        self.trie = Trie[str]()
    
    def test_large_number_of_words(self):
        """Test with a large number of words."""
        words = [f"word_{i}" for i in range(10000)]
        
        for word in words:
            self.trie.insert(word, word)
        
        self.assertEqual(len(self.trie), 10000)
        
        # Test search for some words
        for i in range(0, 10000, 1000):
            word = f"word_{i}"
            self.assertEqual(self.trie.search(word), word)
    
    def test_very_long_strings(self):
        """Test with very long strings."""
        long_string = "a" * 1000
        self.trie.insert(long_string, "long")
        
        self.assertEqual(self.trie.search(long_string), "long")
        self.assertTrue(self.trie.starts_with("a" * 500))
    
    def test_unicode_strings(self):
        """Test with Unicode strings."""
        unicode_strings = ["café", "naïve", "résumé", "你好", "こんにちは"]
        
        for s in unicode_strings:
            self.trie.insert(s, s)
        
        for s in unicode_strings:
            self.assertEqual(self.trie.search(s), s)
    
    def test_special_characters(self):
        """Test with special characters."""
        special_strings = ["hello@world", "test#123", "user.name", "file/path"]
        
        for s in special_strings:
            self.trie.insert(s, s)
        
        for s in special_strings:
            self.assertEqual(self.trie.search(s), s)
    
    def test_none_values(self):
        """Test with None values."""
        self.trie.insert("hello", None)
        self.assertIsNone(self.trie.search("hello"))
    
    def test_duplicate_insertions(self):
        """Test multiple insertions of the same key."""
        self.trie.insert("hello", "world")
        self.trie.insert("hello", "new_world")
        
        self.assertEqual(len(self.trie), 1)
        self.assertEqual(self.trie.search("hello"), "new_world")

if __name__ == '__main__':
    unittest.main() 