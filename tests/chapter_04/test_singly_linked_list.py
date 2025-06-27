"""
Unit tests for SinglyLinkedList implementation.

This module provides comprehensive tests for the SinglyLinkedList class,
ensuring 100% code coverage and testing all edge cases.
"""

import pytest
from typing import List

from chapter_04.singly_linked_list import SinglyLinkedList
from chapter_04.nodes import SinglyNode


class TestSinglyLinkedList:
    """Test cases for SinglyLinkedList class."""
    
    def test_init(self):
        """Test initialization of SinglyLinkedList."""
        sll = SinglyLinkedList()
        assert len(sll) == 0
        assert sll.is_empty()
        assert sll._head_sentinel.next == sll._tail_sentinel
        assert sll._size == 0
    
    def test_append_single_element(self):
        """Test appending a single element."""
        sll = SinglyLinkedList()
        sll.append(42)
        
        assert len(sll) == 1
        assert not sll.is_empty()
        assert sll.get_at_index(0) == 42
    
    def test_append_multiple_elements(self):
        """Test appending multiple elements."""
        sll = SinglyLinkedList()
        elements = [1, 2, 3, 4, 5]
        
        for element in elements:
            sll.append(element)
        
        assert len(sll) == len(elements)
        for i, element in enumerate(elements):
            assert sll.get_at_index(i) == element
    
    def test_prepend_single_element(self):
        """Test prepending a single element."""
        sll = SinglyLinkedList()
        sll.prepend(42)
        
        assert len(sll) == 1
        assert sll.get_at_index(0) == 42
    
    def test_prepend_multiple_elements(self):
        """Test prepending multiple elements."""
        sll = SinglyLinkedList()
        elements = [1, 2, 3, 4, 5]
        
        for element in elements:
            sll.prepend(element)
        
        assert len(sll) == len(elements)
        # Elements should be in reverse order due to prepending
        for i, element in enumerate(reversed(elements)):
            assert sll.get_at_index(i) == element
    
    def test_insert_after_success(self):
        """Test successful insert_after operation."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(30)
        
        result = sll.insert_after(20, 25)
        assert result is True
        assert len(sll) == 4
        assert sll.get_at_index(2) == 25
        assert sll.get_at_index(3) == 30
    
    def test_insert_after_not_found(self):
        """Test insert_after when target is not found."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        
        result = sll.insert_after(30, 25)
        assert result is False
        assert len(sll) == 2
    
    def test_insert_after_empty_list(self):
        """Test insert_after on empty list."""
        sll = SinglyLinkedList()
        result = sll.insert_after(10, 20)
        assert result is False
        assert len(sll) == 0
    
    def test_delete_first_success(self):
        """Test successful delete_first operation."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(30)
        
        result = sll.delete_first(20)
        assert result is True
        assert len(sll) == 2
        assert sll.get_at_index(0) == 10
        assert sll.get_at_index(1) == 30
    
    def test_delete_first_not_found(self):
        """Test delete_first when element is not found."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        
        result = sll.delete_first(30)
        assert result is False
        assert len(sll) == 2
    
    def test_delete_first_empty_list(self):
        """Test delete_first on empty list."""
        sll = SinglyLinkedList()
        result = sll.delete_first(10)
        assert result is False
        assert len(sll) == 0
    
    def test_delete_first_duplicate_elements(self):
        """Test delete_first with duplicate elements."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(20)
        sll.append(30)
        
        result = sll.delete_first(20)
        assert result is True
        assert len(sll) == 3
        assert sll.get_at_index(1) == 20  # Second occurrence remains
        assert sll.get_at_index(2) == 30
    
    def test_get_at_index_valid(self):
        """Test get_at_index with valid indices."""
        sll = SinglyLinkedList()
        elements = [10, 20, 30, 40, 50]
        for element in elements:
            sll.append(element)
        
        for i, element in enumerate(elements):
            assert sll.get_at_index(i) == element
    
    def test_get_at_index_invalid(self):
        """Test get_at_index with invalid indices."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        
        with pytest.raises(IndexError):
            sll.get_at_index(-1)
        
        with pytest.raises(IndexError):
            sll.get_at_index(2)
        
        with pytest.raises(IndexError):
            sll.get_at_index(100)
    
    def test_get_at_index_empty_list(self):
        """Test get_at_index on empty list."""
        sll = SinglyLinkedList()
        with pytest.raises(IndexError):
            sll.get_at_index(0)
    
    def test_set_at_index_valid(self):
        """Test set_at_index with valid indices."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(30)
        
        sll.set_at_index(1, 25)
        assert sll.get_at_index(1) == 25
        assert sll.get_at_index(0) == 10
        assert sll.get_at_index(2) == 30
    
    def test_set_at_index_invalid(self):
        """Test set_at_index with invalid indices."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        
        with pytest.raises(IndexError):
            sll.set_at_index(-1, 30)
        
        with pytest.raises(IndexError):
            sll.set_at_index(2, 30)
    
    def test_iteration(self):
        """Test iteration over the list."""
        sll = SinglyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            sll.append(element)
        
        result = list(sll)
        assert result == elements
    
    def test_iteration_empty(self):
        """Test iteration over empty list."""
        sll = SinglyLinkedList()
        result = list(sll)
        assert result == []
    
    def test_repr(self):
        """Test string representation."""
        sll = SinglyLinkedList()
        assert repr(sll) == "SinglyLinkedList([])"
        
        sll.append(10)
        sll.append(20)
        assert repr(sll) == "SinglyLinkedList([10, 20])"
    
    def test_to_list(self):
        """Test conversion to Python list."""
        sll = SinglyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            sll.append(element)
        
        result = sll.to_list()
        assert result == elements
        assert isinstance(result, list)
    
    def test_reverse_empty(self):
        """Test reverse on empty list."""
        sll = SinglyLinkedList()
        sll.reverse()
        assert len(sll) == 0
        assert sll.is_empty()
    
    def test_reverse_single_element(self):
        """Test reverse on single element list."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.reverse()
        assert len(sll) == 1
        assert sll.get_at_index(0) == 10
    
    def test_reverse_multiple_elements(self):
        """Test reverse on multiple elements."""
        sll = SinglyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            sll.append(element)
        
        sll.reverse()
        reversed_elements = list(reversed(elements))
        
        for i, element in enumerate(reversed_elements):
            assert sll.get_at_index(i) == element
    
    def test_contains_true(self):
        """Test contains with existing element."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(30)
        
        assert sll.contains(20) is True
        assert sll.contains(10) is True
        assert sll.contains(30) is True
    
    def test_contains_false(self):
        """Test contains with non-existing element."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        
        assert sll.contains(30) is False
        assert sll.contains(0) is False
    
    def test_contains_empty(self):
        """Test contains on empty list."""
        sll = SinglyLinkedList()
        assert sll.contains(10) is False
    
    def test_count_single_occurrence(self):
        """Test count with single occurrence."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(30)
        
        assert sll.count(20) == 1
        assert sll.count(10) == 1
        assert sll.count(30) == 1
    
    def test_count_multiple_occurrences(self):
        """Test count with multiple occurrences."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(20)
        sll.append(30)
        sll.append(20)
        
        assert sll.count(20) == 3
        assert sll.count(10) == 1
        assert sll.count(30) == 1
    
    def test_count_not_found(self):
        """Test count with non-existing element."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        
        assert sll.count(30) == 0
        assert sll.count(0) == 0
    
    def test_count_empty(self):
        """Test count on empty list."""
        sll = SinglyLinkedList()
        assert sll.count(10) == 0
    
    def test_clear(self):
        """Test clearing the list."""
        sll = SinglyLinkedList()
        sll.append(10)
        sll.append(20)
        sll.append(30)
        
        sll.clear()
        assert len(sll) == 0
        assert sll.is_empty()
        assert sll._head_sentinel.next == sll._tail_sentinel
    
    def test_clear_empty(self):
        """Test clearing an empty list."""
        sll = SinglyLinkedList()
        sll.clear()
        assert len(sll) == 0
        assert sll.is_empty()
    
    def test_mixed_operations(self):
        """Test mixed operations on the list."""
        sll = SinglyLinkedList()
        
        # Append and prepend
        sll.append(10)
        sll.prepend(5)
        sll.append(20)
        sll.prepend(1)
        
        assert len(sll) == 4
        assert sll.get_at_index(0) == 1
        assert sll.get_at_index(1) == 5
        assert sll.get_at_index(2) == 10
        assert sll.get_at_index(3) == 20
        
        # Insert and delete
        sll.insert_after(5, 7)
        sll.delete_first(10)
        
        assert len(sll) == 4
        assert sll.get_at_index(0) == 1
        assert sll.get_at_index(1) == 5
        assert sll.get_at_index(2) == 7
        assert sll.get_at_index(3) == 20
        
        # Set and get
        sll.set_at_index(2, 8)
        assert sll.get_at_index(2) == 8
        
        # Reverse
        sll.reverse()
        assert sll.get_at_index(0) == 20
        assert sll.get_at_index(1) == 8
        assert sll.get_at_index(2) == 5
        assert sll.get_at_index(3) == 1
    
    def test_large_list_operations(self):
        """Test operations on a large list."""
        sll = SinglyLinkedList()
        size = 1000
        
        # Build large list
        for i in range(size):
            sll.append(i)
        
        assert len(sll) == size
        
        # Test access at different positions
        assert sll.get_at_index(0) == 0
        assert sll.get_at_index(size // 2) == size // 2
        assert sll.get_at_index(size - 1) == size - 1
        
        # Test modification
        sll.set_at_index(size // 2, 9999)
        assert sll.get_at_index(size // 2) == 9999
        
        # Test iteration
        elements = list(sll)
        assert len(elements) == size
        assert elements[0] == 0
        assert elements[size // 2] == 9999
        assert elements[size - 1] == size - 1
    
    def test_memory_efficiency(self):
        """Test memory usage of the list."""
        sll = SinglyLinkedList()
        
        # Test initial memory usage
        initial_size = sll.get_memory_usage()
        
        # Add elements and check memory growth
        for i in range(100):
            sll.append(i)
        
        # Memory should grow but not excessively
        final_size = sll.get_memory_usage()
        assert final_size > initial_size
        
        # Check that we can still access elements
        assert sll.get_at_index(50) == 50
    
    def test_edge_cases(self):
        """Test various edge cases."""
        sll = SinglyLinkedList()
        
        # Test with None values
        sll.append(None)
        sll.append(10)
        sll.append(None)
        
        assert len(sll) == 3
        assert sll.get_at_index(0) is None
        assert sll.get_at_index(1) == 10
        assert sll.get_at_index(2) is None
        
        # Test with different data types
        sll.clear()
        sll.append("string")
        sll.append(42)
        sll.append(3.14)
        sll.append([1, 2, 3])
        sll.append({"key": "value"})
        
        assert len(sll) == 5
        assert sll.get_at_index(0) == "string"
        assert sll.get_at_index(1) == 42
        assert sll.get_at_index(2) == 3.14
        assert sll.get_at_index(3) == [1, 2, 3]
        assert sll.get_at_index(4) == {"key": "value"}
    
    def test_sentinel_nodes(self):
        """Test that sentinel nodes work correctly."""
        sll = SinglyLinkedList()
        
        # Check initial sentinel setup
        assert sll._head_sentinel.data is None
        assert sll._tail_sentinel.data is None
        assert sll._head_sentinel.next == sll._tail_sentinel
        
        # Add elements and check sentinel connections
        sll.append(10)
        sll.append(20)
        
        # Head sentinel should point to first element
        assert sll._head_sentinel.next.data == 10
        
        # Last element should point to tail sentinel
        current = sll._head_sentinel.next
        while current.next != sll._tail_sentinel:
            current = current.next
        assert current.data == 20
        assert current.next == sll._tail_sentinel 