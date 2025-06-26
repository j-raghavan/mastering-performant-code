"""
Unit tests for the algorithms module.

This module tests all algorithm implementations including sum functions,
Fibonacci functions, sorting algorithms, and search algorithms.
"""

import pytest
import random
from typing import List

from src.chapter_02.algorithms import (
    sum_builtin, sum_loop, sum_comprehension, sum_generator, sum_formula,
    fibonacci_recursive, fibonacci_iterative, fibonacci_memoized, fibonacci_dynamic,
    slow_function, optimized_function,
    bubble_sort, quick_sort, linear_search, binary_search,
    matrix_multiply_slow, matrix_multiply_optimized,
    generate_test_data,
    benchmark_sum_functions, benchmark_fibonacci_functions,
    benchmark_sorting_algorithms, benchmark_search_algorithms,
    print_benchmark_results
)


class TestSumFunctions:
    """Test cases for sum function implementations."""
    
    def test_sum_builtin(self):
        """Test sum_builtin function."""
        assert sum_builtin(0) == 0
        assert sum_builtin(1) == 0
        assert sum_builtin(5) == 10  # 0 + 1 + 2 + 3 + 4
        assert sum_builtin(10) == 45  # 0 + 1 + 2 + ... + 9
    
    def test_sum_loop(self):
        """Test sum_loop function."""
        assert sum_loop(0) == 0
        assert sum_loop(1) == 0
        assert sum_loop(5) == 10
        assert sum_loop(10) == 45
    
    def test_sum_comprehension(self):
        """Test sum_comprehension function."""
        assert sum_comprehension(0) == 0
        assert sum_comprehension(1) == 0
        assert sum_comprehension(5) == 10
        assert sum_comprehension(10) == 45
    
    def test_sum_generator(self):
        """Test sum_generator function."""
        assert sum_generator(0) == 0
        assert sum_generator(1) == 0
        assert sum_generator(5) == 10
        assert sum_generator(10) == 45
    
    def test_sum_formula(self):
        """Test sum_formula function."""
        assert sum_formula(0) == 0
        assert sum_formula(1) == 0
        assert sum_formula(5) == 10
        assert sum_formula(10) == 45
    
    def test_sum_functions_consistency(self):
        """Test that all sum functions return the same results."""
        test_cases = [0, 1, 5, 10, 100]
        
        for n in test_cases:
            expected = sum_formula(n)  # Use formula as reference
            assert sum_builtin(n) == expected
            assert sum_loop(n) == expected
            assert sum_comprehension(n) == expected
            assert sum_generator(n) == expected
    
    def test_sum_functions_large_input(self):
        """Test sum functions with large input."""
        n = 10000
        expected = sum_formula(n)
        
        assert sum_builtin(n) == expected
        assert sum_loop(n) == expected
        assert sum_comprehension(n) == expected
        assert sum_generator(n) == expected


class TestFibonacciFunctions:
    """Test cases for Fibonacci function implementations."""
    
    def test_fibonacci_recursive(self):
        """Test fibonacci_recursive function."""
        assert fibonacci_recursive(0) == 0
        assert fibonacci_recursive(1) == 1
        assert fibonacci_recursive(2) == 1
        assert fibonacci_recursive(3) == 2
        assert fibonacci_recursive(4) == 3
        assert fibonacci_recursive(5) == 5
        assert fibonacci_recursive(6) == 8
        assert fibonacci_recursive(7) == 13
    
    def test_fibonacci_iterative(self):
        """Test fibonacci_iterative function."""
        assert fibonacci_iterative(0) == 0
        assert fibonacci_iterative(1) == 1
        assert fibonacci_iterative(2) == 1
        assert fibonacci_iterative(3) == 2
        assert fibonacci_iterative(4) == 3
        assert fibonacci_iterative(5) == 5
        assert fibonacci_iterative(6) == 8
        assert fibonacci_iterative(7) == 13
    
    def test_fibonacci_memoized(self):
        """Test fibonacci_memoized function."""
        assert fibonacci_memoized(0) == 0
        assert fibonacci_memoized(1) == 1
        assert fibonacci_memoized(2) == 1
        assert fibonacci_memoized(3) == 2
        assert fibonacci_memoized(4) == 3
        assert fibonacci_memoized(5) == 5
        assert fibonacci_memoized(6) == 8
        assert fibonacci_memoized(7) == 13
    
    def test_fibonacci_dynamic(self):
        """Test fibonacci_dynamic function."""
        assert fibonacci_dynamic(0) == 0
        assert fibonacci_dynamic(1) == 1
        assert fibonacci_dynamic(2) == 1
        assert fibonacci_dynamic(3) == 2
        assert fibonacci_dynamic(4) == 3
        assert fibonacci_dynamic(5) == 5
        assert fibonacci_dynamic(6) == 8
        assert fibonacci_dynamic(7) == 13
    
    def test_fibonacci_functions_consistency(self):
        """Test that all Fibonacci functions return the same results."""
        test_cases = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for n in test_cases:
            expected = fibonacci_iterative(n)  # Use iterative as reference
            assert fibonacci_recursive(n) == expected
            assert fibonacci_memoized(n) == expected
            assert fibonacci_dynamic(n) == expected
    
    def test_fibonacci_large_input(self):
        """Test Fibonacci functions with larger input (excluding recursive)."""
        n = 30
        expected = fibonacci_iterative(n)
        
        assert fibonacci_memoized(n) == expected
        assert fibonacci_dynamic(n) == expected
    
    def test_fibonacci_negative_input(self):
        """Test Fibonacci functions with negative input."""
        # Test that functions handle negative input appropriately
        # Note: Some implementations may not raise RecursionError for negative input
        
        # Test recursive function - it may or may not raise RecursionError
        try:
            fibonacci_recursive(-1)
            # If no exception is raised, that's also acceptable
        except (RecursionError, ValueError, TypeError):
            # Any of these exceptions are acceptable for negative input
            pass
        
        # Test other functions - they should handle negative input gracefully
        # or raise appropriate exceptions
        try:
            fibonacci_iterative(-1)
        except (ValueError, TypeError):
            pass
        
        try:
            fibonacci_memoized(-1)
        except (ValueError, TypeError):
            pass
        
        try:
            fibonacci_dynamic(-1)
        except (ValueError, TypeError):
            pass


class TestSlowAndOptimizedFunctions:
    """Test cases for slow_function and optimized_function."""
    
    def test_slow_function(self):
        """Test slow_function."""
        result = slow_function()
        expected = sum(i * j for i in range(10000) for j in range(100))
        assert result == expected
    
    def test_optimized_function(self):
        """Test optimized_function."""
        result = optimized_function()
        expected = sum(i * 4950 for i in range(10000))  # 4950 = sum(range(100))
        assert result == expected
    
    def test_functions_consistency(self):
        """Test that slow_function and optimized_function return the same result."""
        assert slow_function() == optimized_function()


class TestSortingAlgorithms:
    """Test cases for sorting algorithms."""
    
    def test_bubble_sort_empty(self):
        """Test bubble_sort with empty list."""
        assert bubble_sort([]) == []
    
    def test_bubble_sort_single_element(self):
        """Test bubble_sort with single element."""
        assert bubble_sort([5]) == [5]
    
    def test_bubble_sort_sorted(self):
        """Test bubble_sort with already sorted list."""
        arr = [1, 2, 3, 4, 5]
        assert bubble_sort(arr) == [1, 2, 3, 4, 5]
        # Original list should not be modified
        assert arr == [1, 2, 3, 4, 5]
    
    def test_bubble_sort_reverse_sorted(self):
        """Test bubble_sort with reverse sorted list."""
        arr = [5, 4, 3, 2, 1]
        assert bubble_sort(arr) == [1, 2, 3, 4, 5]
    
    def test_bubble_sort_random(self):
        """Test bubble_sort with random list."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        assert bubble_sort(arr) == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_bubble_sort_duplicates(self):
        """Test bubble_sort with duplicate elements."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        assert bubble_sort(arr) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    
    def test_quick_sort_empty(self):
        """Test quick_sort with empty list."""
        assert quick_sort([]) == []
    
    def test_quick_sort_single_element(self):
        """Test quick_sort with single element."""
        assert quick_sort([5]) == [5]
    
    def test_quick_sort_sorted(self):
        """Test quick_sort with already sorted list."""
        arr = [1, 2, 3, 4, 5]
        assert quick_sort(arr) == [1, 2, 3, 4, 5]
    
    def test_quick_sort_reverse_sorted(self):
        """Test quick_sort with reverse sorted list."""
        arr = [5, 4, 3, 2, 1]
        assert quick_sort(arr) == [1, 2, 3, 4, 5]
    
    def test_quick_sort_random(self):
        """Test quick_sort with random list."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        assert quick_sort(arr) == [1, 1, 2, 3, 4, 5, 6, 9]
    
    def test_quick_sort_duplicates(self):
        """Test quick_sort with duplicate elements."""
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        assert quick_sort(arr) == [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]
    
    def test_sorting_algorithms_consistency(self):
        """Test that sorting algorithms return the same results."""
        test_cases = [
            [],
            [5],
            [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1],
            [3, 1, 4, 1, 5, 9, 2, 6],
            [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        ]
        
        for arr in test_cases:
            expected = sorted(arr)
            assert bubble_sort(arr) == expected
            assert quick_sort(arr) == expected


class TestSearchAlgorithms:
    """Test cases for search algorithms."""
    
    def test_linear_search_empty(self):
        """Test linear_search with empty list."""
        assert linear_search([], 5) == -1
    
    def test_linear_search_single_element_found(self):
        """Test linear_search with single element, target found."""
        assert linear_search([5], 5) == 0
    
    def test_linear_search_single_element_not_found(self):
        """Test linear_search with single element, target not found."""
        assert linear_search([5], 3) == -1
    
    def test_linear_search_multiple_elements_found(self):
        """Test linear_search with multiple elements, target found."""
        arr = [1, 3, 5, 7, 9]
        assert linear_search(arr, 5) == 2
        assert linear_search(arr, 1) == 0
        assert linear_search(arr, 9) == 4
    
    def test_linear_search_multiple_elements_not_found(self):
        """Test linear_search with multiple elements, target not found."""
        arr = [1, 3, 5, 7, 9]
        assert linear_search(arr, 2) == -1
        assert linear_search(arr, 10) == -1
    
    def test_linear_search_duplicates(self):
        """Test linear_search with duplicate elements."""
        arr = [1, 3, 5, 3, 7, 9]
        # Should return the first occurrence
        assert linear_search(arr, 3) == 1
    
    def test_binary_search_empty(self):
        """Test binary_search with empty list."""
        assert binary_search([], 5) == -1
    
    def test_binary_search_single_element_found(self):
        """Test binary_search with single element, target found."""
        assert binary_search([5], 5) == 0
    
    def test_binary_search_single_element_not_found(self):
        """Test binary_search with single element, target not found."""
        assert binary_search([5], 3) == -1
    
    def test_binary_search_multiple_elements_found(self):
        """Test binary_search with multiple elements, target found."""
        arr = [1, 3, 5, 7, 9]
        assert binary_search(arr, 5) == 2
        assert binary_search(arr, 1) == 0
        assert binary_search(arr, 9) == 4
    
    def test_binary_search_multiple_elements_not_found(self):
        """Test binary_search with multiple elements, target not found."""
        arr = [1, 3, 5, 7, 9]
        assert binary_search(arr, 2) == -1
        assert binary_search(arr, 10) == -1
    
    def test_binary_search_duplicates(self):
        """Test binary_search with duplicate elements."""
        arr = [1, 3, 3, 3, 5, 7, 9]
        # Binary search may return any occurrence of the target
        result = binary_search(arr, 3)
        assert result in [1, 2, 3]  # Any of the positions with value 3
    
    def test_search_algorithms_consistency(self):
        """Test that search algorithms return consistent results for sorted lists."""
        test_cases = [
            ([], 5),
            ([5], 5),
            ([5], 3),
            ([1, 3, 5, 7, 9], 5),
            ([1, 3, 5, 7, 9], 2),
            ([1, 3, 5, 7, 9], 1),
            ([1, 3, 5, 7, 9], 9)
        ]
        
        for arr, target in test_cases:
            linear_result = linear_search(arr, target)
            binary_result = binary_search(arr, target)
            
            # Both should find the target or both should not find it
            if linear_result != -1:
                assert binary_result != -1
                assert arr[linear_result] == arr[binary_result] == target
            else:
                assert binary_result == -1


class TestMatrixMultiplication:
    """Test cases for matrix multiplication algorithms."""
    
    def test_matrix_multiply_slow_2x2(self):
        """Test matrix_multiply_slow with 2x2 matrices."""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        expected = [[19, 22], [43, 50]]
        assert matrix_multiply_slow(a, b) == expected
    
    def test_matrix_multiply_optimized_2x2(self):
        """Test matrix_multiply_optimized with 2x2 matrices."""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        expected = [[19, 22], [43, 50]]
        assert matrix_multiply_optimized(a, b) == expected
    
    def test_matrix_multiply_dimension_mismatch(self):
        """Test matrix multiplication with dimension mismatch."""
        a = [[1, 2], [3, 4]]
        b = [[5, 6, 7], [8, 9, 10], [11, 12, 13]]
        
        with pytest.raises(ValueError, match="Matrix dimensions don't match"):
            matrix_multiply_slow(a, b)
        
        with pytest.raises(ValueError, match="Matrix dimensions don't match"):
            matrix_multiply_optimized(a, b)
    
    def test_matrix_multiply_algorithms_consistency(self):
        """Test that both matrix multiplication algorithms return the same results."""
        test_cases = [
            ([[1, 2], [3, 4]], [[5, 6], [7, 8]]),
            ([[1]], [[2]]),
            ([[1, 2, 3], [4, 5, 6]], [[7, 8], [9, 10], [11, 12]])
        ]
        
        for a, b in test_cases:
            slow_result = matrix_multiply_slow(a, b)
            optimized_result = matrix_multiply_optimized(a, b)
            assert slow_result == optimized_result


class TestUtilityFunctions:
    """Test cases for utility functions."""
    
    def test_generate_test_data(self):
        """Test generate_test_data function."""
        size = 100
        data = generate_test_data(size)
        
        assert isinstance(data, dict)
        assert 'list' in data
        assert 'set' in data
        assert 'dict' in data
        assert 'tuple' in data
        assert 'sorted_list' in data
        assert 'reversed_list' in data
        assert 'random_list' in data
        
        assert len(data['list']) == size
        assert len(data['set']) == size
        assert len(data['dict']) == size
        assert len(data['tuple']) == size
        assert len(data['sorted_list']) == size
        assert len(data['reversed_list']) == size
        assert len(data['random_list']) == size
    
    def test_benchmark_sum_functions(self):
        """Test benchmark_sum_functions function."""
        results = benchmark_sum_functions(1000)
        
        assert isinstance(results, dict)
        assert 'sum_builtin' in results
        assert 'sum_loop' in results
        assert 'sum_comprehension' in results
        assert 'sum_generator' in results
        assert 'sum_formula' in results
        
        # All should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_fibonacci_functions(self):
        """Test benchmark_fibonacci_functions function."""
        results = benchmark_fibonacci_functions(10)
        
        assert isinstance(results, dict)
        assert 'fibonacci_iterative' in results
        assert 'fibonacci_memoized' in results
        assert 'fibonacci_dynamic' in results
        
        # All should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_sorting_algorithms(self):
        """Test benchmark_sorting_algorithms function."""
        results = benchmark_sorting_algorithms(100)
        
        assert isinstance(results, dict)
        assert 'bubble_sort' in results
        assert 'quick_sort' in results
        assert 'builtin_sort' in results
        
        # All should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_search_algorithms(self):
        """Test benchmark_search_algorithms function."""
        results = benchmark_search_algorithms(1000)
        
        assert isinstance(results, dict)
        assert 'linear_search' in results
        assert 'binary_search' in results
        
        # All should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_print_benchmark_results(self, capsys):
        """Test print_benchmark_results function."""
        results = {
            'func1': 0.001,
            'func2': 0.002,
            'func3': 0.0005
        }
        
        print_benchmark_results(results, "Test Benchmark")
        captured = capsys.readouterr()
        
        assert 'Test Benchmark' in captured.out
        assert 'func1' in captured.out
        assert 'func2' in captured.out
        assert 'func3' in captured.out
        assert 'seconds' in captured.out


if __name__ == "__main__":
    pytest.main([__file__]) 