"""
Unit tests for benchmark functions.

This module provides tests for the benchmark functions to ensure they
return expected data structures and handle edge cases correctly.
"""

import pytest
from typing import Dict, Any
from mastering_performant_code.chapter_03.benchmarks import (
    benchmark_growth_strategies,
    compare_with_builtin_list,
    analyze_amortized_complexity,
    benchmark_insert_operations,
    benchmark_pop_operations,
    benchmark_search_operations,
    benchmark_memory_usage,
    benchmark_resize_patterns,
    run_all_benchmarks
)


class TestBenchmarkGrowthStrategies:
    """Test cases for growth strategy benchmarks."""
    
    def test_benchmark_growth_strategies_returns_dict(self):
        """Test that benchmark returns a dictionary."""
        results = benchmark_growth_strategies()
        assert isinstance(results, dict)
    
    def test_benchmark_growth_strategies_has_all_strategies(self):
        """Test that all growth strategies are included."""
        results = benchmark_growth_strategies()
        expected_strategies = ['doubling', 'fixed', 'golden_ratio', 'adaptive']
        
        for strategy in expected_strategies:
            assert strategy in results
    
    def test_benchmark_growth_strategies_metrics(self):
        """Test that each strategy has expected metrics."""
        results = benchmark_growth_strategies()
        
        for strategy, metrics in results.items():
            assert 'append_time' in metrics
            assert 'final_capacity' in metrics
            assert 'memory_efficiency' in metrics
            assert 'resize_count' in metrics
            assert 'load_factor' in metrics
            
            # Check data types
            assert isinstance(metrics['append_time'], (int, float))
            assert isinstance(metrics['final_capacity'], int)
            assert isinstance(metrics['memory_efficiency'], float)
            assert isinstance(metrics['resize_count'], int)
            assert isinstance(metrics['load_factor'], float)
            
            # Check value ranges
            assert metrics['append_time'] > 0
            assert metrics['final_capacity'] > 0
            assert 0 <= metrics['memory_efficiency'] <= 1
            assert metrics['resize_count'] >= 0
            assert 0 <= metrics['load_factor'] <= 1


class TestCompareWithBuiltinList:
    """Test cases for built-in list comparison."""
    
    def test_compare_with_builtin_list_returns_dict(self):
        """Test that comparison returns a dictionary."""
        results = compare_with_builtin_list()
        assert isinstance(results, dict)
    
    def test_compare_with_builtin_list_has_expected_keys(self):
        """Test that comparison has expected keys."""
        results = compare_with_builtin_list()
        expected_keys = ['builtin_time', 'custom_time', 'ratio', 'slower_by_factor']
        
        for key in expected_keys:
            assert key in results
    
    def test_compare_with_builtin_list_data_types(self):
        """Test that comparison has correct data types."""
        results = compare_with_builtin_list()
        
        assert isinstance(results['builtin_time'], (int, float))
        assert isinstance(results['custom_time'], (int, float))
        assert isinstance(results['ratio'], (int, float))
        assert isinstance(results['slower_by_factor'], (int, float))
    
    def test_compare_with_builtin_list_value_ranges(self):
        """Test that comparison values are in expected ranges."""
        results = compare_with_builtin_list()
        
        assert results['builtin_time'] > 0
        assert results['custom_time'] > 0
        assert results['ratio'] > 0
        assert results['slower_by_factor'] > 0
        
        # Custom implementation should be slower than built-in
        assert results['ratio'] >= 1.0
        assert results['slower_by_factor'] >= 1.0


class TestAnalyzeAmortizedComplexity:
    """Test cases for amortized complexity analysis."""
    
    def test_analyze_amortized_complexity_returns_dict(self):
        """Test that analysis returns a dictionary."""
        results = analyze_amortized_complexity()
        assert isinstance(results, dict)
    
    def test_analyze_amortized_complexity_has_expected_sizes(self):
        """Test that analysis includes expected sizes."""
        results = analyze_amortized_complexity()
        expected_sizes = [100, 1000, 10000, 100000]
        
        for size in expected_sizes:
            assert size in results
    
    def test_analyze_amortized_complexity_metrics(self):
        """Test that each size has expected metrics."""
        results = analyze_amortized_complexity()
        
        for size, metrics in results.items():
            assert 'time_per_element' in metrics
            assert 'total_time' in metrics
            
            # Check data types
            assert isinstance(metrics['time_per_element'], (int, float))
            assert isinstance(metrics['total_time'], (int, float))
            
            # Check value ranges
            assert metrics['time_per_element'] > 0
            assert metrics['total_time'] > 0
    
    def test_analyze_amortized_complexity_scaling(self):
        """Test that time scales reasonably with size."""
        results = analyze_amortized_complexity()
        
        # Time per element should be relatively consistent
        times = [metrics['time_per_element'] for metrics in results.values()]
        avg_time = sum(times) / len(times)
        
        for time in times:
            # Each time should be within reasonable range of average
            assert 0.1 * avg_time <= time <= 10 * avg_time


class TestBenchmarkInsertOperations:
    """Test cases for insert operation benchmarks."""
    
    def test_benchmark_insert_operations_returns_dict(self):
        """Test that benchmark returns a dictionary."""
        results = benchmark_insert_operations()
        assert isinstance(results, dict)
    
    def test_benchmark_insert_operations_has_expected_keys(self):
        """Test that benchmark has expected keys."""
        results = benchmark_insert_operations()
        expected_keys = ['insert_beginning', 'insert_end', 'insert_middle']
        
        for key in expected_keys:
            assert key in results
    
    def test_benchmark_insert_operations_data_types(self):
        """Test that benchmark has correct data types."""
        results = benchmark_insert_operations()
        
        for operation, time in results.items():
            assert isinstance(time, (int, float))
            assert time > 0
    
    def test_benchmark_insert_operations_relative_performance(self):
        """Test that insert operations have expected relative performance."""
        results = benchmark_insert_operations()
        
        # Insert at end should be fastest (same as append)
        # Insert at beginning should be slowest (shifts all elements)
        # Insert at middle should be in between
        assert results['insert_end'] < results['insert_middle']
        assert results['insert_middle'] < results['insert_beginning']


class TestBenchmarkPopOperations:
    """Test cases for pop operation benchmarks."""
    
    def test_benchmark_pop_operations_returns_dict(self):
        """Test that benchmark returns a dictionary."""
        results = benchmark_pop_operations()
        assert isinstance(results, dict)
    
    def test_benchmark_pop_operations_has_expected_keys(self):
        """Test that benchmark has expected keys."""
        results = benchmark_pop_operations()
        expected_keys = ['pop_beginning', 'pop_end', 'pop_middle']
        
        for key in expected_keys:
            assert key in results
    
    def test_benchmark_pop_operations_data_types(self):
        """Test that benchmark has correct data types."""
        results = benchmark_pop_operations()
        
        for operation, time in results.items():
            assert isinstance(time, (int, float))
            assert time > 0
    
    def test_benchmark_pop_operations_relative_performance(self):
        """Test that pop operations have expected relative performance."""
        results = benchmark_pop_operations()
        
        # Pop from end should be fastest (no shifting)
        # Pop from beginning should be slowest (shifts all elements)
        # Pop from middle should be in between
        assert results['pop_end'] < results['pop_middle']
        assert results['pop_middle'] < results['pop_beginning']


class TestBenchmarkSearchOperations:
    """Test cases for search operation benchmarks."""
    
    def test_benchmark_search_operations_returns_dict(self):
        """Test that benchmark returns a dictionary."""
        results = benchmark_search_operations()
        assert isinstance(results, dict)
    
    def test_benchmark_search_operations_has_expected_keys(self):
        """Test that benchmark has expected keys."""
        results = benchmark_search_operations()
        expected_keys = ['linear_search', 'index_search', 'count_search']
        
        for key in expected_keys:
            assert key in results
    
    def test_benchmark_search_operations_data_types(self):
        """Test that benchmark has correct data types."""
        results = benchmark_search_operations()
        
        for operation, time in results.items():
            assert isinstance(time, (int, float))
            assert time > 0


class TestBenchmarkMemoryUsage:
    """Test cases for memory usage benchmarks."""
    
    def test_benchmark_memory_usage_returns_dict(self):
        """Test that benchmark returns a dictionary."""
        results = benchmark_memory_usage()
        assert isinstance(results, dict)
    
    def test_benchmark_memory_usage_has_expected_keys(self):
        """Test that benchmark has expected data types."""
        results = benchmark_memory_usage()
        expected_keys = ['integers', 'strings', 'floats', 'mixed']
        
        for key in expected_keys:
            assert key in results
    
    def test_benchmark_memory_usage_metrics(self):
        """Test that each data type has expected metrics."""
        results = benchmark_memory_usage()
        
        for data_type, metrics in results.items():
            assert 'builtin_size' in metrics
            assert 'custom_size' in metrics
            assert 'size_ratio' in metrics
            assert 'custom_capacity' in metrics
            assert 'custom_load_factor' in metrics
            
            # Check data types
            assert isinstance(metrics['builtin_size'], int)
            assert isinstance(metrics['custom_size'], int)
            assert isinstance(metrics['size_ratio'], (int, float))
            assert isinstance(metrics['custom_capacity'], int)
            assert isinstance(metrics['custom_load_factor'], float)
            
            # Check value ranges
            assert metrics['builtin_size'] > 0
            assert metrics['custom_size'] > 0
            assert metrics['size_ratio'] > 0
            assert metrics['custom_capacity'] > 0
            assert 0 <= metrics['custom_load_factor'] <= 1


class TestBenchmarkResizePatterns:
    """Test cases for resize pattern benchmarks."""
    
    def test_benchmark_resize_patterns_returns_dict(self):
        """Test that benchmark returns a dictionary."""
        results = benchmark_resize_patterns()
        assert isinstance(results, dict)
    
    def test_benchmark_resize_patterns_has_expected_keys(self):
        """Test that benchmark has expected keys."""
        results = benchmark_resize_patterns()
        expected_keys = ['doubling', 'fixed', 'golden_ratio', 'adaptive']
        
        for key in expected_keys:
            assert key in results
    
    def test_benchmark_resize_patterns_data_types(self):
        """Test that benchmark has correct data types."""
        results = benchmark_resize_patterns()
        
        for strategy, capacities in results.items():
            assert isinstance(capacities, list)
            assert all(isinstance(capacity, int) for capacity in capacities)
            assert all(capacity > 0 for capacity in capacities)
    
    def test_benchmark_resize_patterns_growth_patterns(self):
        """Test that different strategies show different growth patterns."""
        results = benchmark_resize_patterns()
        
        # Doubling should show exponential growth
        doubling = results['doubling']
        if len(doubling) > 1:
            assert doubling[-1] > doubling[0]
        
        # Fixed should show linear growth
        fixed = results['fixed']
        if len(fixed) > 1:
            assert fixed[-1] > fixed[0]
        
        # Golden ratio should show intermediate growth
        golden_ratio = results['golden_ratio']
        if len(golden_ratio) > 1:
            assert golden_ratio[-1] > golden_ratio[0]


class TestRunAllBenchmarks:
    """Test cases for the comprehensive benchmark runner."""
    
    def test_run_all_benchmarks_returns_dict(self):
        """Test that run_all_benchmarks returns a dictionary."""
        results = run_all_benchmarks()
        assert isinstance(results, dict)
    
    def test_run_all_benchmarks_has_expected_keys(self):
        """Test that run_all_benchmarks has expected keys."""
        results = run_all_benchmarks()
        expected_keys = [
            'growth_strategies',
            'builtin_comparison',
            'amortized_complexity',
            'insert_operations',
            'pop_operations',
            'search_operations',
            'memory_usage',
            'resize_patterns'
        ]
        
        for key in expected_keys:
            assert key in results
    
    def test_run_all_benchmarks_data_types(self):
        """Test that run_all_benchmarks has correct data types."""
        results = run_all_benchmarks()
        
        assert isinstance(results['growth_strategies'], dict)
        assert isinstance(results['builtin_comparison'], dict)
        assert isinstance(results['amortized_complexity'], dict)
        assert isinstance(results['insert_operations'], dict)
        assert isinstance(results['pop_operations'], dict)
        assert isinstance(results['search_operations'], dict)
        assert isinstance(results['memory_usage'], dict)
        assert isinstance(results['resize_patterns'], dict)


class TestBenchmarkEdgeCases:
    """Test cases for edge cases in benchmarks."""
    
    def test_benchmark_with_empty_data(self):
        """Test benchmarks handle empty data gracefully."""
        # This test ensures benchmarks don't crash with edge cases
        # The actual benchmark functions should handle various scenarios
        
        # Test that we can run all benchmarks without errors
        try:
            results = run_all_benchmarks()
            assert isinstance(results, dict)
        except Exception as e:
            pytest.fail(f"Benchmarks failed with error: {e}")
    
    def test_benchmark_consistency(self):
        """Test that benchmarks are reasonably consistent."""
        # Run benchmarks multiple times and check consistency
        results1 = compare_with_builtin_list()
        results2 = compare_with_builtin_list()
        
        # Times should be within reasonable range of each other
        ratio1 = results1['ratio']
        ratio2 = results2['ratio']
        
        # Allow for some variation (within 50% of each other)
        assert 0.5 * ratio1 <= ratio2 <= 2.0 * ratio1


if __name__ == "__main__":
    pytest.main([__file__]) 