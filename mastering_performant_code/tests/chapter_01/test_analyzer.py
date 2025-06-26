"""
Unit tests for BuiltinAnalyzer implementation.

This module provides comprehensive test coverage for the BuiltinAnalyzer class,
including memory analysis, performance benchmarking, and comparison tests.
"""

import unittest
import timeit
from typing import List, Dict, Set

from chapter_01.analyzer import BuiltinAnalyzer, MemoryInfo

class TestBuiltinAnalyzer(unittest.TestCase):
    """Test cases for BuiltinAnalyzer implementation."""
    
    def test_analyze_list(self):
        """Test list analysis."""
        lst = [1, 2, 3, 4, 5]
        info = BuiltinAnalyzer.analyze_list(lst)
        
        self.assertIsInstance(info, MemoryInfo)
        self.assertGreater(info.object_size, 0)
        self.assertGreaterEqual(info.total_size, 0)
        self.assertGreaterEqual(info.overhead, 0)
        self.assertGreater(info.capacity, 0)
        self.assertGreaterEqual(info.load_factor, 0)
        self.assertLessEqual(info.load_factor, 1)
    
    def test_analyze_dict(self):
        """Test dict analysis."""
        dct = {"a": 1, "b": 2, "c": 3}
        info = BuiltinAnalyzer.analyze_dict(dct)
        
        self.assertIsInstance(info, MemoryInfo)
        self.assertGreater(info.object_size, 0)
        self.assertGreaterEqual(info.total_size, 0)
        self.assertGreaterEqual(info.overhead, 0)
        self.assertGreater(info.capacity, 0)
        self.assertGreaterEqual(info.load_factor, 0)
        self.assertLessEqual(info.load_factor, 1)
    
    def test_analyze_set(self):
        """Test set analysis."""
        st = {1, 2, 3, 4, 5}
        info = BuiltinAnalyzer.analyze_set(st)
        
        self.assertIsInstance(info, MemoryInfo)
        self.assertGreater(info.object_size, 0)
        self.assertGreaterEqual(info.total_size, 0)
        self.assertGreaterEqual(info.overhead, 0)
        self.assertGreater(info.capacity, 0)
        self.assertGreaterEqual(info.load_factor, 0)
        self.assertLessEqual(info.load_factor, 1)
    
    def test_analyze_empty_structures(self):
        """Test analysis of empty data structures."""
        # Empty list
        empty_list = []
        info = BuiltinAnalyzer.analyze_list(empty_list)
        self.assertEqual(info.capacity, 0)
        self.assertEqual(info.load_factor, 0)
        
        # Empty dict
        empty_dict = {}
        info = BuiltinAnalyzer.analyze_dict(empty_dict)
        self.assertEqual(info.capacity, 0)
        self.assertEqual(info.load_factor, 0)
        
        # Empty set
        empty_set = set()
        info = BuiltinAnalyzer.analyze_set(empty_set)
        self.assertEqual(info.capacity, 0)
        self.assertEqual(info.load_factor, 0)
    
    def test_analyze_large_structures(self):
        """Test analysis of large data structures."""
        # Large list
        large_list = list(range(1000))
        info = BuiltinAnalyzer.analyze_list(large_list)
        self.assertEqual(info.capacity, 1000)
        self.assertEqual(info.load_factor, 1.0)
        
        # Large dict
        large_dict = {f"key{i}": i for i in range(1000)}
        info = BuiltinAnalyzer.analyze_dict(large_dict)
        self.assertEqual(info.capacity, 1000)
        self.assertEqual(info.load_factor, 1.0)
        
        # Large set
        large_set = set(range(1000))
        info = BuiltinAnalyzer.analyze_set(large_set)
        self.assertEqual(info.capacity, 1000)
        self.assertEqual(info.load_factor, 1.0)
    
    def test_benchmark_operations(self):
        """Test benchmarking operations."""
        # Test with a simple list
        lst = [1, 2, 3, 4, 5]
        operations = ["append", "get"]
        results = BuiltinAnalyzer.benchmark_operations(lst, operations, iterations=100)
        
        self.assertIsInstance(results, dict)
        self.assertIn("append", results)
        self.assertIn("get", results)
        self.assertGreater(results["append"], 0)
        self.assertGreater(results["get"], 0)
    
    def test_benchmark_invalid_operations(self):
        """Test benchmarking with invalid operations."""
        lst = [1, 2, 3, 4, 5]
        operations = ["invalid_op", "append"]
        results = BuiltinAnalyzer.benchmark_operations(lst, operations, iterations=100)
        
        self.assertIsInstance(results, dict)
        self.assertIn("append", results)
        self.assertNotIn("invalid_op", results)
    
    def test_memory_info_dataclass(self):
        """Test MemoryInfo dataclass."""
        info = MemoryInfo(
            object_size=100,
            total_size=200,
            overhead=50,
            capacity=10,
            load_factor=0.5
        )
        
        self.assertEqual(info.object_size, 100)
        self.assertEqual(info.total_size, 200)
        self.assertEqual(info.overhead, 50)
        self.assertEqual(info.capacity, 10)
        self.assertEqual(info.load_factor, 0.5)


class TestBuiltinAnalyzerEdgeCases(unittest.TestCase):
    """Edge case tests for BuiltinAnalyzer."""
    
    def test_analyze_none_values(self):
        """Test analysis with None values."""
        lst = [None, None, None]
        info = BuiltinAnalyzer.analyze_list(lst)
        
        self.assertGreater(info.object_size, 0)
        self.assertGreaterEqual(info.total_size, 0)
    
    def test_analyze_string_values(self):
        """Test analysis with string values."""
        strings = ["hello", "world", "python"]
        info = BuiltinAnalyzer.analyze_list(strings)
        
        self.assertGreater(info.object_size, 0)
        self.assertGreaterEqual(info.total_size, 0)
    
    def test_analyze_mixed_types(self):
        """Test analysis with mixed types."""
        mixed = [1, "hello", 3.14, None, [1, 2, 3]]
        info = BuiltinAnalyzer.analyze_list(mixed)
        
        self.assertGreater(info.object_size, 0)
        self.assertGreaterEqual(info.total_size, 0)
    
    def test_benchmark_zero_iterations(self):
        """Test benchmarking with zero iterations."""
        lst = [1, 2, 3, 4, 5]
        operations = ["append"]
        results = BuiltinAnalyzer.benchmark_operations(lst, operations, iterations=0)
        
        self.assertIsInstance(results, dict)
        self.assertIn("append", results)
        self.assertLess(results["append"], 1e-5)


if __name__ == '__main__':
    unittest.main(verbosity=2) 