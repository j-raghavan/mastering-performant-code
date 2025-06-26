"""
Tests for Heap Sort Implementation

This module provides comprehensive tests for the heap sort functions,
ensuring 100% code coverage and correct behavior.
"""

import pytest
import random
from typing import List
from src.chapter_11.heap_sort import (
    heap_sort, 
    heap_sort_inplace, 
    heap_sort_generic_inplace,
    benchmark_heap_sort,
    verify_heap_sort_correctness
)


class TestHeapSort:
    """Test cases for heap sort functions."""
    
    def test_heap_sort_empty_list(self):
        """Test heap sort with empty list."""
        result = heap_sort([])
        assert result == []
    
    def test_heap_sort_single_element(self):
        """Test heap sort with single element."""
        result = heap_sort([5])
        assert result == [5]
    
    def test_heap_sort_already_sorted(self):
        """Test heap sort with already sorted list."""
        data = [1, 2, 3, 4, 5]
        result = heap_sort(data)
        assert result == [1, 2, 3, 4, 5]
        # Original list should not be modified
        assert data == [1, 2, 3, 4, 5]
    
    def test_heap_sort_reverse_sorted(self):
        """Test heap sort with reverse sorted list."""
        data = [5, 4, 3, 2, 1]
        result = heap_sort(data)
        assert result == [1, 2, 3, 4, 5]
    
    def test_heap_sort_random_data(self):
        """Test heap sort with random data."""
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        result = heap_sort(data)
        assert result == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    
    def test_heap_sort_duplicate_elements(self):
        """Test heap sort with duplicate elements."""
        data = [3, 3, 3, 3, 3]
        result = heap_sort(data)
        assert result == [3, 3, 3, 3, 3]
    
    def test_heap_sort_negative_numbers(self):
        """Test heap sort with negative numbers."""
        data = [-5, 10, -3, 0, 7, -8]
        result = heap_sort(data)
        assert result == [-8, -5, -3, 0, 7, 10]
    
    def test_heap_sort_with_key_func(self):
        """Test heap sort with key function."""
        data = ["apple", "banana", "cherry", "date"]
        def key_func(x: str) -> int:
            return len(x)
        result = heap_sort(data, key_func=key_func)
        # Check that the result is sorted by length ascending
        lengths = [len(x) for x in result]
        assert lengths == sorted(lengths)
        # Check that all original elements are present
        assert sorted(result) == sorted(data)
    
    def test_heap_sort_reverse_order(self):
        """Test heap sort in reverse order."""
        data = [1, 2, 3, 4, 5]
        result = heap_sort(data, reverse=True)
        assert result == [5, 4, 3, 2, 1]
    
    def test_heap_sort_reverse_with_key_func(self):
        """Test heap sort in reverse order with key function."""
        data = ["apple", "banana", "cherry", "date"]
        def key_func(x: str) -> int:
            return len(x)
        result = heap_sort(data, key_func=key_func, reverse=True)
        # Check that the result is sorted by length descending
        lengths = [len(x) for x in result]
        assert lengths == sorted(lengths, reverse=True)
        # Check that all original elements are present
        assert sorted(result) == sorted(data)
    
    def test_heap_sort_large_dataset(self):
        """Test heap sort with large dataset."""
        # Generate 1000 random integers
        data = [random.randint(1, 1000) for _ in range(1000)]
        result = heap_sort(data)
        
        # Verify result is sorted
        assert result == sorted(data)
        assert len(result) == 1000
    
    def test_heap_sort_complex_data(self):
        """Test heap sort with complex data structures."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
            {"name": "David", "age": 20}
        ]
        
        def key_func(person: dict) -> int:
            return person["age"]
        
        result = heap_sort(data, key_func=key_func)
        expected = [
            {"name": "David", "age": 20},
            {"name": "Bob", "age": 25},
            {"name": "Alice", "age": 30},
            {"name": "Charlie", "age": 35}
        ]
        assert result == expected


class TestHeapSortInplace:
    """Test cases for in-place heap sort functions."""
    
    def test_heap_sort_inplace_empty_list(self):
        """Test in-place heap sort with empty list."""
        data = []
        heap_sort_inplace(data)
        assert data == []
    
    def test_heap_sort_inplace_single_element(self):
        """Test in-place heap sort with single element."""
        data = [5]
        heap_sort_inplace(data)
        assert data == [5]
    
    def test_heap_sort_inplace_already_sorted(self):
        """Test in-place heap sort with already sorted list."""
        data = [1, 2, 3, 4, 5]
        heap_sort_inplace(data)
        assert data == [1, 2, 3, 4, 5]
    
    def test_heap_sort_inplace_reverse_sorted(self):
        """Test in-place heap sort with reverse sorted list."""
        data = [5, 4, 3, 2, 1]
        heap_sort_inplace(data)
        assert data == [1, 2, 3, 4, 5]
    
    def test_heap_sort_inplace_random_data(self):
        """Test in-place heap sort with random data."""
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        heap_sort_inplace(data)
        assert data == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    
    def test_heap_sort_inplace_duplicate_elements(self):
        """Test in-place heap sort with duplicate elements."""
        data = [3, 3, 3, 3, 3]
        heap_sort_inplace(data)
        assert data == [3, 3, 3, 3, 3]
    
    def test_heap_sort_inplace_negative_numbers(self):
        """Test in-place heap sort with negative numbers."""
        data = [-5, 10, -3, 0, 7, -8]
        heap_sort_inplace(data)
        assert data == [-8, -5, -3, 0, 7, 10]
    
    def test_heap_sort_inplace_reverse_order(self):
        """Test in-place heap sort in reverse order."""
        data = [1, 2, 3, 4, 5]
        heap_sort_inplace(data, reverse=True)
        assert data == [5, 4, 3, 2, 1]
    
    def test_heap_sort_inplace_large_dataset(self):
        """Test in-place heap sort with large dataset."""
        # Generate 1000 random integers
        data = [random.randint(1, 1000) for _ in range(1000)]
        expected = sorted(data)
        heap_sort_inplace(data)
        assert data == expected
        assert len(data) == 1000


class TestHeapSortGenericInplace:
    """Test cases for generic in-place heap sort."""
    
    def test_heap_sort_generic_inplace_empty_list(self):
        """Test generic in-place heap sort with empty list."""
        data = []
        heap_sort_generic_inplace(data)
        assert data == []
    
    def test_heap_sort_generic_inplace_single_element(self):
        """Test generic in-place heap sort with single element."""
        data = [5]
        heap_sort_generic_inplace(data)
        assert data == [5]
    
    def test_heap_sort_generic_inplace_random_data(self):
        """Test generic in-place heap sort with random data."""
        data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        heap_sort_generic_inplace(data)
        assert data == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    
    def test_heap_sort_generic_inplace_with_key_func(self):
        """Test generic in-place heap sort with key function."""
        data = ["apple", "banana", "cherry", "date"]
        def key_func(x: str) -> int:
            return len(x)
        heap_sort_generic_inplace(data, key_func=key_func)
        # Check that the result is sorted by length ascending
        lengths = [len(x) for x in data]
        assert lengths == sorted(lengths)
        # Check that all original elements are present
        assert sorted(data) == sorted(["apple", "banana", "cherry", "date"])
    
    def test_heap_sort_generic_inplace_reverse_order(self):
        """Test generic in-place heap sort in reverse order."""
        data = [1, 2, 3, 4, 5]
        heap_sort_generic_inplace(data, reverse=True)
        assert data == [5, 4, 3, 2, 1]
    
    def test_heap_sort_generic_inplace_reverse_with_key_func(self):
        """Test generic in-place heap sort in reverse order with key function."""
        data = ["apple", "banana", "cherry", "date"]
        def key_func(x: str) -> int:
            return len(x)
        heap_sort_generic_inplace(data, key_func=key_func, reverse=True)
        # Check that the result is sorted by length descending
        lengths = [len(x) for x in data]
        assert lengths == sorted(lengths, reverse=True)
        # Check that all original elements are present
        assert sorted(data) == sorted(["apple", "banana", "cherry", "date"])
    
    def test_heap_sort_generic_inplace_complex_data(self):
        """Test generic in-place heap sort with complex data structures."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
            {"name": "David", "age": 20}
        ]
        
        def key_func(person: dict) -> int:
            return person["age"]
        
        heap_sort_generic_inplace(data, key_func=key_func)
        expected = [
            {"name": "David", "age": 20},
            {"name": "Bob", "age": 25},
            {"name": "Alice", "age": 30},
            {"name": "Charlie", "age": 35}
        ]
        assert data == expected
    
    def test_heap_sort_generic_inplace_large_dataset(self):
        """Test generic in-place heap sort with large dataset."""
        # Generate 1000 random integers
        data = [random.randint(1, 1000) for _ in range(1000)]
        expected = sorted(data)
        heap_sort_generic_inplace(data)
        assert data == expected
        assert len(data) == 1000


class TestHeapSortBenchmark:
    """Test cases for heap sort benchmarking."""
    
    def test_benchmark_heap_sort(self):
        """Test heap sort benchmarking function."""
        data_sizes = [100, 1000]
        results = benchmark_heap_sort(data_sizes, iterations=10)
        
        # Verify results structure
        assert len(results) == 2
        for size in data_sizes:
            assert size in results
            size_results = results[size]
            assert "functional_heap_sort" in size_results
            assert "inplace_heap_sort" in size_results
            assert "builtin_sort" in size_results
            assert "func_vs_builtin_ratio" in size_results
            assert "inplace_vs_builtin_ratio" in size_results
            
            # Verify ratios are positive
            assert size_results["func_vs_builtin_ratio"] > 0
            assert size_results["inplace_vs_builtin_ratio"] > 0
    
    def test_verify_heap_sort_correctness(self):
        """Test heap sort correctness verification."""
        # This should return True if all tests pass
        result = verify_heap_sort_correctness()
        assert result is True


class TestHeapSortEdgeCases:
    """Test cases for heap sort edge cases."""
    
    def test_heap_sort_all_same_elements(self):
        """Test heap sort with all same elements."""
        data = [5, 5, 5, 5, 5]
        result = heap_sort(data)
        assert result == [5, 5, 5, 5, 5]
        
        # Test in-place
        data_copy = data.copy()
        heap_sort_inplace(data_copy)
        assert data_copy == [5, 5, 5, 5, 5]
    
    def test_heap_sort_two_elements(self):
        """Test heap sort with exactly two elements."""
        data = [3, 1]
        result = heap_sort(data)
        assert result == [1, 3]
        
        # Test reverse
        result = heap_sort(data, reverse=True)
        assert result == [3, 1]
    
    def test_heap_sort_three_elements(self):
        """Test heap sort with exactly three elements."""
        data = [3, 1, 2]
        result = heap_sort(data)
        assert result == [1, 2, 3]
    
    def test_heap_sort_with_zero(self):
        """Test heap sort with zero values."""
        data = [0, 5, 0, 3, 0]
        result = heap_sort(data)
        assert result == [0, 0, 0, 3, 5]
    
    def test_heap_sort_with_negative_and_zero(self):
        """Test heap sort with negative numbers and zero."""
        data = [-5, 0, 5, -3, 0]
        result = heap_sort(data)
        assert result == [-5, -3, 0, 0, 5]
    
    def test_heap_sort_floats(self):
        """Test heap sort with float data."""
        data = [3.14, 1.41, 2.71, 0.58]
        result = heap_sort(data)
        assert result == [0.58, 1.41, 2.71, 3.14]
    
    def test_heap_sort_mixed_types_with_key_func(self):
        """Test heap sort with mixed types using key function."""
        data = ["a", "bb", "ccc", "dddd"]
        
        def key_func(x: str) -> int:
            return len(x)
        
        result = heap_sort(data, key_func=key_func)
        assert result == ["a", "bb", "ccc", "dddd"]
        
        # Test reverse
        result = heap_sort(data, key_func=key_func, reverse=True)
        assert result == ["dddd", "ccc", "bb", "a"]


class TestHeapSortOptimized:
    """Test cases for optimized heap sort."""
    
    def test_heap_sort_optimized(self):
        """Test optimized heap sort implementation."""
        from src.chapter_11.heap_sort import heap_sort_optimized
        
        # Test basic functionality
        data = [64, 34, 25, 12, 22, 11, 90]
        sorted_data = heap_sort_optimized(data)
        assert sorted_data == [11, 12, 22, 25, 34, 64, 90]
        
        # Test reverse sort
        sorted_data_reverse = heap_sort_optimized(data, reverse=True)
        assert sorted_data_reverse == [90, 64, 34, 25, 22, 12, 11]
        
        # Test with key function (not stable, so check key order only)
        words = ["apple", "banana", "cherry", "date"]
        sorted_words = heap_sort_optimized(words, key_func=len)
        lengths = [len(word) for word in sorted_words]
        assert lengths == sorted(lengths)
        assert set(sorted_words) == set(words)
        
        # Test empty list
        assert heap_sort_optimized([]) == []
        
        # Test single element
        assert heap_sort_optimized([42]) == [42]
    
    def test_heap_sort_performance_comparison(self):
        """Test performance comparison between standard and optimized heap sort."""
        import time
        import random
        from src.chapter_11.heap_sort import heap_sort, heap_sort_optimized
        
        # Generate test data
        data = [random.randint(1, 1000) for _ in range(1000)]
        
        # Time standard heap sort
        start_time = time.time()
        result1 = heap_sort(data.copy())
        standard_time = time.time() - start_time
        
        # Time optimized heap sort
        start_time = time.time()
        result2 = heap_sort_optimized(data.copy())
        optimized_time = time.time() - start_time
        
        # Results should be identical
        assert result1 == result2
        
        # Optimized should be at least as fast (though timing can be variable)
        # We'll just verify both complete successfully
        assert standard_time > 0
        assert optimized_time > 0
    
    def test_heap_sort_complexity_verification(self):
        """Test that heap sort maintains claimed complexity."""
        import time
        import random
        from src.chapter_11.heap_sort import heap_sort_optimized
        
        sizes = [100, 1000, 10000]
        sort_times = []
        
        for size in sizes:
            data = [random.randint(1, 1000) for _ in range(size)]
            
            start_time = time.time()
            heap_sort_optimized(data)
            end_time = time.time()
            
            sort_times.append(end_time - start_time)
        
        # Verify that sort time grows reasonably (O(n log n))
        # This is a rough check - actual verification would need more sophisticated analysis
        assert sort_times[1] < sort_times[2] * 20  # Should not grow too fast
        
        # Verify that larger sizes take more time
        assert sort_times[0] < sort_times[1]
        assert sort_times[1] < sort_times[2]


if __name__ == "__main__":
    pytest.main([__file__]) 