"""
Chapter 2 Demo: Algorithmic Complexity & Profiling Techniques

This script demonstrates the profiling and benchmarking tools
introduced in Chapter 2, showing how to analyze Python code performance.
"""

import sys
import timeit
import cProfile
import pstats
import io
import dis
from typing import Dict, List, Any

from .profiler import (
    PerformanceProfiler, 
    MemoryProfiler, 
    ComplexityAnalyzer, 
    BenchmarkSuite,
    timer,
    quick_benchmark
)

from .algorithms import (
    sum_builtin, sum_loop, sum_comprehension, sum_generator, sum_formula,
    fibonacci_recursive, fibonacci_iterative, fibonacci_memoized, fibonacci_dynamic,
    slow_function, optimized_function,
    bubble_sort, quick_sort, linear_search, binary_search
)

from .benchmarks import (
    benchmark_sum_functions,
    benchmark_fibonacci_functions,
    benchmark_list_operations,
    benchmark_dict_operations,
    benchmark_set_operations,
    benchmark_memory_usage,
    benchmark_complexity_analysis,
    run_all_benchmarks
)


def demo_timeit_basics():
    """Demonstrate basic timeit usage."""
    print("=== Basic timeit Examples ===")
    print()
    
    # Simple timing
    n = 10000
    print(f"Timing sum(range({n})):")
    
    time_taken = timeit.timeit(f"sum(range({n}))", number=1000)
    print(f"  Average time: {time_taken/1000:.8f} seconds")
    print()
    
    # Comparing different approaches
    print("Comparing different sum implementations:")
    
    approaches = {
        'Built-in sum': f"sum(range({n}))",
        'Loop sum': f"sum_loop({n})",
        'Generator sum': f"sum(i for i in range({n}))",
        'Formula sum': f"({n}-1)*{n}//2"
    }
    
    for name, stmt in approaches.items():
        try:
            time_taken = timeit.timeit(stmt, number=1000)
            print(f"  {name:15s}: {time_taken/1000:.8f} seconds")
        except Exception as e:
            print(f"  {name:15s}: Error - {e}")
    
    print()


def demo_cprofile():
    """Demonstrate cProfile usage."""
    print("=== cProfile Examples ===")
    print()
    
    # Profile a function
    print("Profiling slow_function():")
    
    profiler = cProfile.Profile()
    profiler.enable()
    
    try:
        result = slow_function()
    finally:
        profiler.disable()
    
    print(f"Result: {result}")
    
    # Get profiling stats
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
    stats.print_stats(5)  # Top 5 functions
    
    print("Top 5 functions by cumulative time:")
    print(s.getvalue())
    print()


def demo_memory_analysis():
    """Demonstrate memory usage analysis."""
    print("=== Memory Usage Analysis ===")
    print()
    
    # Compare different data structures
    size = 10000
    data_structures = {
        'list': list(range(size)),
        'tuple': tuple(range(size)),
        'set': set(range(size)),
        'dict': {i: i for i in range(size)}
    }
    
    print(f"Memory usage for {size} elements:")
    for name, data_structure in data_structures.items():
        memory = sys.getsizeof(data_structure)
        print(f"  {name:10s}: {memory:,} bytes")
    
    print()
    
    # Memory profiler
    memory_profiler = MemoryProfiler()
    
    print("Memory usage during function execution:")
    memory_info = memory_profiler.measure_function_memory(slow_function)
    
    if 'memory_used' in memory_info:
        print(f"  Memory used: {memory_info['memory_used']:,} bytes")
        print(f"  Result size: {memory_info['result_size']:,} bytes")
    else:
        print(f"  Error: {memory_info.get('error', 'Unknown error')}")
    
    print()


def demo_complexity_analysis():
    """Demonstrate complexity analysis."""
    print("=== Complexity Analysis ===")
    print()
    
    # Analyze different functions
    functions = [
        (sum_formula, "Sum Formula (O(1))"),
        (sum_builtin, "Sum Builtin (O(n))"),
        (lambda n: sum(i*i for i in range(n)), "Sum Squares (O(n))")
    ]
    
    input_sizes = [100, 1000, 10000]
    
    for func, name in functions:
        print(f"Analyzing {name}:")
        
        try:
            analysis = benchmark_complexity_analysis(func, input_sizes)
            
            if 'error' not in analysis:
                print(f"  Estimated complexity: {analysis['estimated_complexity']}")
                print(f"  Average growth rate: {analysis['average_growth_rate']:.2f}")
                
                print("  Execution times:")
                for size, time_taken in zip(analysis['input_sizes'], analysis['execution_times']):
                    print(f"    n={size:5d}: {time_taken:.8f} seconds")
            else:
                print(f"  Error: {analysis['error']}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print()


def demo_bytecode_analysis():
    """Demonstrate bytecode analysis."""
    print("=== Bytecode Analysis ===")
    print()
    
    # Disassemble different functions
    functions = [
        (sum_loop, "sum_loop"),
        (sum_formula, "sum_formula"),
        (fibonacci_iterative, "fibonacci_iterative")
    ]
    
    for func, name in functions:
        print(f"Bytecode for {name}:")
        print("-" * 40)
        
        try:
            bytecode = dis.Bytecode(func)
            for instruction in bytecode:
                print(f"  {instruction.opname:20s} {instruction.argrepr}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print()


def demo_performance_profiler():
    """Demonstrate the PerformanceProfiler class."""
    print("=== Performance Profiler Demo ===")
    print()
    
    profiler = PerformanceProfiler(number_of_runs=1000)
    
    # Compare sum functions
    functions = {
        'sum_builtin': sum_builtin,
        'sum_loop': sum_loop,
        'sum_generator': sum_generator,
        'sum_formula': sum_formula
    }
    
    print("Comparing sum function performance (n=10000):")
    results = profiler.compare_functions(functions, 10000)
    
    for name, time_result in results.items():
        if isinstance(time_result, float):
            print(f"  {name:15s}: {time_result:.8f} seconds")
        else:
            print(f"  {name:15s}: {time_result}")
    
    print()
    
    # Complexity analysis
    print("Complexity analysis for sum_builtin:")
    complexity = profiler.analyze_complexity(sum_builtin, [100, 1000, 10000])
    
    if 'error' not in complexity:
        print(f"  Estimated complexity: {complexity['estimated_complexity']}")
        print(f"  Average growth rate: {complexity['average_growth_rate']:.2f}")
    else:
        print(f"  Error: {complexity['error']}")
    
    print()


def demo_benchmark_suite():
    """Demonstrate the BenchmarkSuite class."""
    print("=== Benchmark Suite Demo ===")
    print()
    
    suite = BenchmarkSuite(iterations=1000)
    
    # Run a benchmark
    functions = {
        'sum_builtin': sum_builtin,
        'sum_loop': sum_loop,
        'sum_formula': sum_formula
    }
    
    results = suite.run_benchmark("Sum Functions", functions, 10000)
    suite.print_results(results)
    print()


def demo_context_manager():
    """Demonstrate the timer context manager."""
    print("=== Timer Context Manager Demo ===")
    print()
    
    with timer("Slow function execution"):
        result = slow_function()
        print(f"Result: {result}")
    
    with timer("Optimized function execution"):
        result = optimized_function()
        print(f"Result: {result}")
    
    print()


def demo_quick_benchmark():
    """Demonstrate quick_benchmark function."""
    print("=== Quick Benchmark Demo ===")
    print()
    
    functions = [
        (sum_builtin, "sum_builtin"),
        (sum_loop, "sum_loop"),
        (sum_formula, "sum_formula")
    ]
    
    n = 10000
    print(f"Quick benchmarks (n={n}):")
    
    for func, name in functions:
        try:
            time_taken = quick_benchmark(func, n, iterations=1000)
            print(f"  {name:15s}: {time_taken:.8f} seconds")
        except Exception as e:
            print(f"  {name:15s}: Error - {e}")
    
    print()


def demo_data_structure_benchmarks():
    """Demonstrate data structure benchmarks."""
    print("=== Data Structure Benchmarks ===")
    print()
    
    # List operations
    print("List Operations Benchmark:")
    list_results = benchmark_list_operations(10000)
    for name, time_result in sorted(list_results.items(), key=lambda x: x[1] if isinstance(x[1], float) else float('inf')):
        if isinstance(time_result, float):
            print(f"  {name:20s}: {time_result:.8f} seconds")
        else:
            print(f"  {name:20s}: {time_result}")
    
    print()
    
    # Dict operations
    print("Dictionary Operations Benchmark:")
    dict_results = benchmark_dict_operations(10000)
    for name, time_result in sorted(dict_results.items(), key=lambda x: x[1] if isinstance(x[1], float) else float('inf')):
        if isinstance(time_result, float):
            print(f"  {name:20s}: {time_result:.8f} seconds")
        else:
            print(f"  {name:20s}: {time_result}")
    
    print()
    
    # Set operations
    print("Set Operations Benchmark:")
    set_results = benchmark_set_operations(10000)
    for name, time_result in sorted(set_results.items(), key=lambda x: x[1] if isinstance(x[1], float) else float('inf')):
        if isinstance(time_result, float):
            print(f"  {name:20s}: {time_result:.8f} seconds")
        else:
            print(f"  {name:20s}: {time_result}")
    
    print()


def run_comprehensive_demo():
    """Run the complete demonstration."""
    print("Chapter 2: Algorithmic Complexity & Profiling Techniques")
    print("=" * 60)
    print()
    
    # Run all demos
    demo_timeit_basics()
    demo_cprofile()
    demo_memory_analysis()
    demo_complexity_analysis()
    demo_bytecode_analysis()
    demo_performance_profiler()
    demo_benchmark_suite()
    demo_context_manager()
    demo_quick_benchmark()
    demo_data_structure_benchmarks()
    
    print("=== Complete Benchmark Suite ===")
    print("Running comprehensive benchmarks...")
    print()
    
    # Run the complete benchmark suite
    run_all_benchmarks()
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    run_comprehensive_demo() 