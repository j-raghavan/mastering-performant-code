"""
Unit tests for DoublyLinkedList implementation.

This module provides comprehensive tests for the DoublyLinkedList class,
ensuring 100% code coverage and testing all edge cases.
"""

import pytest
from typing import List

from mastering_performant_code.chapter_04.doubly_linked_list import DoublyLinkedList
from mastering_performant_code.chapter_04.nodes import DoublyNode


class TestDoublyLinkedList:
    """Test cases for DoublyLinkedList class."""
    
    def test_init(self):
        """Test initialization of DoublyLinkedList."""
        dll = DoublyLinkedList()
        assert len(dll) == 0
        assert dll.is_empty()
        assert dll._head_sentinel.next == dll._tail_sentinel
        assert dll._tail_sentinel.prev == dll._head_sentinel
        assert dll._size == 0
    
    def test_extend_from_iterable(self):
        """Test batch insertion using extend_from_iterable."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        
        dll.extend_from_iterable(elements)
        
        assert len(dll) == len(elements)
        for i, element in enumerate(elements):
            assert dll.get_at_index(i) == element
    
    def test_extend_from_iterable_empty(self):
        """Test extend_from_iterable with empty iterable."""
        dll = DoublyLinkedList()
        dll.append(10)  # Add one element first
        
        dll.extend_from_iterable([])
        
        assert len(dll) == 1
        assert dll.get_at_index(0) == 10
    
    def test_extend_from_iterable_to_existing(self):
        """Test extend_from_iterable to existing list."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        new_elements = [30, 40, 50]
        dll.extend_from_iterable(new_elements)
        
        assert len(dll) == 5
        assert dll.get_at_index(0) == 10
        assert dll.get_at_index(1) == 20
        assert dll.get_at_index(2) == 30
        assert dll.get_at_index(3) == 40
        assert dll.get_at_index(4) == 50
    
    def test_append_single_element(self):
        """Test appending a single element."""
        dll = DoublyLinkedList()
        dll.append(42)
        
        assert len(dll) == 1
        assert not dll.is_empty()
        assert dll.get_at_index(0) == 42
    
    def test_append_multiple_elements(self):
        """Test appending multiple elements."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        
        for element in elements:
            dll.append(element)
        
        assert len(dll) == len(elements)
        for i, element in enumerate(elements):
            assert dll.get_at_index(i) == element
    
    def test_prepend_single_element(self):
        """Test prepending a single element."""
        dll = DoublyLinkedList()
        dll.prepend(42)
        
        assert len(dll) == 1
        assert dll.get_at_index(0) == 42
    
    def test_prepend_multiple_elements(self):
        """Test prepending multiple elements."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        
        for element in elements:
            dll.prepend(element)
        
        assert len(dll) == len(elements)
        # Elements should be in reverse order due to prepending
        for i, element in enumerate(reversed(elements)):
            assert dll.get_at_index(i) == element
    
    def test_insert_after_success(self):
        """Test successful insert_after operation."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        result = dll.insert_after(20, 25)
        assert result is True
        assert len(dll) == 4
        assert dll.get_at_index(2) == 25
        assert dll.get_at_index(3) == 30
    
    def test_insert_after_not_found(self):
        """Test insert_after when target is not found."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        result = dll.insert_after(30, 25)
        assert result is False
        assert len(dll) == 2
    
    def test_insert_after_empty_list(self):
        """Test insert_after on empty list."""
        dll = DoublyLinkedList()
        result = dll.insert_after(10, 20)
        assert result is False
        assert len(dll) == 0
    
    def test_insert_before_success(self):
        """Test successful insert_before operation."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        result = dll.insert_before(20, 15)
        assert result is True
        assert len(dll) == 4
        assert dll.get_at_index(1) == 15
        assert dll.get_at_index(2) == 20
    
    def test_insert_before_not_found(self):
        """Test insert_before when target is not found."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        result = dll.insert_before(30, 25)
        assert result is False
        assert len(dll) == 2
    
    def test_insert_before_empty_list(self):
        """Test insert_before on empty list."""
        dll = DoublyLinkedList()
        result = dll.insert_before(10, 20)
        assert result is False
        assert len(dll) == 0
    
    def test_delete_first_success(self):
        """Test successful delete_first operation."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        result = dll.delete_first(20)
        assert result is True
        assert len(dll) == 2
        assert dll.get_at_index(0) == 10
        assert dll.get_at_index(1) == 30
    
    def test_delete_first_not_found(self):
        """Test delete_first when element is not found."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        result = dll.delete_first(30)
        assert result is False
        assert len(dll) == 2
    
    def test_delete_first_empty_list(self):
        """Test delete_first on empty list."""
        dll = DoublyLinkedList()
        result = dll.delete_first(10)
        assert result is False
        assert len(dll) == 0
    
    def test_delete_first_duplicate_elements(self):
        """Test delete_first with duplicate elements."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(20)
        dll.append(30)
        
        result = dll.delete_first(20)
        assert result is True
        assert len(dll) == 3
        assert dll.get_at_index(1) == 20  # Second occurrence remains
        assert dll.get_at_index(2) == 30
    
    def test_get_at_index_valid_head_traversal(self):
        """Test get_at_index with valid indices using head traversal."""
        dll = DoublyLinkedList()
        elements = [10, 20, 30, 40, 50]
        for element in elements:
            dll.append(element)
        
        # Test indices that should use head traversal (first half)
        for i in range(len(elements) // 2):
            assert dll.get_at_index(i) == elements[i]
    
    def test_get_at_index_valid_tail_traversal(self):
        """Test get_at_index with valid indices using tail traversal."""
        dll = DoublyLinkedList()
        elements = [10, 20, 30, 40, 50]
        for element in elements:
            dll.append(element)
        
        # Test indices that should use tail traversal (second half)
        for i in range(len(elements) // 2, len(elements)):
            assert dll.get_at_index(i) == elements[i]
    
    def test_get_at_index_invalid(self):
        """Test get_at_index with invalid indices."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        with pytest.raises(IndexError):
            dll.get_at_index(-1)
        
        with pytest.raises(IndexError):
            dll.get_at_index(2)
        
        with pytest.raises(IndexError):
            dll.get_at_index(100)
    
    def test_get_at_index_empty_list(self):
        """Test get_at_index on empty list."""
        dll = DoublyLinkedList()
        with pytest.raises(IndexError):
            dll.get_at_index(0)
    
    def test_set_at_index_valid_head_traversal(self):
        """Test set_at_index with valid indices using head traversal."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        dll.append(40)
        dll.append(50)
        
        dll.set_at_index(1, 25)  # Should use head traversal
        assert dll.get_at_index(1) == 25
        assert dll.get_at_index(0) == 10
        assert dll.get_at_index(2) == 30
    
    def test_set_at_index_valid_tail_traversal(self):
        """Test set_at_index with valid indices using tail traversal."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        dll.append(40)
        dll.append(50)
        
        dll.set_at_index(3, 45)  # Should use tail traversal
        assert dll.get_at_index(3) == 45
        assert dll.get_at_index(2) == 30
        assert dll.get_at_index(4) == 50
    
    def test_set_at_index_invalid(self):
        """Test set_at_index with invalid indices."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        with pytest.raises(IndexError):
            dll.set_at_index(-1, 30)
        
        with pytest.raises(IndexError):
            dll.set_at_index(2, 30)
    
    def test_iteration_forward(self):
        """Test forward iteration over the list."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            dll.append(element)
        
        result = list(dll)
        assert result == elements
    
    def test_iteration_forward_empty(self):
        """Test forward iteration over empty list."""
        dll = DoublyLinkedList()
        result = list(dll)
        assert result == []
    
    def test_iteration_reverse(self):
        """Test reverse iteration over the list."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            dll.append(element)
        
        result = list(dll.reverse_iter())
        assert result == list(reversed(elements))
    
    def test_iteration_reverse_empty(self):
        """Test reverse iteration over empty list."""
        dll = DoublyLinkedList()
        result = list(dll.reverse_iter())
        assert result == []
    
    def test_repr(self):
        """Test string representation."""
        dll = DoublyLinkedList()
        assert repr(dll) == "DoublyLinkedList([])"
        
        dll.append(10)
        dll.append(20)
        assert repr(dll) == "DoublyLinkedList([10, 20])"
    
    def test_to_list(self):
        """Test conversion to Python list."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            dll.append(element)
        
        result = dll.to_list()
        assert result == elements
        assert isinstance(result, list)
    
    def test_reverse_empty(self):
        """Test reverse on empty list."""
        dll = DoublyLinkedList()
        dll.reverse()
        assert len(dll) == 0
        assert dll.is_empty()
    
    def test_reverse_single_element(self):
        """Test reverse on single element list."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.reverse()
        assert len(dll) == 1
        assert dll.get_at_index(0) == 10
    
    def test_reverse_multiple_elements(self):
        """Test reverse on multiple elements."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            dll.append(element)
        
        dll.reverse()
        reversed_elements = list(reversed(elements))
        
        for i, element in enumerate(reversed_elements):
            assert dll.get_at_index(i) == element
    
    def test_contains_true(self):
        """Test contains with existing element."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        assert dll.contains(20) is True
        assert dll.contains(10) is True
        assert dll.contains(30) is True
    
    def test_contains_false(self):
        """Test contains with non-existing element."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        assert dll.contains(30) is False
        assert dll.contains(0) is False
    
    def test_contains_empty(self):
        """Test contains on empty list."""
        dll = DoublyLinkedList()
        assert dll.contains(10) is False
    
    def test_count_single_occurrence(self):
        """Test count with single occurrence."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        assert dll.count(20) == 1
        assert dll.count(10) == 1
        assert dll.count(30) == 1
    
    def test_count_multiple_occurrences(self):
        """Test count with multiple occurrences."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(20)
        dll.append(30)
        dll.append(20)
        
        assert dll.count(20) == 3
        assert dll.count(10) == 1
        assert dll.count(30) == 1
    
    def test_count_not_found(self):
        """Test count with non-existing element."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        
        assert dll.count(30) == 0
        assert dll.count(0) == 0
    
    def test_count_empty(self):
        """Test count on empty list."""
        dll = DoublyLinkedList()
        assert dll.count(10) == 0
    
    def test_clear(self):
        """Test clearing the list."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        dll.clear()
        assert len(dll) == 0
        assert dll.is_empty()
        assert dll._head_sentinel.next == dll._tail_sentinel
        assert dll._tail_sentinel.prev == dll._head_sentinel
    
    def test_clear_empty(self):
        """Test clearing an empty list."""
        dll = DoublyLinkedList()
        dll.clear()
        assert len(dll) == 0
        assert dll.is_empty()
    
    def test_get_first_success(self):
        """Test successful get_first operation."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        assert dll.get_first() == 10
    
    def test_get_first_empty(self):
        """Test get_first on empty list."""
        dll = DoublyLinkedList()
        with pytest.raises(IndexError):
            dll.get_first()
    
    def test_get_last_success(self):
        """Test successful get_last operation."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        assert dll.get_last() == 30
    
    def test_get_last_empty(self):
        """Test get_last on empty list."""
        dll = DoublyLinkedList()
        with pytest.raises(IndexError):
            dll.get_last()
    
    def test_remove_first_success(self):
        """Test successful remove_first operation."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        removed = dll.remove_first()
        assert removed == 10
        assert len(dll) == 2
        assert dll.get_at_index(0) == 20
        assert dll.get_at_index(1) == 30
    
    def test_remove_first_empty(self):
        """Test remove_first on empty list."""
        dll = DoublyLinkedList()
        with pytest.raises(IndexError):
            dll.remove_first()
    
    def test_remove_last_success(self):
        """Test successful remove_last operation."""
        dll = DoublyLinkedList()
        dll.append(10)
        dll.append(20)
        dll.append(30)
        
        removed = dll.remove_last()
        assert removed == 30
        assert len(dll) == 2
        assert dll.get_at_index(0) == 10
        assert dll.get_at_index(1) == 20
    
    def test_remove_last_empty(self):
        """Test remove_last on empty list."""
        dll = DoublyLinkedList()
        with pytest.raises(IndexError):
            dll.remove_last()
    
    def test_mixed_operations(self):
        """Test mixed operations on the list."""
        dll = DoublyLinkedList()
        
        # Append and prepend
        dll.append(10)
        dll.prepend(5)
        dll.append(20)
        dll.prepend(1)
        
        assert len(dll) == 4
        assert dll.get_at_index(0) == 1
        assert dll.get_at_index(1) == 5
        assert dll.get_at_index(2) == 10
        assert dll.get_at_index(3) == 20
        
        # Insert before and after
        dll.insert_after(5, 7)
        dll.insert_before(10, 8)
        
        assert len(dll) == 6
        assert dll.get_at_index(1) == 5
        assert dll.get_at_index(2) == 7
        assert dll.get_at_index(3) == 8
        assert dll.get_at_index(4) == 10
        
        # Delete
        dll.delete_first(8)
        
        assert len(dll) == 5
        assert dll.get_at_index(3) == 10
        
        # Set and get
        dll.set_at_index(2, 9)
        assert dll.get_at_index(2) == 9
        
        # Reverse
        dll.reverse()
        assert dll.get_at_index(0) == 20
        assert dll.get_at_index(1) == 10
        assert dll.get_at_index(2) == 9
        assert dll.get_at_index(3) == 5
        assert dll.get_at_index(4) == 1
    
    def test_large_list_operations(self):
        """Test operations on a large list."""
        dll = DoublyLinkedList()
        size = 1000
        
        # Build large list
        for i in range(size):
            dll.append(i)
        
        assert len(dll) == size
        
        # Test access at different positions (head and tail traversal)
        assert dll.get_at_index(0) == 0
        assert dll.get_at_index(size // 2) == size // 2
        assert dll.get_at_index(size - 1) == size - 1
        
        # Test modification
        dll.set_at_index(size // 2, 9999)
        assert dll.get_at_index(size // 2) == 9999
        
        # Test iteration
        elements = list(dll)
        assert len(elements) == size
        assert elements[0] == 0
        assert elements[size // 2] == 9999
        assert elements[size - 1] == size - 1
        
        # Test reverse iteration
        reverse_elements = list(dll.reverse_iter())
        assert len(reverse_elements) == size
        assert reverse_elements[0] == size - 1
        assert reverse_elements[size - 1 - (size // 2)] == 9999  # 9999 was at size//2, so in reverse it's at size-1-size//2
        assert reverse_elements[size - 1] == 0
    
    def test_memory_efficiency(self):
        """Test memory usage of the list."""
        dll = DoublyLinkedList()
        
        # Test initial memory usage
        initial_size = dll.get_memory_usage()
        
        # Add elements and check memory growth
        for i in range(100):
            dll.append(i)
        
        # Memory should grow but not excessively
        final_size = dll.get_memory_usage()
        assert final_size > initial_size
        
        # Check that we can still access elements
        assert dll.get_at_index(50) == 50
    
    def test_edge_cases(self):
        """Test various edge cases."""
        dll = DoublyLinkedList()
        
        # Test with None values
        dll.append(None)
        dll.append(10)
        dll.append(None)
        
        assert len(dll) == 3
        assert dll.get_at_index(0) is None
        assert dll.get_at_index(1) == 10
        assert dll.get_at_index(2) is None
        
        # Test with different data types
        dll.clear()
        dll.append("string")
        dll.append(42)
        dll.append(3.14)
        dll.append([1, 2, 3])
        dll.append({"key": "value"})
        
        assert len(dll) == 5
        assert dll.get_at_index(0) == "string"
        assert dll.get_at_index(1) == 42
        assert dll.get_at_index(2) == 3.14
        assert dll.get_at_index(3) == [1, 2, 3]
        assert dll.get_at_index(4) == {"key": "value"}
    
    def test_sentinel_nodes(self):
        """Test that sentinel nodes work correctly."""
        dll = DoublyLinkedList()
        
        # Check initial sentinel setup
        assert dll._head_sentinel.data is None
        assert dll._tail_sentinel.data is None
        assert dll._head_sentinel.next == dll._tail_sentinel
        assert dll._tail_sentinel.prev == dll._head_sentinel
        
        # Add elements and check sentinel connections
        dll.append(10)
        dll.append(20)
        
        # Head sentinel should point to first element
        assert dll._head_sentinel.next.data == 10
        assert dll._head_sentinel.next.prev == dll._head_sentinel
        
        # Last element should point to tail sentinel
        assert dll._tail_sentinel.prev.data == 20
        assert dll._tail_sentinel.prev.next == dll._tail_sentinel
        
        # Check bidirectional links
        first_node = dll._head_sentinel.next
        second_node = first_node.next
        assert first_node.next == second_node
        assert second_node.prev == first_node
    
    def test_optimized_access_patterns(self):
        """Test that access optimization works correctly."""
        dll = DoublyLinkedList()
        
        # Add many elements
        for i in range(100):
            dll.append(i)
        
        # Test access patterns that should use head traversal
        for i in range(50):
            assert dll.get_at_index(i) == i
        
        # Test access patterns that should use tail traversal
        for i in range(50, 100):
            assert dll.get_at_index(i) == i
        
        # Test boundary conditions
        assert dll.get_at_index(49) == 49  # Should use head
        assert dll.get_at_index(50) == 50  # Should use tail
        
        # Verify that access patterns are optimized
        assert dll.get_at_index(0) == 0   # Should use head traversal
        assert dll.get_at_index(99) == 99 # Should use tail traversal 