"""
Unit tests for skip list implementation.

This module provides comprehensive tests for the SkipList and SkipListWithStats
classes, ensuring 100% code coverage and correct behavior.
"""

import pytest
import random
from typing import List
from chapter_05.skip_list import SkipList, SkipListWithStats, SkipListNode


class TestSkipListNode:
    """Test cases for SkipListNode."""
    
    def test_node_creation(self):
        """Test basic node creation."""
        node = SkipListNode(42, [None, None], 2)
        assert node.data == 42
        assert node.height == 2
        assert len(node.forward) == 2
        assert all(ptr is None for ptr in node.forward)
    
    def test_node_post_init(self):
        """Test post_init method adjusts forward list."""
        node = SkipListNode(42, [None], 3)
        assert len(node.forward) == 3
        assert all(ptr is None for ptr in node.forward)
    
    def test_node_repr(self):
        """Test string representation."""
        node = SkipListNode(42, [None], 1)
        assert repr(node) == "SkipListNode(42, height=1)"


class TestSkipList:
    """Test cases for SkipList."""
    
    def test_initialization(self):
        """Test skip list initialization."""
        skip_list = SkipList()
        assert skip_list.max_height == 16
        assert skip_list.probability == 0.5
        assert skip_list.size == 0
        assert skip_list.current_max_height == 1
        assert skip_list.head.data is None
        assert len(skip_list.head.forward) == 16
    
    def test_initialization_custom_params(self):
        """Test skip list initialization with custom parameters."""
        skip_list = SkipList(max_height=8, probability=0.25)
        assert skip_list.max_height == 8
        assert skip_list.probability == 0.25
        assert len(skip_list.head.forward) == 8
    
    def test_random_height(self):
        """Test random height generation."""
        skip_list = SkipList(max_height=4, probability=0.5)
        heights = set()
        for _ in range(100):
            height = skip_list._random_height()
            assert 1 <= height <= 4
            heights.add(height)
        # Should generate different heights
        assert len(heights) > 1
    
    def test_empty_list_operations(self):
        """Test operations on empty skip list."""
        skip_list = SkipList()
        
        # Search should return None
        assert skip_list.search(42) is None
        
        # Delete should return False
        assert skip_list.delete(42) is False
        
        # Length should be 0
        assert len(skip_list) == 0
        
        # Should not contain any element
        assert 42 not in skip_list
        
        # Iterator should be empty
        assert list(skip_list) == []
    
    def test_insert_and_search(self):
        """Test insert and search operations."""
        skip_list = SkipList()
        
        # Insert elements
        elements = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]
        for element in elements:
            skip_list.insert(element)
        
        # Check size
        assert len(skip_list) == len(elements)
        
        # Search for existing elements
        for element in elements:
            assert skip_list.search(element) == element
            assert element in skip_list
        
        # Search for non-existing elements
        non_existing = [1, 2, 4, 5, 8, 10, 11, 13, 14, 15, 16, 18, 20, 22, 23, 24, 27, 28, 29, 30]
        for element in non_existing:
            assert skip_list.search(element) is None
            assert element not in skip_list
    
    def test_insert_duplicates(self):
        """Test inserting duplicate elements."""
        skip_list = SkipList()
        
        # Insert same element multiple times
        skip_list.insert(42)
        skip_list.insert(42)
        skip_list.insert(42)
        
        # Should only have one element
        assert len(skip_list) == 1
        assert skip_list.search(42) == 42
    
    def test_delete_operations(self):
        """Test delete operations."""
        skip_list = SkipList()
        
        # Insert elements
        elements = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]
        for element in elements:
            skip_list.insert(element)
        
        # Delete existing elements
        to_delete = [7, 19, 25]
        for element in to_delete:
            assert skip_list.delete(element) is True
            assert skip_list.search(element) is None
            assert element not in skip_list
        
        # Check size
        assert len(skip_list) == len(elements) - len(to_delete)
        
        # Delete non-existing elements
        assert skip_list.delete(999) is False
    
    def test_delete_all_elements(self):
        """Test deleting all elements."""
        skip_list = SkipList()
        
        # Insert elements
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            skip_list.insert(element)
        
        # Delete all elements
        for element in elements:
            assert skip_list.delete(element) is True
        
        # Check empty state
        assert len(skip_list) == 0
        assert list(skip_list) == []
        assert skip_list.current_max_height == 1
    
    def test_iteration(self):
        """Test iteration over skip list."""
        skip_list = SkipList()
        
        # Insert elements in random order
        elements = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]
        random.shuffle(elements)
        for element in elements:
            skip_list.insert(element)
        
        # Iteration should return elements in sorted order
        sorted_elements = sorted(elements)
        assert list(skip_list) == sorted_elements
    
    def test_range_query(self):
        """Test range query operations."""
        skip_list = SkipList()
        
        # Insert elements
        elements = list(range(20))
        for element in elements:
            skip_list.insert(element)
        
        # Test various ranges
        assert list(skip_list.range_query(5, 10)) == [5, 6, 7, 8, 9]
        assert list(skip_list.range_query(0, 5)) == [0, 1, 2, 3, 4]
        assert list(skip_list.range_query(15, 20)) == [15, 16, 17, 18, 19]
        assert list(skip_list.range_query(10, 10)) == []  # Empty range
        assert list(skip_list.range_query(25, 30)) == []  # No elements in range
    
    def test_level_distribution(self):
        """Test level distribution calculation."""
        skip_list = SkipList(max_height=4)
        
        # Insert elements
        for i in range(10):
            skip_list.insert(i)
        
        distribution = skip_list.get_level_distribution()
        
        # Should have distribution for each level
        assert len(distribution) == 4
        
        # All nodes should be at level 1 or higher
        assert distribution[0] > 0
        
        # Total should equal number of elements
        assert sum(distribution) == 10
    
    def test_max_height_update(self):
        """Test that max height updates correctly."""
        skip_list = SkipList(max_height=4, probability=1.0)  # Always increase height
        
        # Insert elements to trigger height increases
        for i in range(10):
            skip_list.insert(i)
        
        # Max height should have increased
        assert skip_list.current_max_height > 1
    
    def test_repr(self):
        """Test string representation."""
        skip_list = SkipList()
        skip_list.insert(1)
        skip_list.insert(2)
        skip_list.insert(3)
        
        assert repr(skip_list) == "SkipList([1, 2, 3])"
    
    def test_large_dataset(self):
        """Test with larger dataset."""
        skip_list = SkipList()
        
        # Insert 1000 elements
        elements = list(range(1000))
        random.shuffle(elements)
        
        for element in elements:
            skip_list.insert(element)
        
        assert len(skip_list) == 1000
        
        # Test search operations
        for i in range(0, 1000, 100):
            assert skip_list.search(i) == i
        
        # Test range queries
        range_result = list(skip_list.range_query(100, 200))
        assert len(range_result) == 100
        assert range_result == list(range(100, 200))
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        skip_list = SkipList(max_height=2)
        
        # Test with maximum height constraint
        for i in range(100):
            skip_list.insert(i)
        
        # All nodes should have height <= 2
        current = skip_list.head.forward[0]
        while current is not None:
            assert current.height <= 2
            current = current.forward[0]
        
        # Test with probability 0 (all nodes height 1)
        skip_list = SkipList(max_height=4, probability=0.0)
        for i in range(10):
            skip_list.insert(i)
        
        distribution = skip_list.get_level_distribution()
        assert distribution[0] == 10  # All nodes at level 1
        assert sum(distribution[1:]) == 0  # No nodes at higher levels


class TestSkipListWithStats:
    """Test cases for SkipListWithStats."""
    
    def test_initialization(self):
        """Test initialization with statistics."""
        skip_list = SkipListWithStats()
        assert skip_list.skip_list is not None
        assert 'searches' in skip_list.stats
        assert 'inserts' in skip_list.stats
        assert 'deletes' in skip_list.stats
    
    def test_search_with_stats(self):
        """Test search operation with statistics tracking."""
        skip_list = SkipListWithStats()
        skip_list.insert(42)
        
        # Perform search
        result = skip_list.search(42)
        
        assert result == 42
        assert skip_list.stats['searches'] == 1
        assert skip_list.stats['search_time'] > 0
    
    def test_insert_with_stats(self):
        """Test insert operation with statistics tracking."""
        skip_list = SkipListWithStats()
        
        # Perform insert
        skip_list.insert(42)
        
        assert skip_list.stats['inserts'] == 1
        assert skip_list.stats['insert_time'] > 0
        assert 42 in skip_list.skip_list
    
    def test_delete_with_stats(self):
        """Test delete operation with statistics tracking."""
        skip_list = SkipListWithStats()
        skip_list.insert(42)
        
        # Perform delete
        result = skip_list.delete(42)
        
        assert result is True
        assert skip_list.stats['deletes'] == 1
        assert skip_list.stats['delete_time'] > 0
    
    def test_get_stats(self):
        """Test statistics retrieval."""
        skip_list = SkipListWithStats()
        
        # Perform some operations
        skip_list.insert(1)
        skip_list.insert(2)
        skip_list.search(1)
        skip_list.delete(1)
        
        stats = skip_list.get_stats()
        
        assert stats['inserts'] == 2
        assert stats['searches'] == 1
        assert stats['deletes'] == 1
        assert 'avg_insert_time' in stats
        assert 'avg_search_time' in stats
        assert 'avg_delete_time' in stats
        assert 'level_distribution' in stats
    
    def test_reset_stats(self):
        """Test statistics reset."""
        skip_list = SkipListWithStats()
        
        # Perform some operations
        skip_list.insert(1)
        skip_list.search(1)
        
        # Reset stats
        skip_list.reset_stats()
        
        assert skip_list.stats['inserts'] == 0
        assert skip_list.stats['searches'] == 0
        assert skip_list.stats['deletes'] == 0
        assert skip_list.stats['search_time'] == 0.0
        assert skip_list.stats['insert_time'] == 0.0
        assert skip_list.stats['delete_time'] == 0.0
    
    def test_delegation_methods(self):
        """Test that delegation methods work correctly."""
        skip_list = SkipListWithStats()
        
        # Test len
        skip_list.insert(1)
        skip_list.insert(2)
        assert len(skip_list) == 2
        
        # Test contains
        assert 1 in skip_list
        assert 3 not in skip_list
        
        # Test iteration
        assert list(skip_list) == [1, 2]
        
        # Test range query
        skip_list.insert(3)
        assert list(skip_list.range_query(1, 3)) == [1, 2]
        
        # Test repr
        assert repr(skip_list) == "SkipList([1, 2, 3])"


class TestSkipListPerformance:
    """Test cases for performance characteristics."""
    
    def test_search_performance(self):
        """Test that search performance is reasonable."""
        skip_list = SkipList()
        
        # Insert elements
        for i in range(1000):
            skip_list.insert(i)
        
        # Time search operations
        import time
        start_time = time.perf_counter()
        
        for i in range(100):
            skip_list.search(i * 10)
        
        end_time = time.perf_counter()
        search_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        assert search_time < 1.0
    
    def test_insert_performance(self):
        """Test that insert performance is reasonable."""
        skip_list = SkipList()
        
        # Time insert operations
        import time
        start_time = time.perf_counter()
        
        for i in range(1000):
            skip_list.insert(i)
        
        end_time = time.perf_counter()
        insert_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        assert insert_time < 1.0
        assert len(skip_list) == 1000
    
    def test_memory_usage(self):
        """Test that memory usage is reasonable."""
        skip_list = SkipList()
        
        # Insert elements
        for i in range(1000):
            skip_list.insert(i)
        
        # Check memory usage
        memory_size = sys.getsizeof(skip_list)
        
        # Should use reasonable amount of memory (less than 1MB)
        assert memory_size < 1024 * 1024


if __name__ == "__main__":
    pytest.main([__file__]) 