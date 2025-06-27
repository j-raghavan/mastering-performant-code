"""
Chapter 2: Algorithmic Complexity & Profiling Techniques

This module provides tools for analyzing algorithmic complexity,
profiling Python code, and benchmarking different implementations.
"""

from .profiler import (
    PerformanceProfiler,
    MemoryProfiler,
    ComplexityAnalyzer,
    BenchmarkSuite
)

from .algorithms import (
    sum_builtin,
    sum_loop,
    sum_comprehension,
    sum_generator,
    fibonacci_recursive,
    fibonacci_iterative,
    fibonacci_memoized,
    slow_function,
    optimized_function
)

from .benchmarks import (
    benchmark_sum_functions,
    benchmark_fibonacci_functions,
    benchmark_list_operations,
    benchmark_dict_operations,
    benchmark_set_operations,
    run_all_benchmarks
)

__all__ = [
    'PerformanceProfiler',
    'MemoryProfiler', 
    'ComplexityAnalyzer',
    'BenchmarkSuite',
    'sum_builtin',
    'sum_loop',
    'sum_comprehension',
    'sum_generator',
    'fibonacci_recursive',
    'fibonacci_iterative',
    'fibonacci_memoized',
    'slow_function',
    'optimized_function',
    'benchmark_sum_functions',
    'benchmark_fibonacci_functions',
    'benchmark_list_operations',
    'benchmark_dict_operations',
    'benchmark_set_operations',
    'run_all_benchmarks'
] 