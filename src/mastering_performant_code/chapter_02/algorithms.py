"""
Algorithm implementations for benchmarking and complexity analysis.

This module contains various implementations of common algorithms
to demonstrate different complexity classes and optimization techniques.
"""

import timeit
from typing import Dict, List, Any, Callable
from functools import lru_cache


def sum_builtin(n: int) -> int:
    """
    Sum numbers from 0 to n-1 using built-in sum function.
    
    Complexity: O(n) - Linear
    """
    return sum(range(n))


def sum_loop(n: int) -> int:
    """
    Sum numbers from 0 to n-1 using a simple loop.
    
    Complexity: O(n) - Linear
    """
    total = 0
    for i in range(n):
        total += i
    return total


def sum_comprehension(n: int) -> int:
    """
    Sum numbers from 0 to n-1 using list comprehension.
    
    Complexity: O(n) - Linear (but creates intermediate list)
    """
    return sum([i for i in range(n)])


def sum_generator(n: int) -> int:
    """
    Sum numbers from 0 to n-1 using generator expression.
    
    Complexity: O(n) - Linear (no intermediate list)
    """
    return sum(i for i in range(n))


def sum_formula(n: int) -> int:
    """
    Sum numbers from 0 to n-1 using mathematical formula.
    
    Complexity: O(1) - Constant
    """
    return (n - 1) * n // 2


def fibonacci_recursive(n: int) -> int:
    """
    Calculate nth Fibonacci number using recursion.
    
    Complexity: O(2^n) - Exponential
    """
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_iterative(n: int) -> int:
    """
    Calculate nth Fibonacci number using iteration.
    
    Complexity: O(n) - Linear
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


@lru_cache(maxsize=None)
def fibonacci_memoized(n: int) -> int:
    """
    Calculate nth Fibonacci number using recursion with memoization.
    
    Complexity: O(n) - Linear (after memoization)
    """
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def fibonacci_dynamic(n: int) -> int:
    """
    Calculate nth Fibonacci number using dynamic programming.
    
    Complexity: O(n) - Linear
    """
    if n <= 1:
        return n
    
    fib = [0] * (n + 1)
    fib[1] = 1
    
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    
    return fib[n]


def slow_function() -> int:
    """
    A deliberately slow function for profiling demonstration.
    
    Complexity: O(n²) - Quadratic
    """
    total = 0
    for i in range(10000):
        for j in range(100):
            total += i * j
    return total


def optimized_function() -> int:
    """
    An optimized version of the slow function.
    
    Complexity: O(n) - Linear
    """
    total = 0
    for i in range(10000):
        total += i * 4950  # Sum of 0 to 99
    return total


def bubble_sort(arr: List[int]) -> List[int]:
    """
    Sort a list using bubble sort algorithm.
    
    Complexity: O(n²) - Quadratic
    """
    arr = arr.copy()
    n = len(arr)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr


def quick_sort(arr: List[int]) -> List[int]:
    """
    Sort a list using quick sort algorithm.
    
    Complexity: O(n log n) average case, O(n²) worst case
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def linear_search(arr: List[int], target: int) -> int:
    """
    Search for a target value in a list using linear search.
    
    Complexity: O(n) - Linear
    """
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def binary_search(arr: List[int], target: int) -> int:
    """
    Search for a target value in a sorted list using binary search.
    
    Complexity: O(log n) - Logarithmic
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def matrix_multiply_slow(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """
    Multiply two matrices using naive algorithm.
    
    Complexity: O(n³) - Cubic
    """
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    
    if cols_a != rows_b:
        raise ValueError("Matrix dimensions don't match for multiplication")
    
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result


def matrix_multiply_optimized(a: List[List[int]], b: List[List[int]]) -> List[List[int]]:
    """
    Multiply two matrices using optimized algorithm (same complexity but better cache locality).
    
    Complexity: O(n³) - Cubic (but better constant factors)
    """
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    
    if cols_a != rows_b:
        raise ValueError("Matrix dimensions don't match for multiplication")
    
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]
    
    # Transpose matrix b for better cache locality
    b_transposed = list(zip(*b))
    
    for i in range(rows_a):
        for j in range(cols_b):
            result[i][j] = sum(a[i][k] * b_transposed[j][k] for k in range(cols_a))
    
    return result


def generate_test_data(size: int) -> Dict[str, Any]:
    """
    Generate test data for benchmarking.
    
    Args:
        size: Size of the test data
        
    Returns:
        Dictionary containing various test data structures
    """
    return {
        'list': list(range(size)),
        'set': set(range(size)),
        'dict': {i: i for i in range(size)},
        'tuple': tuple(range(size)),
        'sorted_list': sorted(range(size)),
        'reversed_list': list(range(size, 0, -1)),
        'random_list': list(range(size))  # In practice, you'd shuffle this
    }


def benchmark_sum_functions(n: int = 10000) -> Dict[str, float]:
    """
    Benchmark different sum function implementations.
    
    Args:
        n: Size of the range to sum
        
    Returns:
        Dictionary mapping function names to execution times
    """
    functions = {
        'sum_builtin': sum_builtin,
        'sum_loop': sum_loop,
        'sum_comprehension': sum_comprehension,
        'sum_generator': sum_generator,
        'sum_formula': sum_formula
    }
    
    results = {}
    for name, func in functions.items():
        try:
            time_taken = timeit.timeit(lambda: func(n), number=1000)
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
        'fibonacci_iterative': fibonacci_iterative,
        'fibonacci_memoized': fibonacci_memoized,
        'fibonacci_dynamic': fibonacci_dynamic
    }
    
    # Note: We exclude fibonacci_recursive for large n as it's too slow
    if n <= 20:
        functions['fibonacci_recursive'] = fibonacci_recursive
    
    results = {}
    for name, func in functions.items():
        try:
            time_taken = timeit.timeit(lambda: func(n), number=100)
            results[name] = time_taken / 100  # Average time per call
        except Exception as e:
            results[name] = f"Error: {e}"
    
    return results


def benchmark_sorting_algorithms(size: int = 1000) -> Dict[str, float]:
    """
    Benchmark different sorting algorithms.
    
    Args:
        size: Size of the list to sort
        
    Returns:
        Dictionary mapping algorithm names to execution times
    """
    import random
    
    # Generate test data
    test_data = list(range(size))
    random.shuffle(test_data)
    
    functions = {
        'bubble_sort': lambda: bubble_sort(test_data),
        'quick_sort': lambda: quick_sort(test_data),
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
    print("-" * 40)
    
    # Sort by execution time (fastest first)
    sorted_results = sorted(results.items(), key=lambda x: x[1] if isinstance(x[1], float) else float('inf'))
    
    for name, time_result in sorted_results:
        if isinstance(time_result, float):
            print(f"{name:20s}: {time_result:.8f} seconds")
        else:
            print(f"{name:20s}: {time_result}")
    
    print("=" * 40)


if __name__ == "__main__":
    # Run all benchmarks
    print("Running Algorithm Benchmarks...")
    
    print_benchmark_results(benchmark_sum_functions(10000), "Sum Functions Benchmark")
    print_benchmark_results(benchmark_fibonacci_functions(30), "Fibonacci Functions Benchmark")
    print_benchmark_results(benchmark_sorting_algorithms(1000), "Sorting Algorithms Benchmark")
    print_benchmark_results(benchmark_search_algorithms(10000), "Search Algorithms Benchmark") 