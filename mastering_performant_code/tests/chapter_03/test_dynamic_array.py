"""
Unit tests for Dynamic Array implementations.

This module provides comprehensive tests for all dynamic array classes
to ensure 100% code coverage and correct functionality.
"""

import pytest
import sys
from typing import List
from src.chapter_03.dynamic_array import (
    DynamicArray,
    AdvancedDynamicArray,
    ProductionDynamicArray,
    GrowthStrategy
)


class TestDynamicArray:
    """Test cases for the basic DynamicArray class."""
    
    def test_init_valid_parameters(self):
        """Test initialization with valid parameters."""
        arr = DynamicArray[int](initial_capacity=4, growth_factor=1.5)
        assert len(arr) == 0
        assert arr.capacity == 4
        assert arr._growth_factor == 1.5
    
    def test_init_invalid_capacity(self):
        """Test initialization with invalid capacity."""
        with pytest.raises(ValueError, match="Initial capacity must be positive"):
            DynamicArray[int](initial_capacity=0)
        
        with pytest.raises(ValueError, match="Initial capacity must be positive"):
            DynamicArray[int](initial_capacity=-1)
    
    def test_init_invalid_growth_factor(self):
        """Test initialization with invalid growth factor."""
        with pytest.raises(ValueError, match="Growth factor must be greater than 1.0"):
            DynamicArray[int](growth_factor=1.0)
        
        with pytest.raises(ValueError, match="Growth factor must be greater than 1.0"):
            DynamicArray[int](growth_factor=0.5)
    
    def test_len_empty_array(self):
        """Test length of empty array."""
        arr = DynamicArray[int]()
        assert len(arr) == 0
    
    def test_len_after_append(self):
        """Test length after appending elements."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        assert len(arr) == 3
    
    def test_getitem_valid_index(self):
        """Test getting item at valid index."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3
    
    def test_getitem_invalid_index(self):
        """Test getting item at invalid index."""
        arr = DynamicArray[int]()
        arr.append(1)
        
        with pytest.raises(IndexError, match="Index out of range"):
            _ = arr[1]
        
        with pytest.raises(IndexError, match="Index out of range"):
            _ = arr[-1]
    
    def test_setitem_valid_index(self):
        """Test setting item at valid index."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        arr[1] = 42
        assert arr[1] == 42
        assert arr[0] == 1
        assert arr[2] == 3
    
    def test_setitem_invalid_index(self):
        """Test setting item at invalid index."""
        arr = DynamicArray[int]()
        arr.append(1)
        
        with pytest.raises(IndexError, match="Index out of range"):
            arr[1] = 42
    
    def test_append_single_element(self):
        """Test appending a single element."""
        arr = DynamicArray[int]()
        arr.append(42)
        
        assert len(arr) == 1
        assert arr[0] == 42
    
    def test_append_multiple_elements(self):
        """Test appending multiple elements."""
        arr = DynamicArray[int]()
        for i in range(10):
            arr.append(i)
        
        assert len(arr) == 10
        for i in range(10):
            assert arr[i] == i
    
    def test_append_triggers_resize(self):
        """Test that append triggers resize when capacity is reached."""
        arr = DynamicArray[int](initial_capacity=2)
        
        # Fill the array
        arr.append(1)
        arr.append(2)
        assert arr.capacity == 2
        
        # This should trigger resize
        arr.append(3)
        assert arr.capacity == 4
        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3
    
    def test_insert_at_beginning(self):
        """Test inserting at the beginning."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        arr.insert(0, 0)
        assert len(arr) == 3
        assert arr[0] == 0
        assert arr[1] == 1
        assert arr[2] == 2
    
    def test_insert_at_middle(self):
        """Test inserting in the middle."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(3)
        
        arr.insert(1, 2)
        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3
    
    def test_insert_at_end(self):
        """Test inserting at the end."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        arr.insert(2, 3)
        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3
    
    def test_insert_invalid_index(self):
        """Test inserting at invalid index."""
        arr = DynamicArray[int]()
        arr.append(1)
        
        with pytest.raises(IndexError, match="Index out of range"):
            arr.insert(2, 2)
        
        with pytest.raises(IndexError, match="Index out of range"):
            arr.insert(-1, 0)
    
    def test_insert_triggers_resize(self):
        """Test that insert triggers resize when capacity is reached."""
        arr = DynamicArray[int](initial_capacity=2)
        arr.append(1)
        arr.append(2)
        
        arr.insert(1, 1.5)
        assert arr.capacity == 4
        assert len(arr) == 3
    
    def test_pop_last_element(self):
        """Test popping the last element."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        value = arr.pop()
        assert value == 3
        assert len(arr) == 2
        assert arr[0] == 1
        assert arr[1] == 2
    
    def test_pop_specific_index(self):
        """Test popping element at specific index."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        value = arr.pop(1)
        assert value == 2
        assert len(arr) == 2
        assert arr[0] == 1
        assert arr[1] == 3
    
    def test_pop_empty_array(self):
        """Test popping from empty array."""
        arr = DynamicArray[int]()
        
        with pytest.raises(IndexError, match="Cannot pop from empty array"):
            arr.pop()
    
    def test_pop_invalid_index(self):
        """Test popping at invalid index."""
        arr = DynamicArray[int]()
        arr.append(1)
        
        with pytest.raises(IndexError, match="Index out of range"):
            arr.pop(1)
    
    def test_remove_existing_element(self):
        """Test removing an existing element."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        arr.remove(2)
        assert len(arr) == 2
        assert arr[0] == 1
        assert arr[1] == 3
    
    def test_remove_nonexistent_element(self):
        """Test removing a non-existent element."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        with pytest.raises(ValueError, match="Value not found"):
            arr.remove(3)
    
    def test_iteration(self):
        """Test iteration over array elements."""
        arr = DynamicArray[int]()
        for i in range(5):
            arr.append(i)
        
        elements = list(arr)
        assert elements == [0, 1, 2, 3, 4]
    
    def test_contains_existing_element(self):
        """Test contains with existing element."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        assert 2 in arr
        assert 1 in arr
        assert 3 in arr
    
    def test_contains_nonexistent_element(self):
        """Test contains with non-existent element."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        assert 4 not in arr
        assert 0 not in arr
    
    def test_repr(self):
        """Test string representation."""
        arr = DynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.append(3)
        
        assert repr(arr) == "DynamicArray([1, 2, 3])"
    
    def test_capacity_property(self):
        """Test capacity property."""
        arr = DynamicArray[int](initial_capacity=8)
        assert arr.capacity == 8
        
        # Trigger resize
        for i in range(8):
            arr.append(i)
        arr.append(8)
        assert arr.capacity == 16
    
    def test_load_factor_property(self):
        """Test load factor property."""
        arr = DynamicArray[int](initial_capacity=8)
        assert arr.load_factor == 0.0
        
        arr.append(1)
        assert arr.load_factor == 1/8
        
        arr.append(2)
        assert arr.load_factor == 2/8
        
        # Fill to capacity
        for i in range(3, 9):
            arr.append(i)
        assert arr.load_factor == 1.0


class TestAdvancedDynamicArray:
    """Test cases for the AdvancedDynamicArray class."""
    
    def test_init_valid_parameters(self):
        """Test initialization with valid parameters."""
        arr = AdvancedDynamicArray[int](
            initial_capacity=4,
            strategy=GrowthStrategy.DOUBLING,
            shrink_threshold=0.3
        )
        assert len(arr) == 0
        assert arr.capacity == 4
        assert arr._strategy == GrowthStrategy.DOUBLING
        assert arr._shrink_threshold == 0.3
    
    def test_init_invalid_capacity(self):
        """Test initialization with invalid capacity."""
        with pytest.raises(ValueError, match="Initial capacity must be positive"):
            AdvancedDynamicArray[int](initial_capacity=0)
    
    def test_init_invalid_shrink_threshold(self):
        """Test initialization with invalid shrink threshold."""
        with pytest.raises(ValueError, match="Shrink threshold must be between 0 and 1"):
            AdvancedDynamicArray[int](shrink_threshold=0.0)
        
        with pytest.raises(ValueError, match="Shrink threshold must be between 0 and 1"):
            AdvancedDynamicArray[int](shrink_threshold=1.0)
    
    def test_doubling_strategy(self):
        """Test doubling growth strategy."""
        arr = AdvancedDynamicArray[int](strategy=GrowthStrategy.DOUBLING)
        
        # Add elements to trigger resizes
        for i in range(9):
            arr.append(i)
        
        # Should have resized: 8 -> 16
        assert arr.capacity == 16
        assert arr.resize_count == 1
    
    def test_fixed_strategy(self):
        """Test fixed growth strategy."""
        arr = AdvancedDynamicArray[int](strategy=GrowthStrategy.FIXED)
        
        # Add elements to trigger resizes
        for i in range(9):
            arr.append(i)
        
        # Should have resized: 8 -> 18
        assert arr.capacity == 18
        assert arr.resize_count == 1
    
    def test_golden_ratio_strategy(self):
        """Test golden ratio growth strategy."""
        arr = AdvancedDynamicArray[int](strategy=GrowthStrategy.GOLDEN_RATIO)
        
        # Add elements to trigger resizes
        for i in range(9):
            arr.append(i)
        
        # Should have resized: 8 -> 12 (int(8 * 1.618) = 12)
        assert arr.capacity == 12
        assert arr.resize_count == 1
    
    def test_adaptive_strategy_small_array(self):
        """Test adaptive strategy with small array."""
        arr = AdvancedDynamicArray[int](strategy=GrowthStrategy.ADAPTIVE)
        
        # Add elements to trigger resizes
        for i in range(9):
            arr.append(i)
        
        # Should use doubling for small arrays
        assert arr.capacity == 16
        assert arr.resize_count == 1
    
    def test_adaptive_strategy_large_array(self):
        """Test adaptive strategy with large array."""
        arr = AdvancedDynamicArray[int](strategy=GrowthStrategy.ADAPTIVE)
        
        # Add elements to make it a large array
        for i in range(1001):
            arr.append(i)
        
        # Should use golden ratio for large arrays
        # Capacity should be around 1000 * 1.618
        assert arr.capacity > 1000
        assert arr.resize_count > 0
    
    def test_shrink_to_fit(self):
        """Test shrinking array to fit."""
        arr = AdvancedDynamicArray[int](shrink_threshold=0.5)
        
        # Add elements
        for i in range(8):
            arr.append(i)
        
        # Remove elements to trigger shrink
        for _ in range(5):
            arr.pop()
        
        # Should shrink to minimum capacity of 8
        assert arr.capacity == 8
    
    def test_memory_efficiency_property(self):
        """Test memory efficiency property."""
        arr = AdvancedDynamicArray[int]()
        assert arr.memory_efficiency == 0.0
        
        arr.append(1)
        assert arr.memory_efficiency == 1/8
        
        arr.append(2)
        assert arr.memory_efficiency == 2/8
    
    def test_resize_count_property(self):
        """Test resize count property."""
        arr = AdvancedDynamicArray[int]()
        assert arr.resize_count == 0
        
        # Trigger resize
        for i in range(8):
            arr.append(i)
        arr.append(8)
        assert arr.resize_count == 1


class TestProductionDynamicArray:
    """Test cases for the ProductionDynamicArray class."""
    
    def test_init_valid_parameters(self):
        """Test initialization with valid parameters."""
        arr = ProductionDynamicArray[int](
            initial_capacity=4,
            strategy=GrowthStrategy.DOUBLING,
            shrink_threshold=0.3,
            min_capacity=2
        )
        assert len(arr) == 0
        assert arr.capacity == 4
        assert arr._strategy == GrowthStrategy.DOUBLING
        assert arr._shrink_threshold == 0.3
        assert arr._min_capacity == 2
    
    def test_init_invalid_parameters(self):
        """Test initialization with invalid parameters."""
        with pytest.raises(ValueError, match="Initial capacity must be positive"):
            ProductionDynamicArray[int](initial_capacity=0)
        
        with pytest.raises(ValueError, match="Shrink threshold must be between 0 and 1"):
            ProductionDynamicArray[int](shrink_threshold=0.0)
        
        with pytest.raises(ValueError, match="Minimum capacity must be positive"):
            ProductionDynamicArray[int](min_capacity=0)
    
    def test_getitem_with_bounds_checking(self):
        """Test getitem with detailed bounds checking."""
        arr = ProductionDynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        with pytest.raises(IndexError, match="Index 2 out of range for array of size 2"):
            _ = arr[2]
    
    def test_setitem_with_bounds_checking(self):
        """Test setitem with detailed bounds checking."""
        arr = ProductionDynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        with pytest.raises(IndexError, match="Index 2 out of range for array of size 2"):
            arr[2] = 3
    
    def test_insert_with_bounds_checking(self):
        """Test insert with detailed bounds checking."""
        arr = ProductionDynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        with pytest.raises(IndexError, match="Index 3 out of range for insertion"):
            arr.insert(3, 3)
    
    def test_pop_with_bounds_checking(self):
        """Test pop with detailed bounds checking."""
        arr = ProductionDynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        with pytest.raises(IndexError, match="Index 2 out of range for array of size 2"):
            arr.pop(2)
    
    def test_remove_with_detailed_error(self):
        """Test remove with detailed error message."""
        arr = ProductionDynamicArray[int]()
        arr.append(1)
        arr.append(2)
        
        with pytest.raises(ValueError, match="Value 3 not found in array"):
            arr.remove(3)
    
    def test_clear(self):
        """Test clearing the array."""
        arr = ProductionDynamicArray[int]()
        for i in range(10):
            arr.append(i)
        
        arr.clear()
        assert len(arr) == 0
        assert arr.capacity == arr._min_capacity
    
    def test_extend(self):
        """Test extending with iterable."""
        arr = ProductionDynamicArray[int]()
        arr.extend([1, 2, 3])
        
        assert len(arr) == 3
        assert arr[0] == 1
        assert arr[1] == 2
        assert arr[2] == 3
    
    def test_index_valid_range(self):
        """Test index with valid range."""
        arr = ProductionDynamicArray[int]()
        for i in range(10):
            arr.append(i)
        
        assert arr.index(5) == 5
        assert arr.index(5, start=3) == 5
        assert arr.index(5, start=3, end=7) == 5
    
    def test_index_invalid_range(self):
        """Test index with invalid range."""
        arr = ProductionDynamicArray[int]()
        for i in range(10):
            arr.append(i)
        
        with pytest.raises(ValueError, match="Invalid start/end indices"):
            arr.index(5, start=5, end=3)
    
    def test_index_not_found(self):
        """Test index when value not found."""
        arr = ProductionDynamicArray[int]()
        for i in range(10):
            arr.append(i)
        
        with pytest.raises(ValueError, match="Value 15 not found in array"):
            arr.index(15)
    
    def test_count(self):
        """Test counting occurrences."""
        arr = ProductionDynamicArray[int]()
        arr.extend([1, 2, 1, 3, 1, 4])
        
        assert arr.count(1) == 3
        assert arr.count(2) == 1
        assert arr.count(5) == 0
    
    def test_reverse(self):
        """Test reversing the array."""
        arr = ProductionDynamicArray[int]()
        arr.extend([1, 2, 3, 4, 5])
        
        arr.reverse()
        assert list(arr) == [5, 4, 3, 2, 1]
    
    def test_reverse_empty(self):
        """Test reversing empty array."""
        arr = ProductionDynamicArray[int]()
        arr.reverse()
        assert len(arr) == 0
    
    def test_reverse_single_element(self):
        """Test reversing single element array."""
        arr = ProductionDynamicArray[int]()
        arr.append(1)
        
        arr.reverse()
        assert list(arr) == [1]
    
    def test_auto_shrink_on_pop(self):
        """Test automatic shrinking when popping elements."""
        arr = ProductionDynamicArray[int](shrink_threshold=0.5)
        
        # Add elements
        for i in range(16):
            arr.append(i)
        
        # Remove elements to trigger shrink
        for _ in range(9):
            arr.pop()
        
        # Should have shrunk
        assert arr.capacity < 16
    
    def test_stats_property(self):
        """Test stats property."""
        arr = ProductionDynamicArray[int]()
        arr.append(1)
        arr.append(2)
        arr.pop()
        
        stats = arr.stats
        assert stats['size'] == 1
        assert stats['capacity'] == 8
        assert stats['total_added'] == 2
        assert stats['total_removed'] == 1
        assert stats['strategy'] == 'doubling'
    
    def test_performance_tracking(self):
        """Test performance tracking counters."""
        arr = ProductionDynamicArray[int]()
        
        # Add elements
        for i in range(10):
            arr.append(i)
        
        # Remove elements
        for _ in range(5):
            arr.pop()
        
        assert arr._total_elements_added == 10
        assert arr._total_elements_removed == 5


class TestGrowthStrategy:
    """Test cases for the GrowthStrategy enum."""
    
    def test_enum_values(self):
        """Test that all expected enum values exist."""
        assert GrowthStrategy.DOUBLING == GrowthStrategy.DOUBLING
        assert GrowthStrategy.FIXED == GrowthStrategy.FIXED
        assert GrowthStrategy.GOLDEN_RATIO == GrowthStrategy.GOLDEN_RATIO
        assert GrowthStrategy.ADAPTIVE == GrowthStrategy.ADAPTIVE
    
    def test_enum_string_values(self):
        """Test enum string values."""
        assert GrowthStrategy.DOUBLING.value == "doubling"
        assert GrowthStrategy.FIXED.value == "fixed"
        assert GrowthStrategy.GOLDEN_RATIO.value == "golden_ratio"
        assert GrowthStrategy.ADAPTIVE.value == "adaptive"


if __name__ == "__main__":
    pytest.main([__file__]) 