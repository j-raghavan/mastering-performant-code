"""
Unit tests for HashTable implementation.

This module provides comprehensive test coverage for the HashTable class,
including edge cases, collision handling, and performance tests.

Enhanced test coverage includes:
- Hash collision scenarios that could cause clustering
- Memory pressure scenarios under constraints
- Unicode edge cases with various character sets
- Performance regression testing
"""

import unittest
import timeit
import gc
import os
from typing import Dict

from chapter_01.hash_table import HashTable, MemoryTrackedHashTable

class TestHashTable(unittest.TestCase):
    """Test cases for HashTable implementation."""
    
    def setUp(self):
        self.table = HashTable[str, int]()
    
    def test_initialization(self):
        """Test hash table initialization."""
        self.assertEqual(len(self.table), 0)
        self.assertEqual(self.table._capacity, 8)
        self.assertEqual(self.table._load_factor, 0.75)
        
        # Test custom initialization
        custom_table = HashTable[str, int](16, 0.5)
        self.assertEqual(custom_table._capacity, 16)
        self.assertEqual(custom_table._load_factor, 0.5)
    
    def test_set_get(self):
        """Test set and get operations."""
        self.table["key1"] = 42
        self.table["key2"] = 100
        
        self.assertEqual(self.table["key1"], 42)
        self.assertEqual(self.table["key2"], 100)
        self.assertEqual(len(self.table), 2)
    
    def test_key_error(self):
        """Test KeyError on missing key."""
        with self.assertRaises(KeyError):
            _ = self.table["missing"]
    
    def test_delete(self):
        """Test delete operation."""
        self.table["key1"] = 42
        del self.table["key1"]
        
        self.assertEqual(len(self.table), 0)
        self.assertNotIn("key1", self.table)
    
    def test_delete_key_error(self):
        """Test KeyError on delete missing key."""
        with self.assertRaises(KeyError):
            del self.table["missing"]
    
    def test_contains(self):
        """Test contains operation."""
        self.table["key1"] = 42
        
        self.assertIn("key1", self.table)
        self.assertNotIn("key2", self.table)
    
    def test_resize(self):
        """Test automatic resizing."""
        # Add enough items to trigger resize
        for i in range(10):
            self.table[f"key{i}"] = i
        
        self.assertEqual(len(self.table), 10)
        self.assertGreater(self.table._capacity, 8)
        
        # Verify all items are still accessible
        for i in range(10):
            self.assertEqual(self.table[f"key{i}"], i)
    
    def test_collision_handling(self):
        """Test collision handling."""
        # Force collisions by using keys that hash to same value
        class CollisionKey:
            def __init__(self, value):
                self.value = value
            
            def __hash__(self):
                return 42  # Force same hash for all instances
            
            def __eq__(self, other):
                return isinstance(other, CollisionKey) and self.value == other.value
        
        table = HashTable[CollisionKey, int]()
        table[CollisionKey("a")] = 1
        table[CollisionKey("b")] = 2
        
        self.assertEqual(table[CollisionKey("a")], 1)
        self.assertEqual(table[CollisionKey("b")], 2)
        self.assertEqual(len(table), 2)
    
    def test_iteration(self):
        """Test iteration over hash table."""
        self.table["a"] = 1
        self.table["b"] = 2
        self.table["c"] = 3
        
        keys = set(self.table)
        self.assertEqual(keys, {"a", "b", "c"})
    
    def test_items(self):
        """Test items iteration."""
        self.table["a"] = 1
        self.table["b"] = 2
        self.table["c"] = 3
        
        items = dict(self.table.items())
        self.assertEqual(items, {"a": 1, "b": 2, "c": 3})
    
    def test_repr(self):
        """Test string representation."""
        self.assertEqual(repr(self.table), "HashTable({})")
        
        self.table["a"] = 1
        self.table["b"] = 2
        # Note: order may vary due to hash table iteration
        self.assertIn("HashTable({", repr(self.table))
        self.assertIn("'a': 1", repr(self.table))
        self.assertIn("'b': 2", repr(self.table))
    
    def test_update_existing_key(self):
        """Test updating existing key."""
        self.table["key1"] = 42
        self.table["key1"] = 100
        
        self.assertEqual(self.table["key1"], 100)
        self.assertEqual(len(self.table), 1)
    
    def test_delete_and_reinsert(self):
        """Test delete and reinsert of same key."""
        self.table["key1"] = 42
        del self.table["key1"]
        self.table["key1"] = 100
        
        self.assertEqual(self.table["key1"], 100)
        self.assertEqual(len(self.table), 1)
    
    def test_multiple_resizes(self):
        """Test multiple resize operations."""
        # Force multiple resizes
        for i in range(100):
            self.table[f"key{i}"] = i
        
        self.assertEqual(len(self.table), 100)
        self.assertGreater(self.table._capacity, 100)
        
        # Verify all items are correct
        for i in range(100):
            self.assertEqual(self.table[f"key{i}"], i)
    
    def test_get_load_factor(self):
        """Test load factor calculation."""
        self.assertEqual(self.table.get_load_factor(), 0.0)
        
        self.table["key1"] = 1
        self.assertEqual(self.table.get_load_factor(), 1.0 / 8.0)
        
        # Fill to capacity to trigger resize
        for i in range(8):
            self.table[f"key{i}"] = i
        
        # After resize, load factor should be less than threshold (0.75)
        self.assertLess(self.table.get_load_factor(), self.table._load_factor)
    
    def test_get_capacity(self):
        """Test capacity retrieval."""
        self.assertEqual(self.table.get_capacity(), 8)
        
        # Force resize
        for i in range(10):
            self.table[f"key{i}"] = i
        
        self.assertGreater(self.table.get_capacity(), 8)


class TestHashCollisionScenarios(unittest.TestCase):
    """Test specific collision patterns that could cause clustering."""
    
    def test_hash_collision_scenarios(self):
        """Test specific collision patterns that could cause clustering."""
        
        # Test 1: Sequential hash values that could cause clustering
        class SequentialHashKey:
            def __init__(self, value, base_hash=0):
                self.value = value
                self.base_hash = base_hash
            
            def __hash__(self):
                return self.base_hash + hash(self.value)
            
            def __eq__(self, other):
                return isinstance(other, SequentialHashKey) and self.value == other.value
        
        table = HashTable[SequentialHashKey, int]()
        
        # Create keys with sequential hashes that could cluster
        for i in range(20):
            key = SequentialHashKey(f"key{i}", i * 8)  # Sequential hashes
            table[key] = i
        
        # Verify all items are accessible
        for i in range(20):
            key = SequentialHashKey(f"key{i}", i * 8)
            self.assertEqual(table[key], i)
        
        # Test 2: Keys that hash to adjacent positions
        class AdjacentHashKey:
            def __init__(self, value, offset=0):
                self.value = value
                self.offset = offset
            
            def __hash__(self):
                return (hash(self.value) + self.offset) % 8  # Force adjacent positions
            
            def __eq__(self, other):
                return isinstance(other, AdjacentHashKey) and self.value == other.value
        
        table2 = HashTable[AdjacentHashKey, int]()
        
        # Create keys that hash to adjacent positions
        for i in range(10):
            key = AdjacentHashKey(f"adjacent{i}", i)
            table2[key] = i * 10
        
        # Verify all items are accessible
        for i in range(10):
            key = AdjacentHashKey(f"adjacent{i}", i)
            self.assertEqual(table2[key], i * 10)
    
    def test_deletion_clustering(self):
        """Test that deletion doesn't cause clustering issues."""
        table = HashTable[str, int]()
        
        # Fill table
        for i in range(20):
            table[f"key{i}"] = i
        
        # Delete every other key
        for i in range(0, 20, 2):
            del table[f"key{i}"]
        
        # Verify remaining keys are accessible
        for i in range(1, 20, 2):
            self.assertEqual(table[f"key{i}"], i)
        
        # Verify deleted keys are gone
        for i in range(0, 20, 2):
            self.assertNotIn(f"key{i}", table)
        
        # Add new keys to test insertion after deletion
        for i in range(20, 30):
            table[f"newkey{i}"] = i
        
        # Verify all keys are accessible
        for i in range(1, 20, 2):
            self.assertEqual(table[f"key{i}"], i)
        for i in range(20, 30):
            self.assertEqual(table[f"newkey{i}"], i)


class TestMemoryPressureScenarios(unittest.TestCase):
    """Test behavior under memory constraints."""
    
    def test_memory_pressure_scenarios(self):
        """Test behavior under memory constraints."""
        
        # Test 1: Large number of small objects
        table = HashTable[str, str]()
        
        # Add many small strings
        for i in range(10000):
            table[f"key{i}"] = f"value{i}"
        
        # Force garbage collection
        gc.collect()
        
        # Verify all items are still accessible
        for i in range(10000):
            self.assertEqual(table[f"key{i}"], f"value{i}")
        
        # Test 2: Large objects
        table2 = HashTable[str, list]()
        
        # Add large lists
        for i in range(100):
            table2[f"largekey{i}"] = list(range(1000))
        
        # Force garbage collection
        gc.collect()
        
        # Verify all items are still accessible
        for i in range(100):
            self.assertEqual(len(table2[f"largekey{i}"]), 1000)
        
        # Test 3: Memory usage tracking
        tracked_table = MemoryTrackedHashTable[str, int]()
        
        # Add items and check memory stats
        for i in range(100):
            tracked_table[f"memkey{i}"] = i
        
        stats = tracked_table.get_statistics()
        self.assertGreater(stats['resize_count'], 0)
        self.assertGreater(stats['operation_count'], 0)
    
    def test_memory_efficiency(self):
        """Test memory efficiency of hash table."""
        table = HashTable[str, int]()
        
        # Measure initial memory
        initial_memory = sys.getsizeof(table._array)
        
        # Add items
        for i in range(100):
            table[f"effkey{i}"] = i
        
        # Measure final memory
        final_memory = sys.getsizeof(table._array)
        
        # Memory should grow but not excessively
        self.assertGreater(final_memory, initial_memory)
        self.assertLess(final_memory, initial_memory * 20)  # Reasonable growth


class TestUnicodeEdgeCases(unittest.TestCase):
    """Test with various Unicode edge cases."""
    
    def test_unicode_edge_cases(self):
        """Test with various Unicode edge cases."""
        table = HashTable[str, int]()
        
        # Test 1: Basic Unicode
        unicode_strings = [
            "café",  # Latin-1
            "привет",  # Cyrillic
            "こんにちは",  # Japanese
            "你好",  # Chinese
            "안녕하세요",  # Korean
            "مرحبا",  # Arabic
            "שָׁלוֹם",  # Hebrew
            "नमस्ते",  # Devanagari
        ]
        
        for i, text in enumerate(unicode_strings):
            table[text] = i
        
        # Verify all Unicode keys are accessible
        for i, text in enumerate(unicode_strings):
            self.assertEqual(table[text], i)
        
        # Test 2: Unicode combining characters
        combining_chars = [
            "e\u0301",  # e + combining acute accent
            "a\u0308",  # a + combining diaeresis
            "c\u0327",  # c + combining cedilla
        ]
        
        for i, text in enumerate(combining_chars):
            table[text] = i + 100
        
        # Verify combining character keys are accessible
        for i, text in enumerate(combining_chars):
            self.assertEqual(table[text], i + 100)
        
        # Test 3: Emoji and special characters
        special_chars = [
            "🚀",  # Rocket emoji
            "🎉",  # Party emoji
            "🌟",  # Star emoji
            "💻",  # Computer emoji
            "🔥",  # Fire emoji
        ]
        
        for i, char in enumerate(special_chars):
            table[char] = i + 200
        
        # Verify emoji keys are accessible
        for i, char in enumerate(special_chars):
            self.assertEqual(table[char], i + 200)
        
        # Test 4: Mixed Unicode and ASCII
        mixed_strings = [
            "hello世界",
            "приветworld",
            "こんにちはhello",
            "café☕",
            "test🚀test",
        ]
        
        for i, text in enumerate(mixed_strings):
            table[text] = i + 300
        
        # Verify mixed strings are accessible
        for i, text in enumerate(mixed_strings):
            self.assertEqual(table[text], i + 300)
    
    def test_unicode_normalization(self):
        """Test Unicode normalization edge cases."""
        table = HashTable[str, int]()
        
        # Test different Unicode normalizations of the same character
        # é can be represented as U+00E9 or U+0065 U+0301
        e_acute_1 = "é"  # U+00E9
        e_acute_2 = "e\u0301"  # U+0065 U+0301
        
        table[e_acute_1] = 1
        table[e_acute_2] = 2
        
        # These should be different keys
        self.assertEqual(table[e_acute_1], 1)
        self.assertEqual(table[e_acute_2], 2)
        self.assertNotEqual(e_acute_1, e_acute_2)


class TestMemoryTrackedHashTable(unittest.TestCase):
    """Test cases for MemoryTrackedHashTable implementation."""
    
    def setUp(self):
        self.table = MemoryTrackedHashTable[str, int]()
    
    def test_memory_tracking_initialization(self):
        """Test memory tracking initialization."""
        self.assertEqual(self.table._resize_count, 0)
        self.assertEqual(self.table._collision_count, 0)
    
    def test_resize_tracking(self):
        """Test that resizes are tracked."""
        # Force resize
        for i in range(10):
            self.table[f"key{i}"] = i
        
        self.assertGreater(self.table._resize_count, 0)
    
    def test_collision_tracking(self):
        """Test that collisions are tracked."""
        # Force collisions
        class CollisionKey:
            def __init__(self, value):
                self.value = value
            
            def __hash__(self):
                return 42
            
            def __eq__(self, other):
                return isinstance(other, CollisionKey) and self.value == other.value
        
        table = MemoryTrackedHashTable[CollisionKey, int]()
        table[CollisionKey("a")] = 1
        table[CollisionKey("b")] = 2
        
        self.assertGreater(table._collision_count, 0)
    
    def test_memory_info_accuracy(self):
        """Test that memory info is accurate."""
        self.table["key1"] = 42
        self.table["key2"] = 100
        
        memory_info = self.table.get_memory_info()
        
        self.assertGreater(memory_info.object_size, 0)
        self.assertGreater(memory_info.total_size, 0)
        self.assertEqual(memory_info.capacity, self.table._capacity)
        self.assertEqual(memory_info.load_factor, self.table.get_load_factor())
    
    def test_statistics_accuracy(self):
        """Test that statistics are accurate."""
        # Add some items to generate statistics
        for i in range(10):
            self.table[f"key{i}"] = i
        
        stats = self.table.get_statistics()
        
        self.assertGreater(stats['resize_count'], 0)
        self.assertGreater(stats['operation_count'], 0)
        self.assertGreater(stats['total_probes'], 0)
        self.assertGreaterEqual(stats['average_probe_length'], 0)
        self.assertGreaterEqual(stats['collision_rate'], 0)


class TestHashTablePerformance(unittest.TestCase):
    """Performance tests for HashTable implementation."""
    
    def test_set_performance(self):
        """Test set operation performance."""
        table = HashTable[str, int]()
        
        def set_operations():
            for i in range(1000):
                table[f"key{i}"] = i
        
        # Time the operations
        time_taken = timeit.timeit(set_operations, number=1)
        
        # Should complete in reasonable time (adjust threshold as needed)
        self.assertLess(time_taken, 1.0)  # Less than 1 second
        
        # Verify all items were set
        for i in range(1000):
            self.assertEqual(table[f"key{i}"], i)
    
    def test_get_performance(self):
        """Test get operation performance."""
        table = HashTable[str, int]()
        
        # Pre-populate table
        for i in range(1000):
            table[f"key{i}"] = i
        
        def get_operations():
            for i in range(1000):
                _ = table[f"key{i}"]
        
        # Time the operations
        time_taken = timeit.timeit(get_operations, number=1)
        
        # Should complete in reasonable time
        self.assertLess(time_taken, 1.0)
    
    def test_contains_performance(self):
        """Test contains operation performance."""
        table = HashTable[str, int]()
        
        # Pre-populate table
        for i in range(1000):
            table[f"key{i}"] = i
        
        def contains_operations():
            for i in range(1000):
                _ = f"key{i}" in table
        
        # Time the operations
        time_taken = timeit.timeit(contains_operations, number=1)
        
        # Should complete in reasonable time
        self.assertLess(time_taken, 1.0)


class TestHashTableEdgeCases(unittest.TestCase):
    """Edge case tests for HashTable implementation."""
    
    def setUp(self):
        self.table = HashTable[str, int]()
    
    def test_large_number_of_items(self):
        """Test with a large number of items."""
        # Add many items
        for i in range(10000):
            self.table[f"largekey{i}"] = i
        
        self.assertEqual(len(self.table), 10000)
        
        # Verify random access
        import random
        for _ in range(100):
            i = random.randint(0, 9999)
            self.assertEqual(self.table[f"largekey{i}"], i)
    
    def test_none_values(self):
        """Test with None values."""
        self.table["none_key"] = None
        self.assertIsNone(self.table["none_key"])
        self.assertIn("none_key", self.table)
    
    def test_none_keys(self):
        """Test with None keys."""
        self.table[None] = 42
        self.assertEqual(self.table[None], 42)
        self.assertIn(None, self.table)
    
    def test_string_values(self):
        """Test with string values."""
        self.table["string_key"] = "hello world"
        self.assertEqual(self.table["string_key"], "hello world")
    
    def test_mixed_types(self):
        """Test with mixed type keys and values."""
        # Test various key types
        self.table["string"] = 1
        self.table[42] = "number"
        self.table[3.14] = "float"
        self.table[True] = "boolean"
        self.table[False] = "boolean_false"
        
        # Test various value types
        self.table["list_value"] = [1, 2, 3]
        self.table["dict_value"] = {"a": 1, "b": 2}
        self.table["tuple_value"] = (1, 2, 3)
        
        # Verify all values
        self.assertEqual(self.table["string"], 1)
        self.assertEqual(self.table[42], "number")
        self.assertEqual(self.table[3.14], "float")
        self.assertEqual(self.table[True], "boolean")
        self.assertEqual(self.table[False], "boolean_false")
        self.assertEqual(self.table["list_value"], [1, 2, 3])
        self.assertEqual(self.table["dict_value"], {"a": 1, "b": 2})
        self.assertEqual(self.table["tuple_value"], (1, 2, 3))
    
    def test_empty_table_operations(self):
        """Test operations on empty table."""
        self.assertEqual(len(self.table), 0)
        self.assertNotIn("any_key", self.table)
        
        # Test iteration on empty table
        keys = list(self.table)
        self.assertEqual(keys, [])
        
        # Test items on empty table
        items = list(self.table.items())
        self.assertEqual(items, [])


if __name__ == '__main__':
    unittest.main() 