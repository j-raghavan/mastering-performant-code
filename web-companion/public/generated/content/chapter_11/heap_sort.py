"""
Heap Sort Implementation

This module provides heap sort implementations using binary heaps,
including both functional and in-place versions.
"""

from typing import List, TypeVar, Callable, Optional
import timeit
from .binary_heap import BinaryHeap

T = TypeVar('T')

def heap_sort(items: List[T], key_func: Optional[Callable[[T], int]] = None, reverse: bool = False) -> List[T]:
    """
    Sort a list using heap sort algorithm.
    
    Args:
        items: List to sort
        key_func: Function to extract sort key from items
        reverse: If True, sort in descending order
        
    Returns:
        New sorted list
    """
    if not items:
        return []
    
    # Create heap - use min-heap for ascending, max-heap for descending
    heap_type = "min" if not reverse else "max"
    heap = BinaryHeap[T](heap_type=heap_type, key_func=key_func)
    
    # Build heap
    heap.heapify_bottom_up(items)
    
    # Extract elements in sorted order
    result = []
    while not heap.is_empty():
        result.append(heap.pop())
    
    return result

def heap_sort_optimized(items: List[T], key_func: Optional[Callable[[T], int]] = None, reverse: bool = False) -> List[T]:
    """
    Optimized heap sort using heapify for O(n) construction.
    
    This version is more efficient than the standard heap_sort for large datasets
    as it uses bottom-up heapify instead of repeated insertions.
    
    Args:
        items: List to sort
        key_func: Function to extract sort key from items
        reverse: If True, sort in descending order
        
    Returns:
        New sorted list
    """
    if not items:
        return []
    
    # Use heapify for O(n) construction instead of O(n log n) insertions
    # Use same logic as original heap_sort: min-heap for ascending, max-heap for descending
    heap = BinaryHeap[T](heap_type="min" if not reverse else "max", key_func=key_func)
    heap.heapify_bottom_up(items.copy())
    
    result = []
    while not heap.is_empty():
        result.append(heap.pop())
    
    return result

def heap_sort_inplace(items: List[int], reverse: bool = False) -> None:
    """
    Sort a list of integers in-place using heap sort.
    
    Args:
        items: List of integers to sort (modified in-place)
        reverse: If True, sort in descending order
    """
    if not items:
        return
    
    def heapify(arr: List[int], n: int, i: int) -> None:
        """Heapify subtree rooted at index i."""
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if reverse:
            # For descending order (min heap)
            if left < n and arr[left] < arr[largest]:
                largest = left
            if right < n and arr[right] < arr[largest]:
                largest = right
        else:
            # For ascending order (max heap)
            if left < n and arr[left] > arr[largest]:
                largest = left
            if right < n and arr[right] > arr[largest]:
                largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            heapify(arr, n, largest)
    
    n = len(items)
    
    # Build heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(items, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        items[0], items[i] = items[i], items[0]
        heapify(items, i, 0)

def heap_sort_generic_inplace(items: List[T], key_func: Optional[Callable[[T], int]] = None, reverse: bool = False) -> None:
    """
    Sort a list in-place using heap sort with generic types.
    
    Args:
        items: List to sort (modified in-place)
        key_func: Function to extract sort key from items
        reverse: If True, sort in descending order
    """
    if not items:
        return
    
    # Create a list of (key, item) pairs for sorting
    if key_func:
        keys_items = [(key_func(item), item) for item in items]
    else:
        if all(isinstance(item, (int, float)) for item in items):
            keys_items = [(item, item) for item in items]
        else:
            raise ValueError("Must provide key_func for non-numeric items")
    
    # Use min-heap for ascending, max-heap for descending
    heap_type = "min" if not reverse else "max"
    heap = BinaryHeap(heap_type=heap_type, key_func=lambda x: x[0])
    heap.heapify_bottom_up(keys_items)
    
    # Extract sorted items
    sorted_items = []
    while not heap.is_empty():
        sorted_items.append(heap.pop()[1])
    
    # Place back into original list
    items[:] = sorted_items

def benchmark_heap_sort(data_sizes: List[int], iterations: int = 100) -> dict:
    """
    Benchmark heap sort performance across different data sizes.
    
    Args:
        data_sizes: List of data sizes to test
        iterations: Number of iterations per test
        
    Returns:
        Dictionary with benchmark results
    """
    import random
    
    results = {}
    
    for size in data_sizes:
        # Generate test data
        data = [random.randint(1, 1000) for _ in range(size)]
        
        # Benchmark functional heap sort
        setup = f"data = {data.copy()}"
        stmt = "heap_sort(data)"
        time_func = timeit.timeit(stmt, setup=setup, globals={"heap_sort": heap_sort}, number=iterations)
        
        # Benchmark in-place heap sort
        setup = f"data = {data.copy()}"
        stmt = "heap_sort_inplace(data)"
        time_inplace = timeit.timeit(stmt, setup=setup, globals={"heap_sort_inplace": heap_sort_inplace}, number=iterations)
        
        # Benchmark built-in sort
        setup = f"data = {data.copy()}"
        stmt = "data.sort()"
        time_builtin = timeit.timeit(stmt, setup=setup, number=iterations)
        
        results[size] = {
            "functional_heap_sort": time_func,
            "inplace_heap_sort": time_inplace,
            "builtin_sort": time_builtin,
            "func_vs_builtin_ratio": time_func / time_builtin,
            "inplace_vs_builtin_ratio": time_inplace / time_builtin
        }
    
    return results

def verify_heap_sort_correctness() -> bool:
    """
    Verify that heap sort produces correct results.
    
    Returns:
        True if all tests pass, False otherwise
    """
    import random
    
    # Test cases
    test_cases = [
        [],  # Empty list
        [1],  # Single element
        [1, 2, 3, 4, 5],  # Already sorted
        [5, 4, 3, 2, 1],  # Reverse sorted
        [3, 1, 4, 1, 5, 9, 2, 6],  # Random
        [1, 1, 1, 1, 1],  # All same
        [random.randint(1, 100) for _ in range(100)]  # Large random
    ]
    
    for test_case in test_cases:
        # Test functional heap sort
        sorted_func = heap_sort(test_case.copy())
        expected = sorted(test_case)
        
        if sorted_func != expected:
            print(f"Functional heap sort failed for {test_case}")
            print(f"Expected: {expected}")
            print(f"Got: {sorted_func}")
            return False
        
        # Test in-place heap sort (only for integers)
        if all(isinstance(x, int) for x in test_case):
            test_copy = test_case.copy()
            heap_sort_inplace(test_copy)
            if test_copy != expected:
                print(f"In-place heap sort failed for {test_case}")
                print(f"Expected: {expected}")
                print(f"Got: {test_copy}")
                return False
    
    return True 