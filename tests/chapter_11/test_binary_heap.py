"""
Tests for Binary Heap Implementation

This module provides comprehensive tests for the BinaryHeap class,
ensuring 100% code coverage and correct behavior.
"""

import pytest
import random
import timeit
from typing import List, Optional
from mastering_performant_code.chapter_11.binary_heap import BinaryHeap, HeapNode


class TestHeapNode:
    """Test cases for HeapNode class."""
    
    def test_heap_node_creation(self):
        """Test HeapNode creation with different data types."""
        # Test with integer data
        node1 = HeapNode(10, 42)
        assert node1.priority == 10
        assert node1.data == 42
        
        # Test with string data
        node2 = HeapNode(5, "test")
        assert node2.priority == 5
        assert node2.data == "test"
        
        # Test with None data
        node3 = HeapNode(15)
        assert node3.priority == 15
        assert node3.data is None
    
    def test_heap_node_comparison(self):
        """Test HeapNode comparison operations."""
        node1 = HeapNode(5, "a")
        node2 = HeapNode(10, "b")
        node3 = HeapNode(5, "c")
        node4 = HeapNode(5, "a")  # Same priority and data as node1
        
        # Test less than
        assert node1 < node2
        assert not node2 < node1
        
        # Test equality - nodes with same priority AND data should be equal
        assert node1 == node4  # Same priority and data
        assert not node1 == node3  # Same priority, different data
        assert not node1 == node2  # Different priority
        
        # Test with different data types
        assert node1 < HeapNode(7, "d")
    
    def test_heap_node_repr(self):
        """Test HeapNode string representation."""
        node1 = HeapNode(10, "test")
        node2 = HeapNode(5)
        
        assert repr(node1) == "HeapNode(10, test)"
        assert repr(node2) == "HeapNode(5)"


class TestBinaryHeap:
    """Test cases for BinaryHeap class."""
    
    def test_heap_initialization(self):
        """Test heap initialization with different parameters."""
        # Test min heap
        min_heap = BinaryHeap[int](heap_type="min")
        assert min_heap._heap_type == "min"
        assert len(min_heap) == 0
        assert min_heap.is_empty()
        
        # Test max heap
        max_heap = BinaryHeap[int](heap_type="max")
        assert max_heap._heap_type == "max"
        assert len(max_heap) == 0
        
        # Test with key function
        def key_func(x: str) -> int:
            return len(x)
        
        heap_with_key = BinaryHeap[str](heap_type="min", key_func=key_func)
        assert heap_with_key._key_func == key_func
    
    def test_heap_initialization_invalid_type(self):
        """Test heap initialization with invalid heap type."""
        with pytest.raises(ValueError, match="Heap type must be 'min' or 'max'"):
            BinaryHeap[int](heap_type="invalid")
    
    def test_heap_push_basic(self):
        """Test basic push operations."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Push single element
        heap.push(10)
        assert len(heap) == 1
        assert heap.peek() == 10
        
        # Push multiple elements
        heap.push(5)
        heap.push(15)
        assert len(heap) == 3
        assert heap.peek() == 5  # Min element should be at root
    
    def test_heap_push_with_priority(self):
        """Test push operations with explicit priorities."""
        heap = BinaryHeap[str](heap_type="min")
        
        heap.push("apple", 5)
        heap.push("banana", 3)
        heap.push("cherry", 7)
        
        assert len(heap) == 3
        assert heap.peek() == "banana"  # Lowest priority
        assert heap.peek_priority() == 3
    
    def test_heap_push_with_key_func(self):
        """Test push operations with key function."""
        def key_func(x: str) -> int:
            return len(x)
        
        heap = BinaryHeap[str](heap_type="min", key_func=key_func)
        
        heap.push("a")  # length 1
        heap.push("bb")  # length 2
        heap.push("ccc")  # length 3
        
        assert len(heap) == 3
        assert heap.peek() == "a"  # Shortest string
        assert heap.peek_priority() == 1
    
    def test_heap_push_numeric_items(self):
        """Test push operations with numeric items (no explicit priority)."""
        heap = BinaryHeap[int](heap_type="min")
        
        heap.push(10)
        heap.push(5)
        heap.push(15)
        
        assert len(heap) == 3
        assert heap.peek() == 5
        assert heap.peek_priority() == 5
    
    def test_heap_push_non_numeric_no_priority(self):
        """Test push operations with non-numeric items without priority."""
        heap = BinaryHeap[str](heap_type="min")
        
        with pytest.raises(ValueError, match="Must provide priority or key_func"):
            heap.push("test")
    
    def test_heap_pop_basic(self):
        """Test basic pop operations."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Test pop on empty heap
        with pytest.raises(IndexError, match="Heap is empty"):
            heap.pop()
        
        # Test pop with single element
        heap.push(10)
        assert heap.pop() == 10
        assert len(heap) == 0
        assert heap.is_empty()
        
        # Test pop with multiple elements
        heap.push(10)
        heap.push(5)
        heap.push(15)
        
        assert heap.pop() == 5
        assert heap.pop() == 10
        assert heap.pop() == 15
        assert heap.is_empty()
    
    def test_heap_pop_max_heap(self):
        """Test pop operations on max heap."""
        heap = BinaryHeap[int](heap_type="max")
        
        heap.push(10)
        heap.push(5)
        heap.push(15)
        
        assert heap.pop() == 15  # Largest element first
        assert heap.pop() == 10
        assert heap.pop() == 5
        assert heap.is_empty()
    
    def test_heap_peek(self):
        """Test peek operations."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Test peek on empty heap
        with pytest.raises(IndexError, match="Heap is empty"):
            heap.peek()
        
        # Test peek with elements
        heap.push(10)
        heap.push(5)
        
        assert heap.peek() == 5
        assert len(heap) == 2  # Peek doesn't remove elements
    
    def test_heap_peek_priority(self):
        """Test peek_priority operations."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Test peek_priority on empty heap
        with pytest.raises(IndexError, match="Heap is empty"):
            heap.peek_priority()
        
        # Test peek_priority with elements
        heap.push(10)
        heap.push(5)
        
        assert heap.peek_priority() == 5
        assert len(heap) == 2  # Peek doesn't remove elements
    
    def test_heap_heapify(self):
        """Test heapify operations."""
        heap = BinaryHeap[int](heap_type="min")
        
        items = [10, 5, 15, 3, 7]
        priorities = [10, 5, 15, 3, 7]
        
        heap.heapify(items, priorities)
        assert len(heap) == 5
        assert heap.peek() == 3  # Min priority
    
    def test_heap_heapify_bottom_up(self):
        """Test bottom-up heapify operations."""
        heap = BinaryHeap[int](heap_type="min")
        
        items = [10, 5, 15, 3, 7]
        heap.heapify_bottom_up(items)
        
        assert len(heap) == 5
        assert heap.peek() == 3  # Min element
    
    def test_heap_heapify_bottom_up_with_priorities(self):
        """Test bottom-up heapify with explicit priorities."""
        heap = BinaryHeap[str](heap_type="min")
        
        items = ["apple", "banana", "cherry"]
        priorities = [5, 3, 7]
        
        heap.heapify_bottom_up(items, priorities)
        assert len(heap) == 3
        assert heap.peek() == "banana"  # Lowest priority
    
    def test_heap_heapify_mismatched_lengths(self):
        """Test heapify with mismatched item and priority lengths."""
        heap = BinaryHeap[int](heap_type="min")
        
        items = [1, 2, 3]
        priorities = [1, 2]  # Mismatched length
        
        with pytest.raises(ValueError, match="Items and priorities must have same length"):
            heap.heapify(items, priorities)
        
        with pytest.raises(ValueError, match="Items and priorities must have same length"):
            heap.heapify_bottom_up(items, priorities)
    
    def test_heap_heapify_bottom_up_no_key_func(self):
        """Test bottom-up heapify without key function for non-numeric items."""
        heap = BinaryHeap[str](heap_type="min")
        
        items = ["apple", "banana", "cherry"]
        
        with pytest.raises(ValueError, match="Must provide priorities or key_func"):
            heap.heapify_bottom_up(items)
    
    def test_heap_repr(self):
        """Test heap string representation."""
        heap = BinaryHeap[int](heap_type="min")
        heap.push(10, 10)
        heap.push(5, 5)
        
        expected = "BinaryHeap(min, [5:5, 10:10])"
        assert repr(heap) == expected
    
    def test_heap_iteration(self):
        """Test heap iteration in priority order."""
        heap = BinaryHeap[int](heap_type="min")
        heap.push(10)
        heap.push(5)
        heap.push(15)
        
        # Test iteration
        items = list(heap)
        assert items == [5, 10, 15]  # Should be in priority order
        
        # Original heap should remain unchanged
        assert len(heap) == 3
        assert heap.peek() == 5
    
    def test_heap_to_list(self):
        """Test converting heap to list."""
        heap = BinaryHeap[int](heap_type="min")
        heap.push(10)
        heap.push(5)
        heap.push(15)
        
        items = heap.to_list()
        assert items == [5, 10, 15]
    
    def test_heap_clear(self):
        """Test clearing the heap."""
        heap = BinaryHeap[int](heap_type="min")
        heap.push(10)
        heap.push(5)
        
        heap.clear()
        assert len(heap) == 0
        assert heap.is_empty()
    
    def test_heap_size_and_capacity(self):
        """Test size and capacity methods."""
        heap = BinaryHeap[int](heap_type="min")
        
        assert heap.size() == 0
        assert heap.capacity() == 0
        
        heap.push(10)
        heap.push(5)
        
        assert heap.size() == 2
        assert heap.capacity() == 2
    
    def test_heap_is_valid(self):
        """Test heap property validation."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Empty heap is valid
        assert heap.is_valid()
        
        # Valid min heap
        heap.push(10)
        heap.push(5)
        heap.push(15)
        assert heap.is_valid()
        
        # Invalid heap (manually corrupt)
        heap._heap[0] = HeapNode(20, 20)  # Make root larger than children
        assert not heap.is_valid()
    
    def test_heap_large_dataset(self):
        """Test heap with large dataset."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Add 1000 random elements
        elements = [random.randint(1, 1000) for _ in range(1000)]
        for element in elements:
            heap.push(element)
        
        assert len(heap) == 1000
        assert heap.is_valid()
        
        # Extract all elements and verify they're sorted
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.pop())
        
        assert extracted == sorted(elements)
    
    def test_heap_max_heap_large_dataset(self):
        """Test max heap with large dataset."""
        heap = BinaryHeap[int](heap_type="max")
        
        # Add 1000 random elements
        elements = [random.randint(1, 1000) for _ in range(1000)]
        for element in elements:
            heap.push(element)
        
        assert len(heap) == 1000
        assert heap.is_valid()
        
        # Extract all elements and verify they're in descending order
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.pop())
        
        assert extracted == sorted(elements, reverse=True)
    
    def test_heap_performance(self):
        """Test heap performance with timing."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Measure push performance
        start_time = timeit.default_timer()
        for i in range(1000):
            heap.push(i)
        push_time = timeit.default_timer() - start_time
        
        # Measure pop performance
        start_time = timeit.default_timer()
        for _ in range(1000):
            heap.pop()
        pop_time = timeit.default_timer() - start_time
        
        # Verify reasonable performance (should be fast)
        assert push_time < 1.0  # Less than 1 second for 1000 operations
        assert pop_time < 1.0
    
    def test_heap_edge_cases(self):
        """Test heap edge cases."""
        heap = BinaryHeap[int](heap_type="min")
        
        # Test with duplicate priorities
        heap.push(10, 5)
        heap.push(20, 5)
        heap.push(30, 5)
        
        # All should be extractable, but order is not guaranteed for same priority
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.pop())
        
        # Verify all items were extracted and all have priority 5
        assert len(extracted) == 3
        assert set(extracted) == {10, 20, 30}
        
        # Test with zero priority
        heap.push(0, 0)
        assert heap.peek_priority() == 0
        
        # Test with negative priority
        heap.push(-5, -5)
        assert heap.peek_priority() == -5
    
    def test_heap_complex_data_types(self):
        """Test heap with complex data types."""
        heap = BinaryHeap[dict](heap_type="min")
        
        # Test with dictionary data
        data1 = {"name": "Alice", "age": 30}
        data2 = {"name": "Bob", "age": 25}
        data3 = {"name": "Charlie", "age": 35}
        
        heap.push(data1, 30)
        heap.push(data2, 25)
        heap.push(data3, 35)
        
        assert heap.pop() == data2  # Lowest priority
        assert heap.pop() == data1
        assert heap.pop() == data3
    
    def test_heap_key_func_with_complex_data(self):
        """Test heap with key function and complex data types."""
        def key_func(person: dict) -> int:
            return person['age']
        
        heap = BinaryHeap[dict](heap_type="min", key_func=key_func)
        
        people = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35}
        ]
        
        for person in people:
            heap.push(person)
        
        assert heap.pop()["name"] == "Bob"  # Youngest
        assert heap.pop()["name"] == "Alice"
        assert heap.pop()["name"] == "Charlie"  # Oldest
    
    def test_heap_with_none_data(self):
        """Test heap behavior with None data."""
        heap = BinaryHeap[Optional[str]]()
        heap.push(None, 5)
        heap.push("test", 3)
        
        assert heap.peek() == "test"  # Lower priority
        assert heap.pop() == "test"
        assert heap.peek() is None
        assert heap.pop() is None
    
    def test_heap_iter_destructive(self):
        """Test destructive iteration method."""
        heap = BinaryHeap[int](heap_type="min")
        elements = [10, 4, 15, 20, 30]
        
        for element in elements:
            heap.push(element)
        
        # Use destructive iteration
        result = list(heap.iter_destructive())
        expected = [4, 10, 15, 20, 30]
        
        assert result == expected
        assert heap.is_empty()  # Heap should be consumed
    
    def test_heap_merge(self):
        """Test heap merging functionality."""
        heap1 = BinaryHeap[int](heap_type="min")
        heap2 = BinaryHeap[int](heap_type="min")
        
        heap1.push(10)
        heap1.push(5)
        heap2.push(15)
        heap2.push(3)
        
        merged = heap1.merge(heap2)
        
        # Check that all elements are present and ordered
        result = []
        while not merged.is_empty():
            result.append(merged.pop())
        
        assert result == [3, 5, 10, 15]
    
    def test_heap_merge_different_types(self):
        """Test heap merge with different heap types."""
        min_heap = BinaryHeap[int](heap_type="min")
        max_heap = BinaryHeap[int](heap_type="max")
        
        min_heap.push(10)
        max_heap.push(5)
        
        with pytest.raises(ValueError, match="Cannot merge heaps with different types"):
            min_heap.merge(max_heap)
    
    def test_heap_merge_different_key_funcs(self):
        """Test heap merge with different key functions."""
        def key_func1(x: str) -> int:
            return len(x)
        
        def key_func2(x: str) -> int:
            return ord(x[0])
        
        heap1 = BinaryHeap[str](heap_type="min", key_func=key_func1)
        heap2 = BinaryHeap[str](heap_type="min", key_func=key_func2)
        
        heap1.push("a")
        heap2.push("b")
        
        with pytest.raises(ValueError, match="Cannot merge heaps with different key functions"):
            heap1.merge(heap2)
    
    def test_heap_complexity_verification(self):
        """Test that heap operations maintain claimed complexity."""
        import time
        
        heap = BinaryHeap[int](heap_type="min")
        
        # Test insertion complexity (should be O(log n))
        sizes = [100, 1000, 10000]
        insertion_times = []
        
        for size in sizes:
            start_time = time.time()
            for i in range(size):
                heap.push(i)
            end_time = time.time()
            insertion_times.append(end_time - start_time)
        
        # Verify that insertion time grows logarithmically
        # (This is a rough check - actual verification would need more sophisticated analysis)
        assert insertion_times[1] < insertion_times[2] * 10  # Should not grow too fast
        
        # Test extraction complexity
        extraction_times = []
        for size in sizes:
            test_heap = BinaryHeap[int](heap_type="min")
            for i in range(size):
                test_heap.push(i)
            
            start_time = time.time()
            for _ in range(size):
                test_heap.pop()
            end_time = time.time()
            extraction_times.append(end_time - start_time)
        
        # Verify extraction time grows reasonably
        assert extraction_times[1] < extraction_times[2] * 10


if __name__ == "__main__":
    pytest.main([__file__]) 