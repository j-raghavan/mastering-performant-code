"""
Unit tests for DynamicArray implementation.

This module provides comprehensive test coverage for the DynamicArray class,
including edge cases, resizing behavior, and performance tests.
"""

import unittest
import timeit
from typing import List

from mastering_performant_code.chapter_01.dynamic_array import DynamicArray, MemoryTrackedDynamicArray

class TestDynamicArray(unittest.TestCase):
    """Test cases for DynamicArray implementation."""
    
    def setUp(self):
        self.array = DynamicArray[int]()
    
    def test_initialization(self):
        """Test array initialization."""
        self.assertEqual(len(self.array), 0)
        self.assertEqual(self.array._capacity, 8)
        
        # Test custom initial capacity
        custom_array = DynamicArray[int](16)
        self.assertEqual(custom_array._capacity, 16)
    
    def test_append(self):
        """Test append operation."""
        self.array.append(1)
        self.array.append(2)
        self.array.append(3)
        
        self.assertEqual(len(self.array), 3)
        self.assertEqual(self.array[0], 1)
        self.assertEqual(self.array[1], 2)
        self.assertEqual(self.array[2], 3)
    
    def test_resize(self):
        """Test automatic resizing."""
        # Add more items than initial capacity
        for i in range(10):
            self.array.append(i)
        
        self.assertEqual(len(self.array), 10)
        self.assertGreater(self.array._capacity, 8)  # Should have resized
        
        # Verify all items are still accessible
        for i in range(10):
            self.assertEqual(self.array[i], i)
    
    def test_getitem_index_error(self):
        """Test index error on getitem."""
        with self.assertRaises(IndexError):
            _ = self.array[0]
        
        # Test negative index
        self.array.append(1)
        with self.assertRaises(IndexError):
            _ = self.array[-1]
        
        # Test out of bounds positive index
        with self.assertRaises(IndexError):
            _ = self.array[1]
    
    def test_setitem_index_error(self):
        """Test index error on setitem."""
        with self.assertRaises(IndexError):
            self.array[0] = 1
        
        # Test negative index
        self.array.append(1)
        with self.assertRaises(IndexError):
            self.array[-1] = 2
        
        # Test out of bounds positive index
        with self.assertRaises(IndexError):
            self.array[1] = 2
    
    def test_setitem_valid(self):
        """Test valid setitem operations."""
        self.array.append(1)
        self.array.append(2)
        
        self.array[0] = 10
        self.array[1] = 20
        
        self.assertEqual(self.array[0], 10)
        self.assertEqual(self.array[1], 20)
    
    def test_iteration(self):
        """Test iteration over array."""
        items = [1, 2, 3, 4, 5]
        for item in items:
            self.array.append(item)
        
        self.assertEqual(list(self.array), items)
        
        # Test iteration after resize
        for i in range(10):
            self.array.append(i + 100)
        
        expected = items + list(range(100, 110))
        self.assertEqual(list(self.array), expected)
    
    def test_repr(self):
        """Test string representation."""
        self.assertEqual(repr(self.array), "DynamicArray([])")
        
        self.array.append(1)
        self.array.append(2)
        self.assertEqual(repr(self.array), "DynamicArray([1, 2])")
    
    def test_multiple_resizes(self):
        """Test multiple resize operations."""
        # Force multiple resizes
        for i in range(100):
            self.array.append(i)
        
        self.assertEqual(len(self.array), 100)
        self.assertGreater(self.array._capacity, 100)
        
        # Verify all items are correct
        for i in range(100):
            self.assertEqual(self.array[i], i)
    
    def test_empty_array_operations(self):
        """Test operations on empty array."""
        self.assertEqual(len(self.array), 0)
        self.assertEqual(list(self.array), [])
        self.assertEqual(repr(self.array), "DynamicArray([])")
        
        with self.assertRaises(IndexError):
            _ = self.array[0]
        
        with self.assertRaises(IndexError):
            self.array[0] = 1


class TestMemoryTrackedDynamicArray(unittest.TestCase):
    """Test cases for MemoryTrackedDynamicArray implementation."""
    
    def setUp(self):
        self.array = MemoryTrackedDynamicArray[int]()
    
    def test_memory_tracking_initialization(self):
        """Test memory tracking initialization."""
        self.assertEqual(self.array._resize_count, 0)
        self.assertEqual(self.array._total_allocations, 0)
    
    def test_resize_tracking(self):
        """Test that resizes are tracked."""
        # Force resize
        for i in range(10):
            self.array.append(i)
        
        self.assertGreater(self.array._resize_count, 0)
        self.assertGreater(self.array._total_allocations, 0)
    
    def test_get_memory_info(self):
        """Test memory info retrieval."""
        # Add some items
        for i in range(5):
            self.array.append(i)
        
        memory_info = self.array.get_memory_info()
        
        self.assertIsInstance(memory_info.object_size, int)
        self.assertIsInstance(memory_info.total_size, int)
        self.assertIsInstance(memory_info.overhead, int)
        self.assertIsInstance(memory_info.capacity, int)
        self.assertIsInstance(memory_info.load_factor, float)
        
        self.assertGreater(memory_info.object_size, 0)
        self.assertGreaterEqual(memory_info.total_size, 0)
        self.assertGreater(memory_info.capacity, 0)
        self.assertGreaterEqual(memory_info.load_factor, 0)
        self.assertLessEqual(memory_info.load_factor, 1)
    
    def test_memory_info_accuracy(self):
        """Test memory info accuracy."""
        # Add items and check memory info
        for i in range(3):
            self.array.append(i)
        
        memory_info = self.array.get_memory_info()
        
        # Check that load factor is correct
        expected_load_factor = 3 / self.array._capacity
        self.assertAlmostEqual(memory_info.load_factor, expected_load_factor, places=6)
        
        # Check that capacity matches
        self.assertEqual(memory_info.capacity, self.array._capacity)


class TestDynamicArrayPerformance(unittest.TestCase):
    """Performance tests for DynamicArray."""
    
    def test_append_performance(self):
        """Test append performance."""
        array = DynamicArray[int]()
        
        # Time append operations
        start_time = timeit.default_timer()
        for i in range(1000):
            array.append(i)
        end_time = timeit.default_timer()
        
        append_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(append_time, 1.0)
        self.assertEqual(len(array), 1000)
    
    def test_access_performance(self):
        """Test access performance."""
        array = DynamicArray[int]()
        
        # Fill array
        for i in range(1000):
            array.append(i)
        
        # Time access operations
        start_time = timeit.default_timer()
        for i in range(1000):
            _ = array[i]
        end_time = timeit.default_timer()
        
        access_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(access_time, 1.0)
    
    def test_iteration_performance(self):
        """Test iteration performance."""
        array = DynamicArray[int]()
        
        # Fill array
        for i in range(1000):
            array.append(i)
        
        # Time iteration
        start_time = timeit.default_timer()
        items = list(array)
        end_time = timeit.default_timer()
        
        iteration_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(iteration_time, 1.0)
        self.assertEqual(len(items), 1000)


class TestDynamicArrayEdgeCases(unittest.TestCase):
    """Edge case tests for DynamicArray."""
    
    def test_large_number_of_items(self):
        """Test with a large number of items."""
        array = DynamicArray[int]()
        
        # Add many items
        for i in range(10000):
            array.append(i)
        
        self.assertEqual(len(array), 10000)
        
        # Verify random access
        self.assertEqual(array[0], 0)
        self.assertEqual(array[5000], 5000)
        self.assertEqual(array[9999], 9999)
    
    def test_none_values(self):
        """Test handling of None values."""
        array = DynamicArray[type(None)]()
        
        array.append(None)
        array.append(None)
        
        self.assertEqual(len(array), 2)
        self.assertIsNone(array[0])
        self.assertIsNone(array[1])
    
    def test_string_values(self):
        """Test handling of string values."""
        array = DynamicArray[str]()
        
        strings = ["hello", "world", "python", "data", "structures"]
        for s in strings:
            array.append(s)
        
        self.assertEqual(len(array), len(strings))
        for i, s in enumerate(strings):
            self.assertEqual(array[i], s)
    
    def test_mixed_types(self):
        """Test handling of mixed types (using object as type)."""
        array = DynamicArray[object]()
        
        items = [1, "hello", 3.14, None, [1, 2, 3]]
        for item in items:
            array.append(item)
        
        self.assertEqual(len(array), len(items))
        for i, item in enumerate(items):
            self.assertEqual(array[i], item)


if __name__ == '__main__':
    unittest.main(verbosity=2) 