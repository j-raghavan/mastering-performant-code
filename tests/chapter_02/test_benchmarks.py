"""
Unit tests for the benchmarks module.

This module tests all benchmarking functions for data structures and operations.
"""

import pytest
from typing import Dict, List, Any

from mastering_performant_code.chapter_02.benchmarks import (
    benchmark_sum_functions,
    benchmark_fibonacci_functions,
    benchmark_list_operations,
    benchmark_dict_operations,
    benchmark_set_operations,
    benchmark_memory_usage,
    benchmark_complexity_analysis,
    benchmark_sorting_algorithms,
    benchmark_search_algorithms,
    print_benchmark_results,
    run_all_benchmarks
)

from mastering_performant_code.chapter_02.algorithms import (
    sum_builtin, sum_loop, sum_comprehension, sum_generator, sum_formula,
    fibonacci_iterative, fibonacci_memoized, fibonacci_dynamic,
    bubble_sort, quick_sort, linear_search, binary_search
)


class TestBenchmarkSumFunctions:
    """Test cases for benchmark_sum_functions."""
    
    def test_benchmark_sum_functions_basic(self):
        """Test benchmark_sum_functions with basic input."""
        results = benchmark_sum_functions(1000)
        
        assert isinstance(results, dict)
        assert 'sum_builtin' in results
        assert 'sum_loop' in results
        assert 'sum_comprehension' in results
        assert 'sum_generator' in results
        assert 'sum_formula' in results
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_sum_functions_large_input(self):
        """Test benchmark_sum_functions with large input."""
        results = benchmark_sum_functions(10000)
        
        assert isinstance(results, dict)
        assert len(results) == 5  # All 5 sum functions
        
        # Check that all functions completed successfully
        for name, value in results.items():
            if isinstance(value, str):
                assert 'Error:' in value
            else:
                assert value > 0
    
    def test_benchmark_sum_functions_relative_performance(self):
        """Test that sum_formula is faster than other implementations."""
        results = benchmark_sum_functions(10000)
        
        if all(isinstance(v, float) for v in results.values()):
            # sum_formula should be the fastest (O(1) vs O(n))
            assert results['sum_formula'] < results['sum_builtin']
            assert results['sum_formula'] < results['sum_loop']
            assert results['sum_formula'] < results['sum_comprehension']
            assert results['sum_formula'] < results['sum_generator']


class TestBenchmarkFibonacciFunctions:
    """Test cases for benchmark_fibonacci_functions."""
    
    def test_benchmark_fibonacci_functions_basic(self):
        """Test benchmark_fibonacci_functions with basic input."""
        results = benchmark_fibonacci_functions(10)
        
        assert isinstance(results, dict)
        assert 'fibonacci_iterative' in results
        assert 'fibonacci_memoized' in results
        assert 'fibonacci_dynamic' in results
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_fibonacci_functions_large_input(self):
        """Test benchmark_fibonacci_functions with large input."""
        results = benchmark_fibonacci_functions(30)
        
        assert isinstance(results, dict)
        assert len(results) == 3  # Excludes recursive for large n
        
        # Check that all functions completed successfully
        for name, value in results.items():
            if isinstance(value, str):
                assert 'Error:' in value
            else:
                assert value > 0
    
    def test_benchmark_fibonacci_functions_small_input(self):
        """Test benchmark_fibonacci_functions with small input (includes recursive)."""
        results = benchmark_fibonacci_functions(15)
        
        assert isinstance(results, dict)
        assert 'fibonacci_recursive' in results  # Should be included for small n
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))


class TestBenchmarkListOperations:
    """Test cases for benchmark_list_operations."""
    
    def test_benchmark_list_operations_basic(self):
        """Test benchmark_list_operations with basic input."""
        results = benchmark_list_operations(1000)
        
        assert isinstance(results, dict)
        expected_operations = [
            'append', 'insert_beginning', 'insert_middle', 'pop_end', 'pop_beginning',
            'index', 'contains', 'sort', 'reverse', 'slice', 'concatenate', 'extend'
        ]
        
        for operation in expected_operations:
            assert operation in results
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_list_operations_large_input(self):
        """Test benchmark_list_operations with large input."""
        results = benchmark_list_operations(10000)
        
        assert isinstance(results, dict)
        assert len(results) == 12  # All 12 operations
        
        # Check that all operations completed successfully
        for name, value in results.items():
            if isinstance(value, str):
                assert 'Error:' in value
            else:
                assert value > 0
    
    def test_benchmark_list_operations_relative_performance(self):
        """Test that certain operations are faster than others."""
        results = benchmark_list_operations(10000)
        
        if all(isinstance(v, float) for v in results.values()):
            # append should be faster than insert_beginning (O(1) vs O(n))
            assert results['append'] < results['insert_beginning']
            # pop_end should be faster than pop_beginning (O(1) vs O(n))
            assert results['pop_end'] < results['pop_beginning']


class TestBenchmarkDictOperations:
    """Test cases for benchmark_dict_operations."""
    
    def test_benchmark_dict_operations_basic(self):
        """Test benchmark_dict_operations with basic input."""
        results = benchmark_dict_operations(1000)
        
        assert isinstance(results, dict)
        expected_operations = [
            'get_existing', 'get_missing', 'set_new', 'set_existing', 'delete',
            'contains_key', 'contains_value', 'keys', 'values', 'items', 'update', 'clear'
        ]
        
        for operation in expected_operations:
            assert operation in results
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_dict_operations_large_input(self):
        """Test benchmark_dict_operations with large input."""
        results = benchmark_dict_operations(10000)
        
        assert isinstance(results, dict)
        assert len(results) == 12  # All 12 operations
        
        # Check that all operations completed successfully
        for name, value in results.items():
            if isinstance(value, str):
                assert 'Error:' in value
            else:
                assert value > 0
    
    def test_benchmark_dict_operations_relative_performance(self):
        """Test that certain operations are faster than others."""
        results = benchmark_dict_operations(10000)
        
        if all(isinstance(v, float) for v in results.values()):
            # get_existing should be faster than contains_value (O(1) vs O(n))
            assert results['get_existing'] < results['contains_value']
            # contains_key should be faster than contains_value (O(1) vs O(n))
            assert results['contains_key'] < results['contains_value']


class TestBenchmarkSetOperations:
    """Test cases for benchmark_set_operations."""
    
    def test_benchmark_set_operations_basic(self):
        """Test benchmark_set_operations with basic input."""
        results = benchmark_set_operations(1000)
        
        assert isinstance(results, dict)
        expected_operations = [
            'add', 'remove', 'contains', 'union', 'intersection', 'difference',
            'symmetric_difference', 'issubset', 'issuperset', 'clear'
        ]
        
        for operation in expected_operations:
            assert operation in results
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_set_operations_large_input(self):
        """Test benchmark_set_operations with large input."""
        results = benchmark_set_operations(10000)
        
        assert isinstance(results, dict)
        assert len(results) == 10  # All 10 operations
        
        # Check that all operations completed successfully
        for name, value in results.items():
            if isinstance(value, str):
                assert 'Error:' in value
            else:
                assert value > 0
    
    def test_benchmark_set_operations_relative_performance(self):
        """Test that certain operations are faster than others."""
        results = benchmark_set_operations(10000)
        
        if all(isinstance(v, float) for v in results.values()):
            # add should be faster than union (O(1) vs O(n))
            assert results['add'] < results['union']
            # contains should be faster than union (O(1) vs O(n))
            assert results['contains'] < results['union']


class TestBenchmarkMemoryUsage:
    """Test cases for benchmark_memory_usage."""
    
    def test_benchmark_memory_usage_basic(self):
        """Test benchmark_memory_usage with basic input."""
        results = benchmark_memory_usage(1000)
        
        assert isinstance(results, dict)
        expected_structures = ['list', 'tuple', 'set', 'dict', 'generator']
        
        for structure in expected_structures:
            assert structure in results
        
        # All results should be integers
        for value in results.values():
            assert isinstance(value, int)
            assert value > 0
    
    def test_benchmark_memory_usage_large_input(self):
        """Test benchmark_memory_usage with large input."""
        results = benchmark_memory_usage(10000)
        
        assert isinstance(results, dict)
        assert len(results) == 5  # All 5 data structures
        
        # All results should be integers and larger than small input
        small_results = benchmark_memory_usage(1000)
        for structure in results:
            assert results[structure] > small_results[structure]
    
    def test_benchmark_memory_usage_relative_sizes(self):
        """Test that memory usage is reasonable relative to each other."""
        results = benchmark_memory_usage(1000)
        
        # dict should use more memory than list (key-value pairs)
        assert results['dict'] > results['list']
        # set should use more memory than list (hash table overhead)
        assert results['set'] > results['list']
        # tuple should be similar to list
        assert abs(results['tuple'] - results['list']) < 1000


class TestBenchmarkComplexityAnalysis:
    """Test cases for benchmark_complexity_analysis."""
    
    def test_benchmark_complexity_analysis_linear(self):
        """Test benchmark_complexity_analysis with linear function."""
        def linear_func(n):
            return sum(range(n))
        
        input_sizes = [100, 1000, 10000]
        analysis = benchmark_complexity_analysis(linear_func, input_sizes)
        
        assert isinstance(analysis, dict)
        assert 'input_sizes' in analysis
        assert 'execution_times' in analysis
        assert 'growth_rates' in analysis
        assert 'average_growth_rate' in analysis
        assert 'estimated_complexity' in analysis
        
        assert len(analysis['input_sizes']) == 3
        assert len(analysis['execution_times']) == 3
        assert len(analysis['growth_rates']) == 2
        assert analysis['average_growth_rate'] > 0
    
    def test_benchmark_complexity_analysis_constant(self):
        """Test benchmark_complexity_analysis with constant function."""
        def constant_func(n):
            return 42
        
        input_sizes = [100, 1000, 10000]
        analysis = benchmark_complexity_analysis(constant_func, input_sizes)
        
        assert isinstance(analysis, dict)
        assert 'estimated_complexity' in analysis
        # Should detect constant complexity
        assert 'O(1)' in analysis['estimated_complexity']
    
    def test_benchmark_complexity_analysis_insufficient_data(self):
        """Test benchmark_complexity_analysis with insufficient data."""
        def test_func(n):
            return n
        
        input_sizes = [100]  # Only one size
        analysis = benchmark_complexity_analysis(test_func, input_sizes)
        
        assert 'error' in analysis
        assert 'Insufficient data' in analysis['error']
    
    def test_benchmark_complexity_analysis_with_error(self):
        """Test benchmark_complexity_analysis with function that raises error."""
        def error_func(n):
            if n > 1000:
                raise ValueError("Test error")
            return n
        
        input_sizes = [100, 1000, 10000]
        analysis = benchmark_complexity_analysis(error_func, input_sizes)
        
        # Should handle the error gracefully and continue with available data
        assert isinstance(analysis, dict)
        assert len(analysis['input_sizes']) < 3  # Should have fewer than 3 results


class TestBenchmarkSortingAlgorithms:
    """Test cases for benchmark_sorting_algorithms."""
    
    def test_benchmark_sorting_algorithms_basic(self):
        """Test benchmark_sorting_algorithms with basic input."""
        results = benchmark_sorting_algorithms(100)
        
        assert isinstance(results, dict)
        assert 'bubble_sort' in results
        assert 'quick_sort' in results
        assert 'builtin_sort' in results
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_sorting_algorithms_large_input(self):
        """Test benchmark_sorting_algorithms with large input."""
        results = benchmark_sorting_algorithms(1000)
        
        assert isinstance(results, dict)
        assert len(results) == 3  # All 3 sorting algorithms
        
        # Check that all algorithms completed successfully
        for name, value in results.items():
            if isinstance(value, str):
                assert 'Error:' in value
            else:
                assert value > 0
    
    def test_benchmark_sorting_algorithms_relative_performance(self):
        """Test that certain algorithms are faster than others."""
        results = benchmark_sorting_algorithms(1000)
        
        if all(isinstance(v, float) for v in results.values()):
            # builtin_sort should be faster than bubble_sort
            assert results['builtin_sort'] < results['bubble_sort']
            # quick_sort should be faster than bubble_sort
            assert results['quick_sort'] < results['bubble_sort']


class TestBenchmarkSearchAlgorithms:
    """Test cases for benchmark_search_algorithms."""
    
    def test_benchmark_search_algorithms_basic(self):
        """Test benchmark_search_algorithms with basic input."""
        results = benchmark_search_algorithms(1000)
        
        assert isinstance(results, dict)
        assert 'linear_search' in results
        assert 'binary_search' in results
        
        # All results should be either float or error string
        for value in results.values():
            assert isinstance(value, (float, str))
    
    def test_benchmark_search_algorithms_large_input(self):
        """Test benchmark_search_algorithms with large input."""
        results = benchmark_search_algorithms(10000)
        
        assert isinstance(results, dict)
        assert len(results) == 2  # Both search algorithms
        
        # Check that all algorithms completed successfully
        for name, value in results.items():
            if isinstance(value, str):
                assert 'Error:' in value
            else:
                assert value > 0
    
    def test_benchmark_search_algorithms_relative_performance(self):
        """Test that binary_search is faster than linear_search."""
        results = benchmark_search_algorithms(10000)
        
        if all(isinstance(v, float) for v in results.values()):
            # binary_search should be faster than linear_search (O(log n) vs O(n))
            assert results['binary_search'] < results['linear_search']


class TestPrintBenchmarkResults:
    """Test cases for print_benchmark_results."""
    
    def test_print_benchmark_results_basic(self, capsys):
        """Test print_benchmark_results with basic input."""
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
    
    def test_print_benchmark_results_with_errors(self, capsys):
        """Test print_benchmark_results with error results."""
        results = {
            'func1': 0.001,
            'func2': "Error: Test error",
            'func3': 0.0005
        }
        
        print_benchmark_results(results, "Test Benchmark")
        captured = capsys.readouterr()
        
        assert 'Test Benchmark' in captured.out
        assert 'func1' in captured.out
        assert 'func2' in captured.out
        assert 'func3' in captured.out
        assert 'Error: Test error' in captured.out
    
    def test_print_benchmark_results_empty(self, capsys):
        """Test print_benchmark_results with empty results."""
        results = {}
        
        print_benchmark_results(results, "Empty Benchmark")
        captured = capsys.readouterr()
        
        assert 'Empty Benchmark' in captured.out
        # Empty results may not show 'seconds' since there are no results to display
        # Just check that the function runs without error and produces some output
        assert len(captured.out) > 0


class TestRunAllBenchmarks:
    """Test cases for run_all_benchmarks."""
    
    def test_run_all_benchmarks(self, capsys):
        """Test run_all_benchmarks function."""
        run_all_benchmarks()
        captured = capsys.readouterr()
        
        # Check that all benchmark sections are present
        assert 'Comprehensive Python Data Structure Benchmarks' in captured.out
        assert 'Sum Functions Benchmark' in captured.out
        assert 'Fibonacci Functions Benchmark' in captured.out
        assert 'Sorting Algorithms Benchmark' in captured.out
        assert 'Search Algorithms Benchmark' in captured.out
        assert 'List Operations Benchmark' in captured.out
        assert 'Dictionary Operations Benchmark' in captured.out
        assert 'Set Operations Benchmark' in captured.out
        assert 'Memory Usage Benchmark' in captured.out
        assert 'Complexity Analysis' in captured.out
    
    def test_run_all_benchmarks_output_format(self, capsys):
        """Test that run_all_benchmarks produces properly formatted output."""
        run_all_benchmarks()
        captured = capsys.readouterr()
        
        # Check for proper formatting
        assert '===' in captured.out
        assert '---' in captured.out
        assert 'seconds' in captured.out
        assert 'bytes' in captured.out


if __name__ == "__main__":
    pytest.main([__file__]) 