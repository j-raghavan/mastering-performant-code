"""
Tests for Priority Queue Implementation

This module provides comprehensive tests for the PriorityQueue class,
ensuring 100% code coverage and correct behavior.
"""

import pytest
import time
from typing import List, Optional
from mastering_performant_code.chapter_11.priority_queue import PriorityQueue, PriorityQueueItem


class TestPriorityQueueItem:
    """Test cases for PriorityQueueItem class."""
    
    def test_priority_queue_item_creation(self):
        """Test PriorityQueueItem creation."""
        item = PriorityQueueItem(10, 1, "test_data")
        assert item.priority == 10
        assert item.counter == 1
        assert item.data == "test_data"
    
    def test_priority_queue_item_repr(self):
        """Test PriorityQueueItem string representation."""
        item = PriorityQueueItem(5, 2, "test")
        assert repr(item) == "PriorityQueueItem(5, test)"


class TestPriorityQueue:
    """Test cases for PriorityQueue class."""
    
    def test_priority_queue_initialization(self):
        """Test priority queue initialization."""
        # Test min heap (default)
        pq_min = PriorityQueue[str]()
        assert pq_min._heap._heap_type == "min"
        
        # Test max heap
        pq_max = PriorityQueue[str](max_heap=True)
        assert pq_max._heap._heap_type == "min"  # Always min-heap, key function handles ordering
    
    def test_priority_queue_basic_operations(self):
        """Test basic priority queue operations."""
        pq = PriorityQueue[str]()
        
        # Test empty queue
        assert len(pq) == 0
        assert pq.is_empty()
        
        # Test put and get
        pq.put("task1", 5)
        pq.put("task2", 3)
        pq.put("task3", 7)
        
        assert len(pq) == 3
        assert not pq.is_empty()
        
        # Test get in priority order (min heap)
        assert pq.get() == "task2"  # Lowest priority
        assert pq.get() == "task1"
        assert pq.get() == "task3"
        assert pq.is_empty()
    
    def test_priority_queue_max_heap(self):
        """Test priority queue with max heap."""
        pq = PriorityQueue[str](max_heap=True)
        
        pq.put("task1", 5)
        pq.put("task2", 3)
        pq.put("task3", 7)
        
        # Test get in priority order (max heap - higher priorities first)
        assert pq.get() == "task3"  # Highest priority
        assert pq.get() == "task1"  # Medium priority
        assert pq.get() == "task2"  # Lowest priority
    
    def test_priority_queue_with_key_func(self):
        """Test priority queue with key function."""
        def key_func(x: str) -> int:
            return len(x)
        
        pq = PriorityQueue[str](key_func=key_func)
        
        pq.put("a")  # length 1
        pq.put("bb")  # length 2
        pq.put("ccc")  # length 3
        
        assert pq.get() == "a"  # Shortest string
        assert pq.get() == "bb"
        assert pq.get() == "ccc"
    
    def test_priority_queue_numeric_items(self):
        """Test priority queue with numeric items."""
        pq = PriorityQueue[int]()
        
        pq.put(10)
        pq.put(5)
        pq.put(15)
        
        assert pq.get() == 5
        assert pq.get() == 10
        assert pq.get() == 15
    
    def test_priority_queue_non_numeric_no_priority(self):
        """Test priority queue with non-numeric items without priority."""
        pq = PriorityQueue[str]()
        
        with pytest.raises(ValueError, match="Must provide priority or key_func"):
            pq.put("test")
    
    def test_priority_queue_peek(self):
        """Test peek operations."""
        pq = PriorityQueue[str]()
        
        # Test peek on empty queue
        with pytest.raises(IndexError, match="Priority queue is empty"):
            pq.peek()
        
        # Test peek with elements
        pq.put("task1", 5)
        pq.put("task2", 3)
        
        assert pq.peek() == "task2"  # Lowest priority
        assert len(pq) == 2  # Peek doesn't remove elements
    
    def test_priority_queue_peek_priority(self):
        """Test peek_priority operations."""
        pq = PriorityQueue[str]()
        
        # Test peek_priority on empty queue
        with pytest.raises(IndexError, match="Priority queue is empty"):
            pq.peek_priority()
        
        # Test peek_priority with elements
        pq.put("task1", 5)
        pq.put("task2", 3)
        
        assert pq.peek_priority() == 3
        assert len(pq) == 2  # Peek doesn't remove elements
    
    def test_priority_queue_fifo_ordering(self):
        """Test FIFO ordering for items with same priority."""
        pq = PriorityQueue[str]()
        
        # Add items with same priority but different timestamps
        pq.put("task1", 5)
        time.sleep(0.001)  # Ensure different timestamps
        pq.put("task2", 5)
        time.sleep(0.001)
        pq.put("task3", 5)
        
        # Items should be extracted in FIFO order for same priority
        assert pq.get() == "task1"
        assert pq.get() == "task2"
        assert pq.get() == "task3"
    
    def test_priority_queue_repr(self):
        """Test priority queue string representation."""
        pq = PriorityQueue[str]()
        pq.put("task1", 5)
        pq.put("task2", 3)
        
        assert repr(pq) == "PriorityQueue(2 items)"
    
    def test_priority_queue_iteration(self):
        """Test priority queue iteration."""
        pq = PriorityQueue[str]()
        pq.put("task1", 5)
        pq.put("task2", 3)
        pq.put("task3", 7)
        
        # Test iteration
        items = list(pq)
        assert len(items) == 3
        assert "task1" in items
        assert "task2" in items
        assert "task3" in items
        
        # Original queue should remain unchanged
        assert len(pq) == 3
    
    def test_priority_queue_to_list(self):
        """Test converting priority queue to list."""
        pq = PriorityQueue[str]()
        pq.put("task1", 5)
        pq.put("task2", 3)
        pq.put("task3", 7)
        
        items = pq.to_list()
        assert len(items) == 3
        assert "task1" in items
        assert "task2" in items
        assert "task3" in items
    
    def test_priority_queue_clear(self):
        """Test clearing the priority queue."""
        pq = PriorityQueue[str]()
        pq.put("task1", 5)
        pq.put("task2", 3)
        
        pq.clear()
        assert len(pq) == 0
        assert pq.is_empty()
    
    def test_priority_queue_size(self):
        """Test priority queue size method."""
        pq = PriorityQueue[str]()
        
        assert pq.size() == 0
        
        pq.put("task1", 5)
        pq.put("task2", 3)
        
        assert pq.size() == 2
    
    def test_priority_queue_is_valid(self):
        """Test priority queue validity check."""
        pq = PriorityQueue[str]()
        
        # Empty queue is valid
        assert pq.is_valid()
        
        # Queue with elements is valid
        pq.put("task1", 5)
        pq.put("task2", 3)
        assert pq.is_valid()
    
    def test_priority_queue_get_all_with_priority(self):
        """Test getting all items with a specific priority."""
        pq = PriorityQueue[str]()
        
        pq.put("task1", 5)
        pq.put("task2", 3)
        pq.put("task3", 5)
        pq.put("task4", 7)
        pq.put("task5", 3)
        
        # Get all items with priority 3
        priority_3_items = pq.get_all_with_priority(3)
        assert set(priority_3_items) == {"task2", "task5"}
        
        # Get all items with priority 5
        priority_5_items = pq.get_all_with_priority(5)
        assert set(priority_5_items) == {"task1", "task3"}
        
        # Get all items with priority 7
        priority_7_items = pq.get_all_with_priority(7)
        assert set(priority_7_items) == {"task4"}
        
        # Queue should still have all items
        assert len(pq) == 5
    
    def test_priority_queue_remove_all_with_priority(self):
        """Test removing all items with a specific priority."""
        pq = PriorityQueue[str]()
        
        pq.put("task1", 5)
        pq.put("task2", 3)
        pq.put("task3", 5)
        pq.put("task4", 7)
        pq.put("task5", 3)
        
        # Remove all items with priority 3
        removed = pq.remove_all_with_priority(3)
        assert set(removed) == {"task2", "task5"}
        assert len(pq) == 3
        
        # Remove all items with priority 5
        removed = pq.remove_all_with_priority(5)
        assert set(removed) == {"task1", "task3"}
        assert len(pq) == 1
        
        # Only task4 should remain
        assert pq.get() == "task4"
        assert pq.is_empty()
    
    def test_priority_queue_get_priority_distribution(self):
        """Test getting priority distribution."""
        pq = PriorityQueue[str](max_heap=True)
        
        pq.put("task1", 5)
        pq.put("task2", 5)
        pq.put("task3", 10)
        pq.put("task4", 3)
        
        distribution = pq.get_priority_distribution()
        expected = {5: 2, 10: 1, 3: 1}
        
        assert distribution == expected
    
    def test_priority_queue_task_done(self):
        """Test task_done method (should not raise any errors)."""
        pq = PriorityQueue[str]()
        pq.put("task1", 5)
        
        # task_done should not raise any errors
        pq.task_done()
        assert True  # If we get here, no exception was raised
    
    def test_priority_queue_qsize(self):
        """Test qsize method."""
        pq = PriorityQueue[str]()
        
        assert pq.qsize() == 0
        
        pq.put("task1", 5)
        assert pq.qsize() == 1
        
        pq.put("task2", 3)
        assert pq.qsize() == 2
        
        pq.get()
        assert pq.qsize() == 1
    
    def test_priority_queue_full(self):
        """Test full method (should always return False)."""
        pq = PriorityQueue[str]()
        
        assert pq.full() is False
        
        # Even after adding many items, it should still not be full
        for i in range(100):
            pq.put(f"task{i}", i)
        
        assert pq.full() is False
    
    def test_priority_queue_empty(self):
        """Test empty method."""
        pq = PriorityQueue[str]()
        
        assert pq.empty() is True
        
        pq.put("task1", 5)
        assert pq.empty() is False
        
        pq.get()
        assert pq.empty() is True
    
    def test_priority_queue_edge_cases(self):
        """Test priority queue with edge cases."""
        pq = PriorityQueue[Optional[str]]()
        
        # Test with None data
        pq.put(None, 5)
        assert pq.peek() is None
        
        # Test with zero priority
        pq.put("zero", 0)
        assert pq.peek() == "zero"  # Should be first in min-heap
        
        # Test with negative priority
        pq.put("negative", -1)
        assert pq.peek() == "negative"  # Should be first in min-heap
    
    def test_priority_queue_custom_objects(self):
        """Test priority queue with custom objects that don't implement comparison."""
        class Task:
            def __init__(self, name: str, priority: int):
                self.name = name
                self.priority = priority
            
            def __repr__(self):
                return f"Task({self.name})"
        
        pq = PriorityQueue[Task]()
        
        task1 = Task("task1", 5)
        task2 = Task("task2", 3)
        
        pq.put(task1, 5)
        pq.put(task2, 3)
        
        # Should get task2 first (lower priority in min-heap)
        assert pq.get() == task2
        assert pq.get() == task1
    
    def test_priority_queue_large_dataset(self):
        """Test priority queue with large dataset."""
        pq = PriorityQueue[int]()
        
        # Add 1000 items with random priorities
        import random
        items = [(i, random.randint(1, 100)) for i in range(1000)]
        
        for item, priority in items:
            pq.put(item, priority)
        
        assert len(pq) == 1000
        
        # Extract all items and verify they're in priority order
        extracted = []
        extracted_priorities = []
        while not pq.is_empty():
            val = pq.get()
            extracted.append(val)
        
        # Map item to priority for verification
        item_to_priority = dict(items)
        extracted_priorities = [item_to_priority[x] for x in extracted]
        
        # Priorities should be non-decreasing
        assert all(extracted_priorities[i] <= extracted_priorities[i+1] for i in range(len(extracted_priorities)-1))
        assert len(extracted) == 1000


if __name__ == "__main__":
    pytest.main([__file__]) 