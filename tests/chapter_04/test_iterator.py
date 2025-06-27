"""
Unit tests for LinkedListIterator implementation.

This module provides comprehensive tests for the LinkedListIterator class,
ensuring 100% code coverage and testing all edge cases.
"""

import pytest
from typing import List

from mastering_performant_code.chapter_04.iterator import LinkedListIterator, IteratorState
from mastering_performant_code.chapter_04.doubly_linked_list import DoublyLinkedList


class TestLinkedListIterator:
    """Test cases for LinkedListIterator class."""
    
    def test_init_forward(self):
        """Test initialization with forward direction."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        assert iterator._direction == 'forward'
        assert iterator._state.current_node == dll._head_sentinel.next
        assert iterator._state.index == -1
        assert not iterator._state.exhausted
    
    def test_init_reverse(self):
        """Test initialization with reverse direction."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='reverse')
        assert iterator._direction == 'reverse'
        assert iterator._state.current_node == dll._tail_sentinel.prev
        assert iterator._state.index == 5
        assert not iterator._state.exhausted
    
    def test_init_invalid_direction(self):
        """Test initialization with invalid direction."""
        dll = DoublyLinkedList()
        dll.append(1)
        
        with pytest.raises(ValueError, match="Direction must be 'forward' or 'reverse'"):
            LinkedListIterator(dll, direction='invalid')
    
    def test_init_with_start_index(self):
        """Test initialization with start index."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, start_index=2)
        assert iterator._state.index == 1
        assert iterator._state.current_node.data == 2
    
    def test_init_with_invalid_start_index(self):
        """Test initialization with invalid start index."""
        dll = DoublyLinkedList()
        dll.append(1)
        
        with pytest.raises(IndexError, match="Start index out of range"):
            LinkedListIterator(dll, start_index=5)
    
    def test_iter_forward(self):
        """Test forward iteration."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            dll.append(element)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator)
        assert result == elements
    
    def test_iter_reverse(self):
        """Test reverse iteration."""
        dll = DoublyLinkedList()
        elements = [1, 2, 3, 4, 5]
        for element in elements:
            dll.append(element)
        
        iterator = LinkedListIterator(dll, direction='reverse')
        result = list(iterator)
        assert result == list(reversed(elements))
    
    def test_iter_empty_list(self):
        """Test iteration over empty list."""
        dll = DoublyLinkedList()
        
        # Forward iteration
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator)
        assert result == []
        
        # Reverse iteration
        iterator = LinkedListIterator(dll, direction='reverse')
        result = list(iterator)
        assert result == []
    
    def test_current_index(self):
        """Test current_index method."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        assert iterator.current_index() == -1
        
        # Iterate and check index
        for i, _ in enumerate(iterator):
            assert iterator.current_index() == i
    
    def test_has_next_forward(self):
        """Test has_next with forward direction."""
        dll = DoublyLinkedList()
        dll.append(1)
        dll.append(2)
        
        iterator = LinkedListIterator(dll, direction='forward')
        assert iterator.has_next() is True
        
        # Consume first element
        next(iterator)
        assert iterator.has_next() is True
        
        # Consume second element
        next(iterator)
        assert iterator.has_next() is False
    
    def test_has_next_reverse(self):
        """Test has_next with reverse direction."""
        dll = DoublyLinkedList()
        dll.append(1)
        dll.append(2)
        
        iterator = LinkedListIterator(dll, direction='reverse')
        assert iterator.has_next() is True
        
        # Consume first element
        next(iterator)
        assert iterator.has_next() is True
        
        # Consume second element
        next(iterator)
        assert iterator.has_next() is False
    
    def test_has_next_empty(self):
        """Test has_next on empty list."""
        dll = DoublyLinkedList()
        
        iterator = LinkedListIterator(dll, direction='forward')
        assert iterator.has_next() is False
        
        iterator = LinkedListIterator(dll, direction='reverse')
        assert iterator.has_next() is False
    
    def test_filter(self):
        """Test filter method."""
        dll = DoublyLinkedList()
        for i in range(10):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        even_numbers = list(iterator.filter(lambda x: x % 2 == 0))
        assert even_numbers == [0, 2, 4, 6, 8]
    
    def test_filter_empty_result(self):
        """Test filter with no matching elements."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        large_numbers = list(iterator.filter(lambda x: x > 10))
        assert large_numbers == []
    
    def test_take(self):
        """Test take method."""
        dll = DoublyLinkedList()
        for i in range(10):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        first_three = list(iterator.take(3))
        assert first_three == [0, 1, 2]
    
    def test_take_more_than_available(self):
        """Test take with count larger than available elements."""
        dll = DoublyLinkedList()
        for i in range(3):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator.take(5))
        assert result == [0, 1, 2]
    
    def test_take_zero(self):
        """Test take with zero count."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator.take(0))
        assert result == []
    
    def test_take_negative_count(self):
        """Test take with negative count."""
        dll = DoublyLinkedList()
        dll.append(1)
        
        iterator = LinkedListIterator(dll, direction='forward')
        with pytest.raises(ValueError, match="Count must be non-negative"):
            list(iterator.take(-1))
    
    def test_skip(self):
        """Test skip method."""
        dll = DoublyLinkedList()
        for i in range(10):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        after_three = list(iterator.skip(3))
        assert after_three == [3, 4, 5, 6, 7, 8, 9]
    
    def test_skip_more_than_available(self):
        """Test skip with count larger than available elements."""
        dll = DoublyLinkedList()
        for i in range(3):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator.skip(5))
        assert result == []
    
    def test_skip_zero(self):
        """Test skip with zero count."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator.skip(0))
        assert result == [0, 1, 2, 3, 4]
    
    def test_skip_negative_count(self):
        """Test skip with negative count."""
        dll = DoublyLinkedList()
        dll.append(1)
        
        iterator = LinkedListIterator(dll, direction='forward')
        with pytest.raises(ValueError, match="Count must be non-negative"):
            list(iterator.skip(-1))
    
    def test_map(self):
        """Test map method."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        doubled = list(iterator.map(lambda x: x * 2))
        assert doubled == [0, 2, 4, 6, 8]
    
    def test_enumerate(self):
        """Test enumerate method."""
        dll = DoublyLinkedList()
        for i in range(3):
            dll.append(i * 10)
        
        iterator = LinkedListIterator(dll, direction='forward')
        enumerated = list(iterator.enumerate())
        assert enumerated == [(0, 0), (1, 10), (2, 20)]
    
    def test_collect(self):
        """Test collect method."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.collect()
        assert result == [0, 1, 2, 3, 4]
        assert isinstance(result, list)
    
    def test_find_first_found(self):
        """Test find_first with matching element."""
        dll = DoublyLinkedList()
        for i in range(10):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.find_first(lambda x: x > 5)
        assert result == 6
    
    def test_find_first_not_found(self):
        """Test find_first with no matching element."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.find_first(lambda x: x > 10)
        assert result is None
    
    def test_all_true(self):
        """Test all method with all elements matching."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.all(lambda x: x >= 0)
        assert result is True
    
    def test_all_false(self):
        """Test all method with some elements not matching."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.all(lambda x: x > 2)
        assert result is False
    
    def test_any_true(self):
        """Test any method with some elements matching."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.any(lambda x: x > 3)
        assert result is True
    
    def test_any_false(self):
        """Test any method with no elements matching."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.any(lambda x: x > 10)
        assert result is False
    
    def test_count_matching(self):
        """Test count_matching method."""
        dll = DoublyLinkedList()
        for i in range(10):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.count_matching(lambda x: x % 2 == 0)
        assert result == 5
    
    def test_count_matching_zero(self):
        """Test count_matching with no matching elements."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = iterator.count_matching(lambda x: x > 10)
        assert result == 0
    
    def test_get_state(self):
        """Test get_state method."""
        dll = DoublyLinkedList()
        for i in range(3):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        state = iterator.get_state()
        
        assert isinstance(state, IteratorState)
        assert state.direction == 'forward'
        assert state.index == -1
        assert not state.exhausted
    
    def test_set_state(self):
        """Test set_state method."""
        dll = DoublyLinkedList()
        for i in range(3):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        
        # Get current state
        original_state = iterator.get_state()
        
        # Modify iterator
        next(iterator)
        
        # Set back to original state
        iterator.set_state(original_state)
        
        # Should start from beginning
        result = list(iterator)
        assert result == [0, 1, 2]
    
    def test_reset(self):
        """Test _reset method."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        
        # Consume some elements
        next(iterator)
        next(iterator)
        
        # Reset
        iterator._reset()
        
        # Should start from beginning
        result = list(iterator)
        assert result == [0, 1, 2, 3, 4]
    
    def test_reset_with_start_index(self):
        """Test _reset method with start index."""
        dll = DoublyLinkedList()
        for i in range(5):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        
        # Reset to specific index
        iterator._reset(2)
        
        # Should start from index 2
        result = list(iterator)
        assert result == [2, 3, 4]
    
    def test_reset_with_invalid_start_index(self):
        """Test _reset method with invalid start index."""
        dll = DoublyLinkedList()
        dll.append(1)
        
        iterator = LinkedListIterator(dll, direction='forward')
        
        with pytest.raises(IndexError, match="Start index out of range"):
            iterator._reset(5)
    
    def test_exhausted_state(self):
        """Test exhausted state handling."""
        dll = DoublyLinkedList()
        dll.append(1)
        
        iterator = LinkedListIterator(dll, direction='forward')
        
        # Consume the element
        next(iterator)
        
        # Should be exhausted
        assert iterator._state.exhausted is True
        
        # Should raise StopIteration
        with pytest.raises(StopIteration):
            next(iterator)
    
    def test_mixed_operations(self):
        """Test mixed operations on iterator."""
        dll = DoublyLinkedList()
        for i in range(10):
            dll.append(i)
        
        iterator = LinkedListIterator(dll, direction='forward')
        
        # Skip first 2, take next 3, filter even numbers
        result = list(iterator.skip(2).take(3).filter(lambda x: x % 2 == 0))
        assert result == [2, 4]
    
    def test_large_list_iteration(self):
        """Test iteration over large list."""
        dll = DoublyLinkedList()
        size = 1000
        
        for i in range(size):
            dll.append(i)
        
        # Forward iteration
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator)
        assert len(result) == size
        assert result[0] == 0
        assert result[size - 1] == size - 1
        
        # Reverse iteration
        iterator = LinkedListIterator(dll, direction='reverse')
        result = list(iterator)
        assert len(result) == size
        assert result[0] == size - 1
        assert result[size - 1] == 0
    
    def test_edge_cases(self):
        """Test various edge cases."""
        dll = DoublyLinkedList()
        
        # Test with None values
        dll.append(None)
        dll.append(1)
        dll.append(None)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator)
        assert result == [None, 1, None]
        
        # Test with different data types
        dll.clear()
        dll.append("string")
        dll.append(42)
        dll.append(3.14)
        
        iterator = LinkedListIterator(dll, direction='forward')
        result = list(iterator)
        assert result == ["string", 42, 3.14]
        
        # Test that the iterator is properly exhausted
        with pytest.raises(StopIteration):
            next(iterator)


class TestChainableIterator:
    """Test cases for ChainableIterator class."""
    
    def setup_method(self):
        """Set up test data."""
        from mastering_performant_code.chapter_04.doubly_linked_list import DoublyLinkedList
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        self.dll = DoublyLinkedList()
        for i in range(10):
            self.dll.append(i)
        self.iterator = ChainableIterator(self.dll)
    
    def test_filter_chaining(self):
        """Test filter method chaining."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        # Create a new iterator with filter
        filtered_iter = ChainableIterator(self.dll).filter(lambda x: x % 2 == 0)
        
        # Should return even numbers
        result = list(filtered_iter)
        assert result == [0, 2, 4, 6, 8]
    
    def test_map_chaining(self):
        """Test map method chaining."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        # Create a new iterator with map
        mapped_iter = ChainableIterator(self.dll).map(lambda x: x * 2)
        
        # Should return doubled values
        result = list(mapped_iter)
        assert result == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    
    def test_take_chaining(self):
        """Test take method chaining."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        # Create a new iterator with take
        taken_iter = ChainableIterator(self.dll).take(5)
        
        # Should return first 5 elements
        result = list(taken_iter)
        assert result == [0, 1, 2, 3, 4]
    
    def test_multiple_chaining(self):
        """Test multiple method chaining."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        # Chain multiple operations
        chained_iter = (ChainableIterator(self.dll)
                       .filter(lambda x: x % 2 == 0)  # Even numbers
                       .map(lambda x: x * 2)          # Double them
                       .take(3))                      # Take first 3
        
        result = list(chained_iter)
        assert result == [0, 4, 8]  # 0*2, 2*2, 4*2
    
    def test_filter_with_predicate(self):
        """Test filter with custom predicate."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        # Filter numbers greater than 5
        filtered_iter = ChainableIterator(self.dll).filter(lambda x: x > 5)
        
        result = list(filtered_iter)
        assert result == [6, 7, 8, 9]
    
    def test_map_with_transform(self):
        """Test map with custom transformation."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        # Transform to strings
        mapped_iter = ChainableIterator(self.dll).map(lambda x: f"num_{x}")
        
        result = list(mapped_iter)
        assert result == ["num_0", "num_1", "num_2", "num_3", "num_4", 
                         "num_5", "num_6", "num_7", "num_8", "num_9"]
    
    def test_take_zero(self):
        """Test take with zero elements."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        taken_iter = ChainableIterator(self.dll).take(0)
        result = list(taken_iter)
        assert result == []
    
    def test_take_more_than_available(self):
        """Test take with more elements than available."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        taken_iter = ChainableIterator(self.dll).take(15)
        result = list(taken_iter)
        assert result == list(range(10))  # All elements
    
    def test_empty_list_chaining(self):
        """Test chaining on empty list."""
        from mastering_performant_code.chapter_04.doubly_linked_list import DoublyLinkedList
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        empty_dll = DoublyLinkedList()
        chained_iter = (ChainableIterator(empty_dll)
                       .filter(lambda x: x > 0)
                       .map(lambda x: x * 2)
                       .take(5))
        
        result = list(chained_iter)
        assert result == []
    
    def test_iterator_reuse(self):
        """Test that chained iterators are properly exhausted after use."""
        from mastering_performant_code.chapter_04.iterator import ChainableIterator
        
        # Create chained iterator
        chained_iter = ChainableIterator(self.dll).filter(lambda x: x % 2 == 0)
        
        # Use it once
        result1 = list(chained_iter)
        assert result1 == [0, 2, 4, 6, 8]
        
        # Iterator should be exhausted after first use
        result2 = list(chained_iter)
        assert result2 == []  # Empty because iterator is exhausted
        
        # Create a new iterator for reuse
        chained_iter2 = ChainableIterator(self.dll).filter(lambda x: x % 2 == 0)
        result3 = list(chained_iter2)
        assert result3 == [0, 2, 4, 6, 8]  # New iterator works correctly 