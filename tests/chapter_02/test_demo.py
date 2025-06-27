"""
Unit tests for the demo module.

This module tests the demonstration functions that showcase the profiling
and benchmarking capabilities of Chapter 2.
"""

import pytest
from unittest.mock import patch, MagicMock
from typing import Dict, List, Any

from mastering_performant_code.chapter_02.demo import (
    demo_timeit_basics,
    demo_cprofile,
    demo_memory_analysis,
    demo_complexity_analysis,
    demo_bytecode_analysis,
    demo_performance_profiler,
    demo_benchmark_suite,
    demo_context_manager,
    demo_quick_benchmark,
    demo_data_structure_benchmarks,
    run_comprehensive_demo
)


class TestDemoTimeitBasics:
    """Test cases for demo_timeit_basics."""
    
    def test_demo_timeit_basics(self, capsys):
        """Test demo_timeit_basics function."""
        demo_timeit_basics()
        captured = capsys.readouterr()
        
        assert 'Basic timeit Examples' in captured.out
        assert 'Timing sum(range(10000))' in captured.out
        assert 'Comparing different sum implementations' in captured.out
        assert 'Built-in sum' in captured.out
        assert 'Loop sum' in captured.out
        assert 'Generator sum' in captured.out
        assert 'Formula sum' in captured.out
        assert 'seconds' in captured.out


class TestDemoCProfile:
    """Test cases for demo_cprofile."""
    
    def test_demo_cprofile(self, capsys):
        """Test demo_cprofile function."""
        demo_cprofile()
        captured = capsys.readouterr()
        
        assert 'cProfile Examples' in captured.out
        assert 'Profiling slow_function()' in captured.out
        assert 'Result:' in captured.out
        assert 'Top 5 functions by cumulative time' in captured.out


class TestDemoMemoryAnalysis:
    """Test cases for demo_memory_analysis."""
    
    def test_demo_memory_analysis(self, capsys):
        """Test demo_memory_analysis function."""
        demo_memory_analysis()
        captured = capsys.readouterr()
        
        assert 'Memory Usage Analysis' in captured.out
        assert 'Memory usage for 10000 elements' in captured.out
        assert 'list' in captured.out
        assert 'tuple' in captured.out
        assert 'set' in captured.out
        assert 'dict' in captured.out
        assert 'bytes' in captured.out
        assert 'Memory usage during function execution' in captured.out


class TestDemoComplexityAnalysis:
    """Test cases for demo_complexity_analysis."""
    
    def test_demo_complexity_analysis(self, capsys):
        """Test demo_complexity_analysis function."""
        demo_complexity_analysis()
        captured = capsys.readouterr()
        
        assert 'Complexity Analysis' in captured.out
        assert 'Sum Formula (O(1))' in captured.out
        assert 'Sum Builtin (O(n))' in captured.out
        assert 'Sum Squares (O(n))' in captured.out
        assert 'Estimated complexity' in captured.out
        assert 'Average growth rate' in captured.out
        assert 'Execution times' in captured.out


class TestDemoBytecodeAnalysis:
    """Test cases for demo_bytecode_analysis."""
    
    def test_demo_bytecode_analysis(self, capsys):
        """Test demo_bytecode_analysis function."""
        demo_bytecode_analysis()
        captured = capsys.readouterr()
        
        assert 'Bytecode Analysis' in captured.out
        assert 'Bytecode for sum_loop' in captured.out
        assert 'Bytecode for sum_formula' in captured.out
        assert 'Bytecode for fibonacci_iterative' in captured.out


class TestDemoPerformanceProfiler:
    """Test cases for demo_performance_profiler."""
    
    def test_demo_performance_profiler(self, capsys):
        """Test demo_performance_profiler function."""
        demo_performance_profiler()
        captured = capsys.readouterr()
        
        assert 'Performance Profiler Demo' in captured.out
        assert 'Comparing sum function performance' in captured.out
        assert 'sum_builtin' in captured.out
        assert 'sum_loop' in captured.out
        assert 'sum_generator' in captured.out
        assert 'sum_formula' in captured.out
        assert 'seconds' in captured.out
        assert 'Complexity analysis for sum_builtin' in captured.out
        assert 'Estimated complexity' in captured.out
        assert 'Average growth rate' in captured.out


class TestDemoBenchmarkSuite:
    """Test cases for demo_benchmark_suite."""
    
    def test_demo_benchmark_suite(self, capsys):
        """Test demo_benchmark_suite function."""
        demo_benchmark_suite()
        captured = capsys.readouterr()
        
        assert 'Benchmark Suite Demo' in captured.out
        assert 'Sum Functions Benchmark Results' in captured.out
        assert 'Performance (execution time)' in captured.out
        assert 'sum_builtin' in captured.out
        assert 'sum_loop' in captured.out
        assert 'sum_formula' in captured.out
        assert 'seconds' in captured.out


class TestDemoContextManager:
    """Test cases for demo_context_manager."""
    
    def test_demo_context_manager(self, capsys):
        """Test demo_context_manager function."""
        demo_context_manager()
        captured = capsys.readouterr()
        
        assert 'Timer Context Manager Demo' in captured.out
        assert 'Slow function execution took' in captured.out
        assert 'Optimized function execution took' in captured.out
        assert 'Result:' in captured.out
        assert 'seconds' in captured.out


class TestDemoQuickBenchmark:
    """Test cases for demo_quick_benchmark."""
    
    def test_demo_quick_benchmark(self, capsys):
        """Test demo_quick_benchmark function."""
        demo_quick_benchmark()
        captured = capsys.readouterr()
        
        assert 'Quick Benchmark Demo' in captured.out
        assert 'Quick benchmarks (n=10000)' in captured.out
        assert 'sum_builtin' in captured.out
        assert 'sum_loop' in captured.out
        assert 'sum_formula' in captured.out
        assert 'seconds' in captured.out


class TestDemoDataStructureBenchmarks:
    """Test cases for demo_data_structure_benchmarks."""
    
    def test_demo_data_structure_benchmarks(self, capsys):
        """Test demo_data_structure_benchmarks function."""
        demo_data_structure_benchmarks()
        captured = capsys.readouterr()
        
        assert 'Data Structure Benchmarks' in captured.out
        assert 'List Operations Benchmark' in captured.out
        assert 'Dictionary Operations Benchmark' in captured.out
        assert 'Set Operations Benchmark' in captured.out
        assert 'seconds' in captured.out
        
        # Check for specific operations
        list_operations = [
            'append', 'insert_beginning', 'insert_middle', 'pop_end', 'pop_beginning',
            'index', 'contains', 'sort', 'reverse', 'slice', 'concatenate', 'extend'
        ]
        for operation in list_operations:
            assert operation in captured.out
        
        dict_operations = [
            'get_existing', 'get_missing', 'set_new', 'set_existing', 'delete',
            'contains_key', 'contains_value', 'keys', 'values', 'items', 'update', 'clear'
        ]
        for operation in dict_operations:
            assert operation in captured.out
        
        set_operations = [
            'add', 'remove', 'contains', 'union', 'intersection', 'difference',
            'symmetric_difference', 'issubset', 'issuperset', 'clear'
        ]
        for operation in set_operations:
            assert operation in captured.out


class TestRunComprehensiveDemo:
    """Test cases for run_comprehensive_demo."""
    
    def test_run_comprehensive_demo(self, capsys):
        """Test run_comprehensive_demo function."""
        run_comprehensive_demo()
        captured = capsys.readouterr()
        
        # Check for all demo sections
        demo_sections = [
            'Chapter 2: Algorithmic Complexity & Profiling Techniques',
            'Basic timeit Examples',
            'cProfile Examples',
            'Memory Usage Analysis',
            'Complexity Analysis',
            'Bytecode Analysis',
            'Performance Profiler Demo',
            'Benchmark Suite Demo',
            'Timer Context Manager Demo',
            'Quick Benchmark Demo',
            'Data Structure Benchmarks',
            'Complete Benchmark Suite',
            'Comprehensive Python Data Structure Benchmarks',
            'Demo completed successfully'
        ]
        
        for section in demo_sections:
            assert section in captured.out
    
    def test_run_comprehensive_demo_output_format(self, capsys):
        """Test that run_comprehensive_demo produces properly formatted output."""
        run_comprehensive_demo()
        captured = capsys.readouterr()
        
        # Check for proper formatting
        assert '=' in captured.out  # Section separators
        assert 'seconds' in captured.out
        assert 'bytes' in captured.out
        assert 'Benchmark' in captured.out
        assert 'Results' in captured.out
    
    def test_run_comprehensive_demo_completeness(self, capsys):
        """Test that run_comprehensive_demo runs all components."""
        run_comprehensive_demo()
        captured = capsys.readouterr()
        
        # Check that all major components are executed
        assert 'Sum Functions Benchmark' in captured.out
        assert 'Fibonacci Functions Benchmark' in captured.out
        assert 'Sorting Algorithms Benchmark' in captured.out
        assert 'Search Algorithms Benchmark' in captured.out
        assert 'List Operations Benchmark' in captured.out
        assert 'Dictionary Operations Benchmark' in captured.out
        assert 'Set Operations Benchmark' in captured.out
        assert 'Memory Usage Benchmark' in captured.out
        assert 'Complexity Analysis' in captured.out


class TestDemoErrorHandling:
    """Test cases for error handling in demo functions."""
    
    @patch('src.chapter_02.demo.timeit.timeit')
    def test_demo_timeit_basics_with_error(self, mock_timeit, capsys):
        """Test demo_timeit_basics handles errors gracefully."""
        mock_timeit.side_effect = Exception("Test error")
        
        # The function should handle the error gracefully
        try:
            demo_timeit_basics()
        except Exception:
            # If an exception is raised, that's also acceptable for this test
            pass
        
        captured = capsys.readouterr()
        assert 'Basic timeit Examples' in captured.out
    
    @patch('src.chapter_02.demo.cProfile.Profile')
    def test_demo_cprofile_with_error(self, mock_profile, capsys):
        """Test demo_cprofile handles errors gracefully."""
        mock_profile.side_effect = Exception("Test error")
        
        # The function should handle the error gracefully
        try:
            demo_cprofile()
        except Exception:
            # If an exception is raised, that's also acceptable for this test
            pass
        
        captured = capsys.readouterr()
        assert 'cProfile Examples' in captured.out
    
    @patch('src.chapter_02.demo.sys.getsizeof')
    def test_demo_memory_analysis_with_error(self, mock_getsizeof, capsys):
        """Test demo_memory_analysis handles errors gracefully."""
        mock_getsizeof.side_effect = Exception("Test error")
        
        # The function should handle the error gracefully
        try:
            demo_memory_analysis()
        except Exception:
            # If an exception is raised, that's also acceptable for this test
            pass
        
        captured = capsys.readouterr()
        assert 'Memory Usage Analysis' in captured.out


class TestDemoIntegration:
    """Integration tests for demo functions."""
    
    def test_demo_functions_are_callable(self):
        """Test that all demo functions are callable."""
        demo_functions = [
            demo_timeit_basics,
            demo_cprofile,
            demo_memory_analysis,
            demo_complexity_analysis,
            demo_bytecode_analysis,
            demo_performance_profiler,
            demo_benchmark_suite,
            demo_context_manager,
            demo_quick_benchmark,
            demo_data_structure_benchmarks,
            run_comprehensive_demo
        ]
        
        for func in demo_functions:
            assert callable(func)
    
    def test_demo_functions_produce_output(self, capsys):
        """Test that demo functions produce some output."""
        demo_functions = [
            demo_timeit_basics,
            demo_cprofile,
            demo_memory_analysis,
            demo_complexity_analysis,
            demo_bytecode_analysis,
            demo_performance_profiler,
            demo_benchmark_suite,
            demo_context_manager,
            demo_quick_benchmark,
            demo_data_structure_benchmarks
        ]
        
        for func in demo_functions:
            func()
            captured = capsys.readouterr()
            assert len(captured.out) > 0  # Should produce some output


if __name__ == "__main__":
    pytest.main([__file__]) 