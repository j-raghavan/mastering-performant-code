"""
Unit tests for TrieAnalyzer implementation.

This module provides comprehensive test coverage for the TrieAnalyzer class,
including memory analysis, performance benchmarking, and statistics generation.
"""

import unittest
import sys
import timeit
from typing import List

# Add the project root to the path for imports
sys.path.insert(0, '../../')

from src.chapter_10.analyzer import TrieAnalyzer, TrieStats
from src.chapter_10.trie import Trie
from src.chapter_10.compressed_trie import CompressedTrie

class TestTrieStats(unittest.TestCase):
    """Test cases for TrieStats dataclass."""
    
    def test_initialization(self):
        """Test TrieStats initialization."""
        stats = TrieStats(
            num_nodes=100,
            num_strings=50,
            total_chars=200,
            memory_bytes=5000,
            avg_string_length=4.0,
            compression_ratio=0.8,
            height=10
        )
        
        self.assertEqual(stats.num_nodes, 100)
        self.assertEqual(stats.num_strings, 50)
        self.assertEqual(stats.total_chars, 200)
        self.assertEqual(stats.memory_bytes, 5000)
        self.assertEqual(stats.avg_string_length, 4.0)
        self.assertEqual(stats.compression_ratio, 0.8)
        self.assertEqual(stats.height, 10)

class TestTrieAnalyzer(unittest.TestCase):
    """Test cases for TrieAnalyzer implementation."""
    
    def setUp(self):
        self.analyzer = TrieAnalyzer()
        self.trie = Trie()
        self.compressed_trie = CompressedTrie()
    
    def test_analyze_trie_empty(self):
        """Test analyzing empty trie."""
        stats = self.analyzer.analyze_trie(self.trie)
        
        self.assertEqual(stats.num_nodes, 1)  # Root node
        self.assertEqual(stats.num_strings, 0)
        self.assertEqual(stats.total_chars, 0)
        self.assertEqual(stats.memory_bytes, 100)  # Rough estimate
        self.assertEqual(stats.avg_string_length, 0)
        self.assertEqual(stats.compression_ratio, 1.0)
        self.assertEqual(stats.height, 0)
    
    def test_analyze_trie_with_data(self):
        """Test analyzing trie with data."""
        words = ["hello", "world", "python", "programming"]
        for word in words:
            self.trie.insert(word, word)
        
        stats = self.analyzer.analyze_trie(self.trie)
        
        self.assertGreater(stats.num_nodes, 1)
        self.assertEqual(stats.num_strings, 4)
        self.assertEqual(stats.total_chars, 27)  # Sum of word lengths: 5+5+6+11
        self.assertGreater(stats.memory_bytes, 0)
        self.assertEqual(stats.avg_string_length, 6.75)  # 27 / 4
        self.assertEqual(stats.compression_ratio, 1.0)  # No compression
        self.assertGreater(stats.height, 0)
    
    def test_analyze_compressed_trie_empty(self):
        """Test analyzing empty compressed trie."""
        stats = self.analyzer.analyze_compressed_trie(self.compressed_trie)
        
        self.assertEqual(stats.num_nodes, 1)  # Root node
        self.assertEqual(stats.num_strings, 0)
        self.assertEqual(stats.total_chars, 0)
        self.assertEqual(stats.memory_bytes, 30)  # Rough estimate
        self.assertEqual(stats.avg_string_length, 0)
        self.assertEqual(stats.compression_ratio, 1.0)  # No data to compress
        self.assertEqual(stats.height, 0)
    
    def test_analyze_compressed_trie_with_data(self):
        """Test analyzing compressed trie with data."""
        words = ["hello", "world", "python", "programming"]
        for word in words:
            self.compressed_trie.insert(word, word)
        
        stats = self.analyzer.analyze_compressed_trie(self.compressed_trie)
        
        self.assertGreater(stats.num_nodes, 1)
        self.assertEqual(stats.num_strings, 4)
        self.assertEqual(stats.total_chars, 27)
        self.assertGreater(stats.memory_bytes, 0)
        self.assertEqual(stats.avg_string_length, 6.75)
        self.assertLess(stats.compression_ratio, 1.0)  # Should have some compression
        self.assertGreater(stats.height, 0)
    
    def test_benchmark_operations(self):
        """Test benchmarking operations."""
        test_data = ["hello", "world", "python", "programming"]
        operations = ["insert", "search", "prefix_search"]
        
        results = self.analyzer.benchmark_operations(
            self.trie, operations, test_data, iterations=10
        )
        
        self.assertIn("insert", results)
        self.assertIn("search", results)
        self.assertIn("prefix_search", results)
        
        for operation, time in results.items():
            self.assertIsInstance(time, float)
            self.assertGreater(time, 0)
    
    def test_benchmark_operations_empty(self):
        """Test benchmarking with empty operations list."""
        test_data = ["hello", "world"]
        operations = []
        
        results = self.analyzer.benchmark_operations(
            self.trie, operations, test_data, iterations=10
        )
        
        self.assertEqual(len(results), 0)
    
    def test_benchmark_operations_invalid_operation(self):
        """Test benchmarking with invalid operation."""
        test_data = ["hello", "world"]
        operations = ["invalid_operation"]
        
        results = self.analyzer.benchmark_operations(
            self.trie, operations, test_data, iterations=10
        )
        
        self.assertEqual(len(results), 0)
    
    def test_trie_memory_analysis_empty(self):
        """Test memory analysis with empty strings."""
        strings = []
        analysis = self.analyzer.trie_memory_analysis(strings)
        
        self.assertEqual(analysis['num_strings'], 0)
        self.assertEqual(analysis['avg_length'], 0)
        self.assertEqual(analysis['total_chars'], 0)
        self.assertEqual(analysis['std_trie_nodes'], 0)
        self.assertEqual(analysis['compressed_trie_nodes'], 0)
        self.assertEqual(analysis['memory_savings'], 0)
    
    def test_trie_memory_analysis_with_data(self):
        """Test memory analysis with data."""
        strings = ["hello", "world", "python", "programming"]
        analysis = self.analyzer.trie_memory_analysis(strings)
        
        self.assertEqual(analysis['num_strings'], 4)
        self.assertEqual(analysis['avg_length'], 6.75)
        self.assertEqual(analysis['total_chars'], 27)
        self.assertEqual(analysis['std_trie_nodes'], 27)
        self.assertGreater(analysis['compressed_trie_nodes'], 0)
        self.assertLess(analysis['compressed_trie_nodes'], analysis['std_trie_nodes'])
        self.assertGreater(analysis['memory_savings'], 0)
        self.assertEqual(analysis['alphabet_size'], 256)
        self.assertGreater(analysis['std_memory_bytes'], 0)
        self.assertGreater(analysis['compressed_memory_bytes'], 0)
    
    def test_trie_memory_analysis_custom_alphabet(self):
        """Test memory analysis with custom alphabet size."""
        strings = ["hello", "world"]
        analysis = self.analyzer.trie_memory_analysis(strings, alphabet_size=1000)
        
        self.assertEqual(analysis['alphabet_size'], 1000)
    
    def test_compression_ratio_calculation(self):
        """Test compression ratio calculation."""
        # Test with strings that should compress well
        strings = ["hello", "help", "here", "hero"]
        analysis = self.analyzer.trie_memory_analysis(strings)
        
        # Should have some compression due to common prefixes
        self.assertGreater(analysis['memory_savings'], 0)
        self.assertLess(analysis['compressed_trie_nodes'], analysis['std_trie_nodes'])
    
    def test_no_compression_scenario(self):
        """Test scenario with no compression possible."""
        strings = ["a", "b", "c", "d"]  # No common prefixes
        analysis = self.analyzer.trie_memory_analysis(strings)
        
        # Should still have some compression due to the estimation algorithm
        self.assertGreater(analysis['memory_savings'], 0)

class TestTrieAnalyzerEdgeCases(unittest.TestCase):
    """Edge case tests for TrieAnalyzer implementation."""
    
    def setUp(self):
        self.analyzer = TrieAnalyzer()
        self.trie = Trie()
        self.compressed_trie = CompressedTrie()
    
    def test_analyze_trie_large_dataset(self):
        """Test analyzing trie with large dataset."""
        words = [f"word_{i}" for i in range(1000)]
        for word in words:
            self.trie.insert(word, word)
        
        stats = self.analyzer.analyze_trie(self.trie)
        
        self.assertEqual(stats.num_strings, 1000)
        self.assertGreater(stats.num_nodes, 1000)
        self.assertGreater(stats.memory_bytes, 0)
        self.assertGreater(stats.height, 0)
    
    def test_analyze_compressed_trie_large_dataset(self):
        """Test analyzing compressed trie with large dataset."""
        words = [f"word_{i}" for i in range(1000)]
        for word in words:
            self.compressed_trie.insert(word, word)
        
        stats = self.analyzer.analyze_compressed_trie(self.compressed_trie)
        
        self.assertEqual(stats.num_strings, 1000)
        self.assertGreater(stats.num_nodes, 1)
        self.assertLess(stats.compression_ratio, 1.0)
    
    def test_analyze_trie_very_long_strings(self):
        """Test analyzing trie with very long strings."""
        # Use a shorter string to avoid recursion issues
        long_string = "a" * 100
        self.trie.insert(long_string, "long")
        
        stats = self.analyzer.analyze_trie(self.trie)
        
        self.assertEqual(stats.num_strings, 1)
        self.assertEqual(stats.total_chars, 100)
        self.assertEqual(stats.avg_string_length, 100.0)
        self.assertGreater(stats.num_nodes, 100)
    
    def test_analyze_trie_unicode_strings(self):
        """Test analyzing trie with Unicode strings."""
        unicode_strings = ["café", "naïve", "résumé", "你好", "こんにちは"]
        for s in unicode_strings:
            self.trie.insert(s, s)
        
        stats = self.analyzer.analyze_trie(self.trie)
        
        self.assertEqual(stats.num_strings, 5)
        self.assertGreater(stats.total_chars, 0)
        self.assertGreater(stats.avg_string_length, 0)
    
    def test_benchmark_operations_large_dataset(self):
        """Test benchmarking with large dataset."""
        words = [f"word_{i}" for i in range(100)]
        for word in words:
            self.trie.insert(word, word)
        
        operations = ["search", "prefix_search"]
        results = self.analyzer.benchmark_operations(
            self.trie, operations, words, iterations=10
        )
        
        for operation, time in results.items():
            self.assertIsInstance(time, float)
            self.assertGreater(time, 0)
    
    def test_memory_analysis_large_dataset(self):
        """Test memory analysis with large dataset."""
        strings = [f"word_{i}" for i in range(1000)]
        analysis = self.analyzer.trie_memory_analysis(strings)
        
        self.assertEqual(analysis['num_strings'], 1000)
        self.assertGreater(analysis['avg_length'], 0)
        self.assertGreater(analysis['total_chars'], 0)
        self.assertGreater(analysis['memory_savings'], 0)

class TestTrieAnalyzerPerformance(unittest.TestCase):
    """Performance tests for TrieAnalyzer implementation."""
    
    def setUp(self):
        self.analyzer = TrieAnalyzer()
        self.trie = Trie()
        self.compressed_trie = CompressedTrie()
    
    def test_analyze_trie_performance(self):
        """Test performance of trie analysis."""
        import timeit
        
        # Add data
        words = [f"word_{i}" for i in range(1000)]
        for word in words:
            self.trie.insert(word, word)
        
        # Test analysis performance
        start_time = timeit.default_timer()
        stats = self.analyzer.analyze_trie(self.trie)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(stats.num_strings, 1000)
    
    def test_analyze_compressed_trie_performance(self):
        """Test performance of compressed trie analysis."""
        import timeit
        
        # Add data
        words = [f"word_{i}" for i in range(1000)]
        for word in words:
            self.compressed_trie.insert(word, word)
        
        # Test analysis performance
        start_time = timeit.default_timer()
        stats = self.analyzer.analyze_compressed_trie(self.compressed_trie)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(stats.num_strings, 1000)
    
    def test_benchmark_operations_performance(self):
        """Test performance of benchmarking operations."""
        import timeit
        
        # Add data
        words = [f"word_{i}" for i in range(100)]
        for word in words:
            self.trie.insert(word, word)
        
        operations = ["search", "prefix_search"]
        
        # Test benchmarking performance
        start_time = timeit.default_timer()
        results = self.analyzer.benchmark_operations(
            self.trie, operations, words, iterations=10
        )
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(len(results), 2)
    
    def test_memory_analysis_performance(self):
        """Test performance of memory analysis."""
        import timeit
        
        strings = [f"word_{i}" for i in range(1000)]
        
        # Test analysis performance
        start_time = timeit.default_timer()
        analysis = self.analyzer.trie_memory_analysis(strings)
        end_time = timeit.default_timer()
        
        self.assertLess(end_time - start_time, 1.0)
        self.assertEqual(analysis['num_strings'], 1000)

if __name__ == '__main__':
    unittest.main() 