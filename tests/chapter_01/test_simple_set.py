"""
Unit tests for SimpleSet implementation.

This module provides comprehensive test coverage for the SimpleSet class,
including set operations, edge cases, and performance tests.
"""

import unittest
import sys
import timeit
from typing import Set

# Add the code directory to the path for imports
sys.path.insert(0, '../../src')

from src.chapter_01.simple_set import SimpleSet

class TestSimpleSet(unittest.TestCase):
    """Test cases for SimpleSet implementation."""
    
    def setUp(self):
        self.set = SimpleSet[int]()
    
    def test_initialization(self):
        """Test set initialization."""
        self.assertEqual(len(self.set), 0)
        
        # Test initialization with iterable
        items = [1, 2, 3, 4, 5]
        set_with_items = SimpleSet[int](items)
        self.assertEqual(len(set_with_items), 5)
        for item in items:
            self.assertIn(item, set_with_items)
    
    def test_add_contains(self):
        """Test add and contains operations."""
        self.set.add(1)
        self.set.add(2)
        
        self.assertIn(1, self.set)
        self.assertIn(2, self.set)
        self.assertNotIn(3, self.set)
        self.assertEqual(len(self.set), 2)
    
    def test_remove(self):
        """Test remove operation."""
        self.set.add(1)
        self.set.remove(1)
        
        self.assertNotIn(1, self.set)
        self.assertEqual(len(self.set), 0)
    
    def test_remove_key_error(self):
        """Test KeyError on remove missing item."""
        with self.assertRaises(KeyError):
            self.set.remove(1)
    
    def test_discard(self):
        """Test discard operation."""
        self.set.add(1)
        self.set.discard(1)
        self.set.discard(2)  # Should not raise error
        
        self.assertNotIn(1, self.set)
        self.assertEqual(len(self.set), 0)
    
    def test_iteration(self):
        """Test iteration over set."""
        items = [1, 2, 3, 4, 5]
        for item in items:
            self.set.add(item)
        
        self.assertEqual(set(self.set), set(items))
    
    def test_repr(self):
        """Test string representation."""
        self.assertEqual(repr(self.set), "SimpleSet({})")
        
        self.set.add(1)
        self.set.add(2)
        # Note: order may vary due to hash table iteration
        self.assertIn("SimpleSet({", repr(self.set))
        self.assertIn("1", repr(self.set))
        self.assertIn("2", repr(self.set))
    
    def test_duplicate_add(self):
        """Test adding duplicate items."""
        self.set.add(1)
        self.set.add(1)  # Duplicate
        
        self.assertEqual(len(self.set), 1)
        self.assertIn(1, self.set)
    
    def test_multiple_operations(self):
        """Test multiple operations in sequence."""
        # Add items
        for i in range(10):
            self.set.add(i)
        
        self.assertEqual(len(self.set), 10)
        
        # Remove some items
        for i in range(0, 10, 2):
            self.set.remove(i)
        
        self.assertEqual(len(self.set), 5)
        
        # Check remaining items
        for i in range(1, 10, 2):
            self.assertIn(i, self.set)
        
        for i in range(0, 10, 2):
            self.assertNotIn(i, self.set)


class TestSimpleSetOperations(unittest.TestCase):
    """Test cases for set operations."""
    
    def test_union(self):
        """Test union operation."""
        set1 = SimpleSet[int]([1, 2, 3])
        set2 = SimpleSet[int]([2, 3, 4])
        
        union = set1.union(set2)
        
        self.assertEqual(set(union), {1, 2, 3, 4})
        self.assertEqual(len(union), 4)
    
    def test_intersection(self):
        """Test intersection operation."""
        set1 = SimpleSet[int]([1, 2, 3, 4])
        set2 = SimpleSet[int]([2, 3, 4, 5])
        
        intersection = set1.intersection(set2)
        
        self.assertEqual(set(intersection), {2, 3, 4})
        self.assertEqual(len(intersection), 3)
    
    def test_difference(self):
        """Test difference operation."""
        set1 = SimpleSet[int]([1, 2, 3, 4])
        set2 = SimpleSet[int]([2, 3, 5])
        
        difference = set1.difference(set2)
        
        self.assertEqual(set(difference), {1, 4})
        self.assertEqual(len(difference), 2)
    
    def test_empty_set_operations(self):
        """Test set operations with empty sets."""
        empty_set = SimpleSet[int]()
        non_empty_set = SimpleSet[int]([1, 2, 3])
        
        # Union with empty set
        union = empty_set.union(non_empty_set)
        self.assertEqual(set(union), {1, 2, 3})
        
        # Intersection with empty set
        intersection = empty_set.intersection(non_empty_set)
        self.assertEqual(set(intersection), set())
        
        # Difference with empty set
        difference = empty_set.difference(non_empty_set)
        self.assertEqual(set(difference), set())
        
        # Difference from non-empty set
        difference2 = non_empty_set.difference(empty_set)
        self.assertEqual(set(difference2), {1, 2, 3})
    
    def test_disjoint_sets(self):
        """Test operations on disjoint sets."""
        set1 = SimpleSet[int]([1, 2, 3])
        set2 = SimpleSet[int]([4, 5, 6])
        
        union = set1.union(set2)
        intersection = set1.intersection(set2)
        difference = set1.difference(set2)
        
        self.assertEqual(set(union), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(intersection), set())
        self.assertEqual(set(difference), {1, 2, 3})
    
    def test_identical_sets(self):
        """Test operations on identical sets."""
        set1 = SimpleSet[int]([1, 2, 3])
        set2 = SimpleSet[int]([1, 2, 3])
        
        union = set1.union(set2)
        intersection = set1.intersection(set2)
        difference = set1.difference(set2)
        
        self.assertEqual(set(union), {1, 2, 3})
        self.assertEqual(set(intersection), {1, 2, 3})
        self.assertEqual(set(difference), set())


class TestSimpleSetPerformance(unittest.TestCase):
    """Performance tests for SimpleSet."""
    
    def test_add_performance(self):
        """Test add performance."""
        set_obj = SimpleSet[int]()
        
        # Time add operations
        start_time = timeit.default_timer()
        for i in range(1000):
            set_obj.add(i)
        end_time = timeit.default_timer()
        
        add_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(add_time, 1.0)
        self.assertEqual(len(set_obj), 1000)
    
    def test_contains_performance(self):
        """Test contains performance."""
        set_obj = SimpleSet[int]()
        
        # Fill set
        for i in range(1000):
            set_obj.add(i)
        
        # Time contains operations
        start_time = timeit.default_timer()
        for i in range(1000):
            _ = i in set_obj
        end_time = timeit.default_timer()
        
        contains_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(contains_time, 1.0)
    
    def test_iteration_performance(self):
        """Test iteration performance."""
        set_obj = SimpleSet[int]()
        
        # Fill set
        for i in range(1000):
            set_obj.add(i)
        
        # Time iteration
        start_time = timeit.default_timer()
        items = list(set_obj)
        end_time = timeit.default_timer()
        
        iteration_time = end_time - start_time
        
        # Should complete in reasonable time (less than 1 second)
        self.assertLess(iteration_time, 1.0)
        self.assertEqual(len(items), 1000)
    
    def test_set_operations_performance(self):
        """Test set operations performance."""
        set1 = SimpleSet[int](range(500))
        set2 = SimpleSet[int](range(250, 750))
        
        # Time union
        start_time = timeit.default_timer()
        union = set1.union(set2)
        end_time = timeit.default_timer()
        
        union_time = end_time - start_time
        self.assertLess(union_time, 1.0)
        
        # Time intersection
        start_time = timeit.default_timer()
        intersection = set1.intersection(set2)
        end_time = timeit.default_timer()
        
        intersection_time = end_time - start_time
        self.assertLess(intersection_time, 1.0)
        
        # Time difference
        start_time = timeit.default_timer()
        difference = set1.difference(set2)
        end_time = timeit.default_timer()
        
        difference_time = end_time - start_time
        self.assertLess(difference_time, 1.0)


class TestSimpleSetEdgeCases(unittest.TestCase):
    """Edge case tests for SimpleSet."""
    
    def setUp(self):
        self.set = SimpleSet[int]()
    
    def test_large_number_of_items(self):
        """Test with a large number of items."""
        set_obj = SimpleSet[int]()
        
        # Add many items
        for i in range(10000):
            set_obj.add(i)
        
        self.assertEqual(len(set_obj), 10000)
        
        # Verify random access
        self.assertIn(0, set_obj)
        self.assertIn(5000, set_obj)
        self.assertIn(9999, set_obj)
        self.assertNotIn(10000, set_obj)
    
    def test_none_values(self):
        """Test handling of None values."""
        set_obj = SimpleSet[type(None)]()
        
        set_obj.add(None)
        set_obj.add(None)  # Duplicate
        
        self.assertEqual(len(set_obj), 1)
        self.assertIn(None, set_obj)
    
    def test_string_values(self):
        """Test handling of string values."""
        set_obj = SimpleSet[str]()
        
        strings = ["hello", "world", "python", "data", "structures"]
        for s in strings:
            set_obj.add(s)
        
        self.assertEqual(len(set_obj), len(strings))
        for s in strings:
            self.assertIn(s, set_obj)
    
    def test_mixed_types(self):
        """Test handling of mixed types (using object as type)."""
        set_obj = SimpleSet[object]()
        
        # Use hashable objects only
        items = [1, "hello", 3.14, None, (1, 2, 3)]
        for item in items:
            set_obj.add(item)
        
        self.assertEqual(len(set_obj), len(items))
        for item in items:
            self.assertIn(item, set_obj)
    
    def test_empty_set_operations(self):
        """Test operations on empty set."""
        self.assertEqual(len(self.set), 0)
        self.assertEqual(list(self.set), [])
        self.assertEqual(repr(self.set), "SimpleSet({})")
        
        with self.assertRaises(KeyError):
            self.set.remove(1)
        
        # Discard should not raise error
        self.set.discard(1)
    
    def test_self_operations(self):
        """Test set operations with self."""
        set_obj = SimpleSet[int]([1, 2, 3])
        
        # Union with self
        union = set_obj.union(set_obj)
        self.assertEqual(set(union), {1, 2, 3})
        
        # Intersection with self
        intersection = set_obj.intersection(set_obj)
        self.assertEqual(set(intersection), {1, 2, 3})
        
        # Difference with self
        difference = set_obj.difference(set_obj)
        self.assertEqual(set(difference), set())


if __name__ == '__main__':
    unittest.main(verbosity=2) 