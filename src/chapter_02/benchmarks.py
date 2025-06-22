"""
Comprehensive benchmarking suite for Python data structures and operations.

This module provides benchmarking functions for comparing the performance
of different Python data structures and operations using timeit.
"""

import timeit
import sys
import random
from typing import Dict, List, Any, Callable, Tuple
from .algorithms import (
    sum_builtin, sum_loop, sum_comprehension, sum_generator, sum_formula,
    fibonacci_recursive, fibonacci_iterative, fibonacci_memoized, fibonacci_dynamic,
    bubble_sort, quick_sort, linear_search, binary_search
)


def benchmark_sum_functions(n: int = 10000) -> Dict[str, float]:
    """
    Benchmark different sum function implementations.
    
    Args:
        n: Size of the range to sum
        
    Returns:
        Dictionary mapping function names to execution times
    """
    functions = {
        'sum_builtin': lambda: sum_builtin(n),
        'sum_loop': lambda: sum_loop(n),
        'sum_comprehension': lambda: sum_comprehension(n),
        'sum_generator': lambda: sum_generator(n),
        'sum_formula': lambda: sum_formula(n)
    }
    
    results = {}
    for name, func in functions.items():
        try:
            time_taken = timeit.timeit(func, number=1000)
            results[name] = time_taken / 1000  # Average time per call
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def benchmark_fibonacci_functions(n: int = 30) -> Dict[str, float]:
    """
    Benchmark different Fibonacci function implementations.
    
    Args:
        n: Fibonacci number to calculate
        
    Returns:
        Dictionary mapping function names to execution times
    """
    functions = {
        'fibonacci_iterative': lambda: fibonacci_iterative(n),
        'fibonacci_memoized': lambda: fibonacci_memoized(n),
        'fibonacci_dynamic': lambda: fibonacci_dynamic(n)
    }
    
    # Note: We exclude fibonacci_recursive for large n as it's too slow
    if n <= 20:
        functions['fibonacci_recursive'] = lambda: fibonacci_recursive(n)
    
    results = {}
    for name, func in functions.items():
        try:
            time_taken = timeit.timeit(func, number=100)
            results[name] = time_taken / 100  # Average time per call
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def benchmark_list_operations(size: int = 10000) -> Dict[str, float]:
    """
    Benchmark common list operations.
    
    Args:
        size: Size of the list for testing
        
    Returns:
        Dictionary mapping operation names to execution times
    """
    # Setup test data
    test_list = list(range(size))
    test_list_sorted = sorted(test_list)
    
    operations = {
        'append': lambda: test_list.append(999),
        'insert_beginning': lambda: test_list.insert(0, 999),
        'insert_middle': lambda: test_list.insert(size//2, 999),
        'pop_end': lambda: test_list.pop(),
        'pop_beginning': lambda: test_list.pop(0),
        'index': lambda: test_list.index(size//2),
        'contains': lambda: size//2 in test_list,
        'sort': lambda: sorted(test_list),
        'reverse': lambda: list(reversed(test_list)),
        'slice': lambda: test_list[:size//2],
        'concatenate': lambda: test_list + test_list,
        'extend': lambda: test_list.extend(range(100))
    }
    
    results = {}
    for name, operation in operations.items():
        try:
            # Reset test data for each operation
            if 'list' in name or name in ['append', 'insert_beginning', 'insert_middle', 'pop_end', 'pop_beginning', 'extend']:
                test_list = list(range(size))
            
            time_taken = timeit.timeit(operation, number=1000)
            results[name] = time_taken / 1000
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def benchmark_dict_operations(size: int = 10000) -> Dict[str, float]:
    """
    Benchmark common dictionary operations.
    
    Args:
        size: Size of the dictionary for testing
        
    Returns:
        Dictionary mapping operation names to execution times
    """
    # Setup test data
    test_dict = {i: i for i in range(size)}
    
    operations = {
        'get_existing': lambda: test_dict.get(size//2),
        'get_missing': lambda: test_dict.get(-1),
        'set_new': lambda: test_dict.__setitem__(size+1, size+1),
        'set_existing': lambda: test_dict.__setitem__(size//2, 999),
        'delete': lambda: test_dict.__delitem__(size//2),
        'contains_key': lambda: size//2 in test_dict,
        'contains_value': lambda: size//2 in test_dict.values(),
        'keys': lambda: list(test_dict.keys()),
        'values': lambda: list(test_dict.values()),
        'items': lambda: list(test_dict.items()),
        'update': lambda: test_dict.update({size+1: size+1}),
        'clear': lambda: test_dict.clear()
    }
    
    results = {}
    for name, operation in operations.items():
        try:
            # Reset test data for destructive operations
            if name in ['set_new', 'set_existing', 'delete', 'update', 'clear']:
                test_dict = {i: i for i in range(size)}
            
            time_taken = timeit.timeit(operation, number=1000)
            results[name] = time_taken / 1000
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def benchmark_set_operations(size: int = 10000) -> Dict[str, float]:
    """
    Benchmark common set operations.
    
    Args:
        size: Size of the set for testing
        
    Returns:
        Dictionary mapping operation names to execution times
    """
    # Setup test data
    test_set = set(range(size))
    other_set = set(range(size//2, size + size//2))
    
    operations = {
        'add': lambda: test_set.add(size+1),
        'remove': lambda: test_set.discard(size//2),
        'contains': lambda: size//2 in test_set,
        'union': lambda: test_set.union(other_set),
        'intersection': lambda: test_set.intersection(other_set),
        'difference': lambda: test_set.difference(other_set),
        'symmetric_difference': lambda: test_set.symmetric_difference(other_set),
        'issubset': lambda: test_set.issubset(other_set),
        'issuperset': lambda: test_set.issuperset(other_set),
        'clear': lambda: test_set.clear()
    }
    
    results = {}
    for name, operation in operations.items():
        try:
            # Reset test data for destructive operations
            if name in ['add', 'remove', 'clear']:
                test_set = set(range(size))
            
            time_taken = timeit.timeit(operation, number=1000)
            results[name] = time_taken / 1000
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def benchmark_memory_usage(size: int = 10000) -> Dict[str, int]:
    """
    Benchmark memory usage of different data structures.
    
    Args:
        size: Size of the data structures to test
        
    Returns:
        Dictionary mapping data structure names to memory usage in bytes
    """
    data_structures = {
        'list': list(range(size)),
        'tuple': tuple(range(size)),
        'set': set(range(size)),
        'dict': {i: i for i in range(size)},
        'generator': (i for i in range(size))
    }
    
    results = {}
    for name, data_structure in data_structures.items():
        if name == 'generator':
            # For generators, we need to materialize them to measure
            results[name] = sys.getsizeof(list(data_structure))
        else:
            results[name] = sys.getsizeof(data_structure)
    
    return results


def benchmark_complexity_analysis(func: Callable, input_sizes: List[int]) -> Dict[str, Any]:
    """
    Analyze the time complexity of a function by measuring execution time
    across different input sizes.
    
    Args:
        func: The function to analyze
        input_sizes: List of input sizes to test
        
    Returns:
        Dictionary containing complexity analysis results
    """
    times = []
    
    for size in input_sizes:
        try:
            time_taken = timeit.timeit(lambda: func(size), number=100)
            times.append((size, time_taken / 100))
        except Exception as e:
            print(f"Error testing size {size}: {e}")
            continue
    
    if len(times) < 2:
        return {"error": "Insufficient data for complexity analysis"}
    
    # Calculate growth rates
    growth_rates = []
    for i in range(1, len(times)):
        size_ratio = times[i][0] / times[i-1][0]
        time_ratio = times[i][1] / times[i-1][1]
        growth_rates.append(time_ratio / size_ratio)
    
    avg_growth_rate = sum(growth_rates) / len(growth_rates)
    
    # Estimate complexity
    if avg_growth_rate < 1.1:
        complexity = "O(1) - Constant"
    elif avg_growth_rate < 1.5:
        complexity = "O(log n) - Logarithmic"
    elif avg_growth_rate < 2.5:
        complexity = "O(n) - Linear"
    elif avg_growth_rate < 4.0:
        complexity = "O(n log n) - Linearithmic"
    elif avg_growth_rate < 8.0:
        complexity = "O(n²) - Quadratic"
    else:
        complexity = "O(n³) or higher - Polynomial"
    
    return {
        'input_sizes': [t[0] for t in times],
        'execution_times': [t[1] for t in times],
        'growth_rates': growth_rates,
        'average_growth_rate': avg_growth_rate,
        'estimated_complexity': complexity
    }


def benchmark_sorting_algorithms(size: int = 1000) -> Dict[str, float]:
    """
    Benchmark different sorting algorithms.
    
    Args:
        size: Size of the list to sort
        
    Returns:
        Dictionary mapping algorithm names to execution times
    """
    # Generate test data
    test_data = list(range(size))
    random.shuffle(test_data)
    
    functions = {
        'bubble_sort': lambda: bubble_sort(test_data.copy()),
        'quick_sort': lambda: quick_sort(test_data.copy()),
        'builtin_sort': lambda: sorted(test_data)
    }
    
    results = {}
    for name, func in functions.items():
        try:
            time_taken = timeit.timeit(func, number=10)
            results[name] = time_taken / 10  # Average time per call
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def benchmark_search_algorithms(size: int = 10000) -> Dict[str, float]:
    """
    Benchmark different search algorithms.
    
    Args:
        size: Size of the list to search in
        
    Returns:
        Dictionary mapping algorithm names to execution times
    """
    # Generate test data
    test_list = list(range(size))
    target = size // 2  # Search for middle element
    
    functions = {
        'linear_search': lambda: linear_search(test_list, target),
        'binary_search': lambda: binary_search(test_list, target)
    }
    
    results = {}
    for name, func in functions.items():
        try:
            time_taken = timeit.timeit(func, number=1000)
            results[name] = time_taken / 1000  # Average time per call
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def print_benchmark_results(results: Dict[str, float], title: str) -> None:
    """
    Print benchmark results in a formatted way.
    
    Args:
        results: Dictionary of benchmark results
        title: Title for the benchmark
    """
    print(f"\n=== {title} ===")
    print("-" * 50)
    
    # Sort by execution time (fastest first)
    sorted_results = sorted(
        results.items(), 
        key=lambda x: x[1] if isinstance(x[1], float) else float('inf')
    )
    
    for name, time_result in sorted_results:
        if isinstance(time_result, float):
            print(f"{name:25s}: {time_result:.8f} seconds")
        else:
            print(f"{name:25s}: {time_result}")
    
    print("=" * 50)


def run_all_benchmarks() -> None:
    """
    Run all benchmarks and print results.
    """
    print("Running Comprehensive Python Data Structure Benchmarks")
    print("=" * 60)
    
    # Algorithm benchmarks
    print_benchmark_results(benchmark_sum_functions(10000), "Sum Functions Benchmark")
    print_benchmark_results(benchmark_fibonacci_functions(30), "Fibonacci Functions Benchmark")
    print_benchmark_results(benchmark_sorting_algorithms(1000), "Sorting Algorithms Benchmark")
    print_benchmark_results(benchmark_search_algorithms(10000), "Search Algorithms Benchmark")
    
    # Data structure benchmarks
    print_benchmark_results(benchmark_list_operations(10000), "List Operations Benchmark")
    print_benchmark_results(benchmark_dict_operations(10000), "Dictionary Operations Benchmark")
    print_benchmark_results(benchmark_set_operations(10000), "Set Operations Benchmark")
    
    # Memory usage benchmark
    print("\n=== Memory Usage Benchmark ===")
    print("-" * 50)
    memory_results = benchmark_memory_usage(10000)
    for name, memory in memory_results.items():
        print(f"{name:25s}: {memory:,} bytes")
    print("=" * 50)
    
    # Complexity analysis
    print("\n=== Complexity Analysis ===")
    print("-" * 50)
    
    # Test different functions
    test_functions = [
        (sum_formula, "Sum Formula (O(1))"),
        (sum_builtin, "Sum Builtin (O(n))"),
        (lambda n: sum(i*i for i in range(n)), "Sum Squares (O(n))")
    ]
    
    input_sizes = [100, 1000, 10000]
    
    for func, name in test_functions:
        try:
            analysis = benchmark_complexity_analysis(func, input_sizes)
            if 'error' not in analysis:
                print(f"{name}:")
                print(f"  Estimated complexity: {analysis['estimated_complexity']}")
                print(f"  Average growth rate: {analysis['average_growth_rate']:.2f}")
            else:
                print(f"{name}: {analysis['error']}")
        except Exception as e:
            print(f"{name}: Error - {e}")
    
    print("=" * 50)


if __name__ == "__main__":
    run_all_benchmarks() 