"""
Unit tests for skip list priority queue implementation.

This module provides comprehensive tests for the SkipListPriorityQueue
class, ensuring correct behavior and edge cases.
"""

import pytest
from src.chapter_05.priority_queue import SkipListPriorityQueue, PriorityItem


class TestPriorityItem:
    """Test cases for PriorityItem."""
    
    def test_priority_item_creation(self):
        """Test basic priority item creation."""
        item = PriorityItem(5, "test")
        assert item.key == 5
        assert item.value == "test"
    
    def test_priority_item_comparison(self):
        """Test priority item comparison."""
        item1 = PriorityItem(1, "high")
        item2 = PriorityItem(5, "low")
        item3 = PriorityItem(1, "high2")
        
        # Lower key = higher priority
        assert item1 < item2
        assert item2 > item1
        assert item1 == item3  # Same key, different value
        assert item1 != item2
    
    def test_priority_item_hash(self):
        """Test priority item hashing."""
        item1 = PriorityItem(1, "test")
        item2 = PriorityItem(1, "test")
        item3 = PriorityItem(2, "test")
        
        assert hash(item1) == hash(item2)
        assert hash(item1) != hash(item3)


class TestSkipListPriorityQueue:
    """Test cases for SkipListPriorityQueue."""
    
    def test_initialization(self):
        """Test priority queue initialization."""
        pq = SkipListPriorityQueue()
        assert len(pq) == 0
        assert len(pq._item_map) == 0
    
    def test_put_and_get(self):
        """Test basic put and get operations."""
        pq = SkipListPriorityQueue()
        
        # Add items
        pq.put(3, "task3")
        pq.put(1, "task1")
        pq.put(2, "task2")
        
        assert len(pq) == 3
        
        # Get items in priority order
        priority, value = pq.get()
        assert priority == 1
        assert value == "task1"
        
        priority, value = pq.get()
        assert priority == 2
        assert value == "task2"
        
        priority, value = pq.get()
        assert priority == 3
        assert value == "task3"
        
        assert len(pq) == 0
    
    def test_peek(self):
        """Test peek operation."""
        pq = SkipListPriorityQueue()
        
        # Add items
        pq.put(3, "task3")
        pq.put(1, "task1")
        pq.put(2, "task2")
        
        # Peek at highest priority item
        priority, value = pq.peek()
        assert priority == 1
        assert value == "task1"
        
        # Queue should still have all items
        assert len(pq) == 3
    
    def test_peek_empty_queue(self):
        """Test peek on empty queue."""
        pq = SkipListPriorityQueue()
        
        with pytest.raises(IndexError):
            pq.peek()
    
    def test_get_empty_queue(self):
        """Test get on empty queue."""
        pq = SkipListPriorityQueue()
        
        with pytest.raises(IndexError):
            pq.get()
    
    def test_duplicate_values(self):
        """Test handling of duplicate values."""
        pq = SkipListPriorityQueue()
        
        # Add same value with different priorities
        pq.put(3, "task")
        pq.put(1, "task")  # Should replace the previous one
        
        assert len(pq) == 1
        
        priority, value = pq.get()
        assert priority == 1
        assert value == "task"
    
    def test_remove(self):
        """Test remove operation."""
        pq = SkipListPriorityQueue()
        
        # Add items
        pq.put(3, "task3")
        pq.put(1, "task1")
        pq.put(2, "task2")
        
        # Remove existing item
        assert pq.remove("task2") is True
        assert len(pq) == 2
        
        # Remove non-existing item
        assert pq.remove("nonexistent") is False
        assert len(pq) == 2
        
        # Get remaining items
        priority, value = pq.get()
        assert priority == 1
        assert value == "task1"
        
        priority, value = pq.get()
        assert priority == 3
        assert value == "task3"
    
    def test_update_priority(self):
        """Test priority update operation."""
        pq = SkipListPriorityQueue()
        
        # Add item
        pq.put(3, "task")
        
        # Update priority
        assert pq.update_priority("task", 1) is True
        assert len(pq) == 1
        
        # Get item with new priority
        priority, value = pq.get()
        assert priority == 1
        assert value == "task"
    
    def test_update_priority_nonexistent(self):
        """Test updating priority of non-existing item."""
        pq = SkipListPriorityQueue()
        
        assert pq.update_priority("nonexistent", 1) is False
    
    def test_contains(self):
        """Test contains operation."""
        pq = SkipListPriorityQueue()
        
        pq.put(1, "task1")
        pq.put(2, "task2")
        
        assert "task1" in pq
        assert "task2" in pq
        assert "task3" not in pq
    
    def test_iteration(self):
        """Test iteration over priority queue."""
        pq = SkipListPriorityQueue()
        
        # Add items in random order
        pq.put(3, "task3")
        pq.put(1, "task1")
        pq.put(2, "task2")
        
        # Iteration should return items in priority order
        items = list(pq)
        assert items == [(1, "task1"), (2, "task2"), (3, "task3")]
    
    def test_get_priority(self):
        """Test getting priority of specific value."""
        pq = SkipListPriorityQueue()
        
        pq.put(3, "task3")
        pq.put(1, "task1")
        pq.put(2, "task2")
        
        assert pq.get_priority("task1") == 1
        assert pq.get_priority("task2") == 2
        assert pq.get_priority("task3") == 3
        assert pq.get_priority("nonexistent") is None
    
    def test_repr(self):
        """Test string representation."""
        pq = SkipListPriorityQueue()
        pq.put(1, "task1")
        pq.put(2, "task2")
        
        expected = "SkipListPriorityQueue([(1, 'task1'), (2, 'task2')])"
        assert repr(pq) == expected
    
    def test_large_dataset(self):
        """Test with larger dataset."""
        pq = SkipListPriorityQueue()
        
        # Add 1000 items with sequential priorities to ensure uniqueness
        import random
        random.seed(42)
        
        for i in range(1000):
            priority = i + 1  # Use sequential priorities to ensure uniqueness
            pq.put(priority, f"task{i}")  # Use unique task names
        
        assert len(pq) == 1000
        
        # Get items and verify they're in priority order
        last_priority = 0
        for priority, value in pq:
            assert priority >= last_priority
            last_priority = priority
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        pq = SkipListPriorityQueue()
        
        # Test with negative priorities
        pq.put(-1, "negative")
        pq.put(0, "zero")
        pq.put(1, "positive")
        
        priority, value = pq.get()
        assert priority == -1
        assert value == "negative"
        
        # Test with very large priorities
        pq.put(1000000, "large")
        priority, value = pq.get()
        assert priority == 0
        assert value == "zero"
        
        # Test with empty string values
        pq.put(1, "")
        assert "" in pq
        assert pq.get_priority("") == 1
    
    def test_priority_update_removes_old(self):
        """Test that priority update removes old item."""
        pq = SkipListPriorityQueue()
        
        pq.put(3, "task")
        pq.put(1, "task")  # Should replace the previous one
        
        assert len(pq) == 1
        priority, value = pq.get()
        assert priority == 1
        assert value == "task"
    
    def test_multiple_operations(self):
        """Test complex sequence of operations."""
        pq = SkipListPriorityQueue()
        
        # Add items
        pq.put(5, "task5")
        pq.put(1, "task1")
        pq.put(3, "task3")
        
        # Peek
        priority, value = pq.peek()
        assert priority == 1
        assert value == "task1"
        
        # Update priority
        pq.update_priority("task5", 0)
        
        # Get highest priority
        priority, value = pq.get()
        assert priority == 0
        assert value == "task5"
        
        # Remove item
        pq.remove("task3")
        
        # Get remaining item
        priority, value = pq.get()
        assert priority == 1
        assert value == "task1"
        
        assert len(pq) == 0


if __name__ == "__main__":
    pytest.main([__file__]) 