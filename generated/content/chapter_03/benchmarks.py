"""
Performance Benchmarks for Dynamic Arrays

This module contains benchmarking functions to compare different growth strategies
and implementations of dynamic arrays.
"""

import timeit
import sys
from typing import Dict, Any, List
from .dynamic_array import (
    DynamicArray, 
    AdvancedDynamicArray, 
    ProductionDynamicArray, 
    GrowthStrategy
)


def benchmark_growth_strategies() -> Dict[str, Dict[str, Any]]:
    """
    Benchmark different growth strategies.
    
    Returns:
        Dictionary with performance metrics for each strategy
    """
    strategies = [
        GrowthStrategy.DOUBLING,
        GrowthStrategy.FIXED,
        GrowthStrategy.GOLDEN_RATIO,
        GrowthStrategy.ADAPTIVE
    ]
    
    results = {}
    
    for strategy in strategies:
        # Test append performance
        def append_test():
            arr = ProductionDynamicArray[int](strategy=strategy)
            for i in range(10000):
                arr.append(i)
            return arr
        
        # Benchmark append operations
        append_time = timeit.timeit(append_test, number=100)
        
        # Test memory efficiency
        arr = ProductionDynamicArray[int](strategy=strategy)
        for i in range(10000):
            arr.append(i)
        
        results[strategy.value] = {
            'append_time': append_time,
            'final_capacity': arr.capacity,
            'memory_efficiency': arr.memory_efficiency,
            'resize_count': arr.resize_count,
            'load_factor': arr.load_factor
        }
    
    return results


def compare_with_builtin_list() -> Dict[str, Any]:
    """
    Compare our implementation with Python's built-in list.
    
    Returns:
        Dictionary with comparison metrics
    """
    
    # Test append performance
    def builtin_append():
        lst = []
        for i in range(10000):
            lst.append(i)
        return lst
    
    def custom_append():
        arr = ProductionDynamicArray[int]()
        for i in range(10000):
            arr.append(i)
        return arr
    
    builtin_time = timeit.timeit(builtin_append, number=100)
    custom_time = timeit.timeit(custom_append, number=100)
    
    return {
        'builtin_time': builtin_time,
        'custom_time': custom_time,
        'ratio': custom_time / builtin_time,
        'slower_by_factor': custom_time / builtin_time
    }


def analyze_amortized_complexity() -> Dict[int, Dict[str, float]]:
    """
    Analyze amortized complexity of append operations.
    
    Returns:
        Dictionary with time per element for different sizes
    """
    sizes = [100, 1000, 10000, 100000]
    results = {}
    
    for size in sizes:
        def append_n_elements():
            arr = ProductionDynamicArray[int]()
            for i in range(size):
                arr.append(i)
            return arr
        
        time_per_element = timeit.timeit(append_n_elements, number=10) / size
        
        results[size] = {
            'time_per_element': time_per_element,
            'total_time': time_per_element * size
        }
    
    return results


def benchmark_insert_operations() -> Dict[str, float]:
    """
    Benchmark different insert operations.
    
    Returns:
        Dictionary with timing for different insert scenarios
    """
    results = {}
    
    # Test insert at beginning
    def insert_at_beginning():
        arr = ProductionDynamicArray[int]()
        for i in range(1000):
            arr.insert(0, i)
        return arr
    
    # Test insert at end (same as append)
    def insert_at_end():
        arr = ProductionDynamicArray[int]()
        for i in range(1000):
            arr.insert(len(arr), i)
        return arr
    
    # Test insert at middle
    def insert_at_middle():
        arr = ProductionDynamicArray[int]()
        for i in range(1000):
            arr.insert(len(arr) // 2, i)
        return arr
    
    results['insert_beginning'] = timeit.timeit(insert_at_beginning, number=10)
    results['insert_end'] = timeit.timeit(insert_at_end, number=10)
    results['insert_middle'] = timeit.timeit(insert_at_middle, number=10)
    
    return results


def benchmark_pop_operations() -> Dict[str, float]:
    """
    Benchmark different pop operations.
    
    Returns:
        Dictionary with timing for different pop scenarios
    """
    results = {}
    
    # Test pop from beginning
    def pop_from_beginning():
        arr = ProductionDynamicArray[int]()
        # Pre-populate array
        for i in range(1000):
            arr.append(i)
        # Pop from beginning
        for _ in range(100):
            arr.pop(0)
        return arr
    
    # Test pop from end
    def pop_from_end():
        arr = ProductionDynamicArray[int]()
        # Pre-populate array
        for i in range(1000):
            arr.append(i)
        # Pop from end
        for _ in range(100):
            arr.pop()
        return arr
    
    # Test pop from middle
    def pop_from_middle():
        arr = ProductionDynamicArray[int]()
        # Pre-populate array
        for i in range(1000):
            arr.append(i)
        # Pop from middle
        for _ in range(100):
            arr.pop(len(arr) // 2)
        return arr
    
    results['pop_beginning'] = timeit.timeit(pop_from_beginning, number=10)
    results['pop_end'] = timeit.timeit(pop_from_end, number=10)
    results['pop_middle'] = timeit.timeit(pop_from_middle, number=10)
    
    return results


def benchmark_search_operations() -> Dict[str, float]:
    """
    Benchmark search operations.
    
    Returns:
        Dictionary with timing for different search scenarios
    """
    results = {}
    
    # Test linear search (contains)
    def linear_search():
        arr = ProductionDynamicArray[int]()
        # Add elements
        for i in range(1000):
            arr.append(i)
        # Search for elements
        for i in range(100):
            _ = i in arr
        return arr
    
    # Test index operation
    def index_search():
        arr = ProductionDynamicArray[int]()
        # Add elements
        for i in range(1000):
            arr.append(i)
        # Search for elements
        for i in range(100):
            try:
                _ = arr.index(i)
            except ValueError:
                pass
        return arr
    
    # Test count operation
    def count_search():
        arr = ProductionDynamicArray[int]()
        # Add elements with some duplicates
        for i in range(1000):
            arr.append(i % 100)  # Creates duplicates
        # Count elements
        for i in range(100):
            _ = arr.count(i)
        return arr
    
    results['linear_search'] = timeit.timeit(linear_search, number=10)
    results['index_search'] = timeit.timeit(index_search, number=10)
    results['count_search'] = timeit.timeit(count_search, number=10)
    
    return results


def benchmark_memory_usage() -> Dict[str, Dict[str, Any]]:
    """
    Benchmark memory usage patterns.
    
    Returns:
        Dictionary with memory usage metrics
    """
    results = {}
    
    # Test different data types
    data_types = [
        ('integers', [i for i in range(1000)]),
        ('strings', [str(i) for i in range(1000)]),
        ('floats', [float(i) for i in range(1000)]),
        ('mixed', [i if i % 2 == 0 else str(i) for i in range(1000)])
    ]
    
    for data_type, data in data_types:
        # Test built-in list
        lst = list(data)
        builtin_size = sys.getsizeof(lst)
        
        # Test our implementation
        arr = ProductionDynamicArray()
        for item in data:
            arr.append(item)
        custom_size = sys.getsizeof(arr._array)
        
        results[data_type] = {
            'builtin_size': builtin_size,
            'custom_size': custom_size,
            'size_ratio': custom_size / builtin_size if builtin_size > 0 else 0,
            'custom_capacity': arr.capacity,
            'custom_load_factor': arr.load_factor
        }
    
    return results


def benchmark_resize_patterns() -> Dict[str, List[int]]:
    """
    Analyze resize patterns for different growth strategies.
    
    Returns:
        Dictionary with resize patterns for each strategy
    """
    results = {}
    
    for strategy in GrowthStrategy:
        arr = ProductionDynamicArray[int](strategy=strategy)
        capacities = [arr.capacity]
        
        # Add elements and track capacity changes
        for i in range(1000):
            arr.append(i)
            if arr.capacity != capacities[-1]:
                capacities.append(arr.capacity)
        
        results[strategy.value] = capacities
    
    return results


def run_all_benchmarks() -> Dict[str, Any]:
    """
    Run all benchmarks and return comprehensive results.
    
    Returns:
        Dictionary with all benchmark results
    """
    print("Running dynamic array benchmarks...")
    
    results = {
        'growth_strategies': benchmark_growth_strategies(),
        'builtin_comparison': compare_with_builtin_list(),
        'amortized_complexity': analyze_amortized_complexity(),
        'insert_operations': benchmark_insert_operations(),
        'pop_operations': benchmark_pop_operations(),
        'search_operations': benchmark_search_operations(),
        'memory_usage': benchmark_memory_usage(),
        'resize_patterns': benchmark_resize_patterns()
    }
    
    print("Benchmarks completed!")
    return results


def print_benchmark_results(results: Dict[str, Any]) -> None:
    """
    Print benchmark results in a formatted way.
    
    Args:
        results: Results from run_all_benchmarks()
    """
    print("\n" + "="*60)
    print("DYNAMIC ARRAY BENCHMARK RESULTS")
    print("="*60)
    
    # Growth Strategies
    print("\n1. Growth Strategy Comparison:")
    print("-" * 40)
    for strategy, metrics in results['growth_strategies'].items():
        print(f"{strategy:15} | "
              f"Time: {metrics['append_time']:.4f}s | "
              f"Capacity: {metrics['final_capacity']:6} | "
              f"Resizes: {metrics['resize_count']:3} | "
              f"Efficiency: {metrics['memory_efficiency']:.3f}")
    
    # Built-in Comparison
    print("\n2. Built-in List Comparison:")
    print("-" * 40)
    builtin = results['builtin_comparison']
    print(f"Built-in time: {builtin['builtin_time']:.4f}s")
    print(f"Custom time:   {builtin['custom_time']:.4f}s")
    print(f"Slower by:     {builtin['slower_by_factor']:.2f}x")
    
    # Amortized Complexity
    print("\n3. Amortized Complexity Analysis:")
    print("-" * 40)
    for size, metrics in results['amortized_complexity'].items():
        print(f"Size {size:6} | Time per element: {metrics['time_per_element']:.8f}s")
    
    # Insert Operations
    print("\n4. Insert Operations:")
    print("-" * 40)
    for operation, time in results['insert_operations'].items():
        print(f"{operation:15} | {time:.4f}s")
    
    # Pop Operations
    print("\n5. Pop Operations:")
    print("-" * 40)
    for operation, time in results['pop_operations'].items():
        print(f"{operation:15} | {time:.4f}s")
    
    # Memory Usage
    print("\n6. Memory Usage:")
    print("-" * 40)
    for data_type, metrics in results['memory_usage'].items():
        print(f"{data_type:10} | "
              f"Built-in: {metrics['builtin_size']:6} bytes | "
              f"Custom: {metrics['custom_size']:6} bytes | "
              f"Ratio: {metrics['size_ratio']:.2f}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    # Run benchmarks and print results
    results = run_all_benchmarks()
    print_benchmark_results(results) 