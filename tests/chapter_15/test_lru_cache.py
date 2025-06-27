import unittest
import timeit
import random
from mastering_performant_code.chapter_15.lru_cache import LRUCacheOrderedDict, LRUCacheDLL

class TestLRUCacheOrderedDict(unittest.TestCase):
    """Comprehensive test suite for LRU cache using OrderedDict."""
    
    def setUp(self):
        self.cache = LRUCacheOrderedDict(3)
    
    def test_init_validation(self):
        """Test initialization with invalid parameters."""
        with self.assertRaises(ValueError):
            LRUCacheOrderedDict(0)
        
        with self.assertRaises(ValueError):
            LRUCacheOrderedDict(-1)
    
    def test_basic_operations(self):
        """Test basic put and get operations."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.assertEqual(self.cache.get("a"), 1)
        self.assertEqual(self.cache.get("b"), 2)
        self.assertIsNone(self.cache.get("c"))
    
    def test_eviction_policy(self):
        """Test LRU eviction when cache is full."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        self.cache.put("d", 4)  # Should evict "a" (LRU)
        
        self.assertIsNone(self.cache.get("a"))
        self.assertEqual(self.cache.get("b"), 2)
        self.assertEqual(self.cache.get("c"), 3)
        self.assertEqual(self.cache.get("d"), 4)
    
    def test_access_order_update(self):
        """Test that accessing an item makes it most recently used."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        
        # Access "a" to make it most recently used
        self.cache.get("a")
        
        # Add new item, should evict "b" (now LRU)
        self.cache.put("d", 4)
        
        self.assertEqual(self.cache.get("a"), 1)  # Should still be there
        self.assertIsNone(self.cache.get("b"))    # Should be evicted
        self.assertEqual(self.cache.get("c"), 3)
        self.assertEqual(self.cache.get("d"), 4)
    
    def test_statistics_tracking(self):
        """Test statistics collection."""
        self.cache.put("a", 1)
        self.cache.get("a")  # Hit
        self.cache.get("b")  # Miss
        
        self.assertEqual(self.cache.stats['hits'], 1)
        self.assertEqual(self.cache.stats['misses'], 1)
        self.assertEqual(self.cache.stats['total_requests'], 2)
        self.assertEqual(self.cache.get_hit_ratio(), 0.5)
    
    def test_eviction_statistics(self):
        """Test eviction statistics tracking."""
        # Fill cache to capacity
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        
        # Add one more to trigger eviction
        self.cache.put("d", 4)
        
        self.assertEqual(self.cache.stats['evictions'], 1)
    
    def test_performance_benchmark(self):
        """Test performance with timing."""
        cache = LRUCacheOrderedDict(1000)
        
        # Benchmark put operations
        put_time = timeit.timeit(
            lambda: [cache.put(f"key_{i}", f"value_{i}") for i in range(1000)],
            number=10
        )
        
        # Benchmark get operations
        get_time = timeit.timeit(
            lambda: [cache.get(f"key_{i}") for i in range(1000)],
            number=10
        )
        
        # Verify reasonable performance
        self.assertLess(put_time, 1.0)  # Less than 1 second for 10k operations
        self.assertLess(get_time, 1.0)  # Less than 1 second for 10k operations
    
    def test_memory_usage(self):
        """Test memory usage calculation."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        
        memory = self.cache.get_memory_usage()
        self.assertGreater(memory, 0)
        self.assertIsInstance(memory, int)
    
    def test_large_dataset(self):
        """Test with large dataset."""
        large_cache = LRUCacheOrderedDict(1000)
        
        # Add many items
        for i in range(1500):  # More than capacity
            large_cache.put(f"key_{i}", f"value_{i}")
        
        # Should not exceed capacity
        self.assertLessEqual(len(large_cache), 1000)
        
        # Most recent items should still be present
        for i in range(1000, 1500):
            self.assertEqual(large_cache.get(f"key_{i}"), f"value_{i}")
    
    def test_different_data_types(self):
        """Test with various data types."""
        test_items = [
            ("string", "value"),
            (42, "number"),
            ((1, 2, 3), "tuple"),
            (frozenset([1, 2, 3]), "frozenset"),
            (None, "none_key"),
            ("", "empty_string")
        ]
        
        for key, value in test_items:
            self.cache.put(key, value)
            self.assertEqual(self.cache.get(key), value)
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Single item cache
        single_cache = LRUCacheOrderedDict(1)
        single_cache.put("a", 1)
        single_cache.put("b", 2)  # Should evict "a"
        self.assertIsNone(single_cache.get("a"))
        self.assertEqual(single_cache.get("b"), 2)
        
        # Update existing key
        self.cache.put("a", 1)
        self.cache.put("a", 2)  # Update value
        self.assertEqual(self.cache.get("a"), 2)
        
        # Zero capacity cache
        zero_cache = LRUCacheOrderedDict(1)
        zero_cache.put("a", 1)
        zero_cache.put("b", 2)  # Should evict "a" immediately
        self.assertIsNone(zero_cache.get("a"))
    
    def test_clear_stats(self):
        """Test statistics clearing."""
        self.cache.put("a", 1)
        self.cache.get("a")
        self.cache.get("b")
        
        # Verify stats are populated
        self.assertGreater(self.cache.stats['total_requests'], 0)
        
        # Clear stats
        self.cache.clear_stats()
        
        # Verify stats are reset
        self.assertEqual(self.cache.stats['total_requests'], 0)
        self.assertEqual(self.cache.stats['hits'], 0)
        self.assertEqual(self.cache.stats['misses'], 0)
        self.assertEqual(self.cache.stats['evictions'], 0)
    
    def test_get_stats(self):
        """Test comprehensive statistics retrieval."""
        self.cache.put("a", 1)
        self.cache.get("a")
        self.cache.get("b")
        
        stats = self.cache.get_stats()
        
        # Verify all expected keys are present
        expected_keys = ['hits', 'misses', 'evictions', 'total_requests', 
                        'hit_ratio', 'size', 'capacity', 'memory_usage']
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Verify data types
        self.assertIsInstance(stats['hit_ratio'], float)
        self.assertIsInstance(stats['size'], int)
        self.assertIsInstance(stats['capacity'], int)
        self.assertIsInstance(stats['memory_usage'], int)
    
    def test_magic_methods(self):
        """Test magic methods."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        
        # Test __len__
        self.assertEqual(len(self.cache), 2)
        
        # Test __contains__
        self.assertIn("a", self.cache)
        self.assertNotIn("c", self.cache)
        
        # Test __repr__
        repr_str = repr(self.cache)
        self.assertIn("LRUCache", repr_str)
        self.assertIn("capacity=3", repr_str)
        self.assertIn("size=2", repr_str)
    
    def test_concurrent_access_pattern(self):
        """Test realistic concurrent access patterns."""
        cache = LRUCacheOrderedDict(10)
        
        # Simulate mixed read/write workload
        for i in range(100):
            # 70% reads, 30% writes
            if random.random() < 0.7:
                # Read operation
                key = f"key_{random.randint(0, 20)}"
                cache.get(key)
            else:
                # Write operation
                key = f"key_{random.randint(0, 20)}"
                value = f"value_{i}"
                cache.put(key, value)
        
        # Verify cache is still functional
        self.assertLessEqual(len(cache), 10)
        self.assertGreater(cache.stats['total_requests'], 0)

class TestLRUCacheDLL(unittest.TestCase):
    """Comprehensive test suite for LRU cache using doubly-linked list."""
    
    def setUp(self):
        self.cache = LRUCacheDLL(3)
    
    def test_init_validation(self):
        """Test initialization with invalid parameters."""
        with self.assertRaises(ValueError):
            LRUCacheDLL(0)
        
        with self.assertRaises(ValueError):
            LRUCacheDLL(-1)
    
    def test_basic_operations(self):
        """Test basic put and get operations."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.assertEqual(self.cache.get("a"), 1)
        self.assertEqual(self.cache.get("b"), 2)
        self.assertIsNone(self.cache.get("c"))
    
    def test_eviction_policy(self):
        """Test LRU eviction when cache is full."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        self.cache.put("d", 4)  # Should evict "a" (LRU)
        
        self.assertIsNone(self.cache.get("a"))
        self.assertEqual(self.cache.get("b"), 2)
        self.assertEqual(self.cache.get("c"), 3)
        self.assertEqual(self.cache.get("d"), 4)
    
    def test_access_order_update(self):
        """Test that accessing an item makes it most recently used."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        
        # Access "a" to make it most recently used
        self.cache.get("a")
        
        # Add new item, should evict "b" (now LRU)
        self.cache.put("d", 4)
        
        self.assertEqual(self.cache.get("a"), 1)  # Should still be there
        self.assertIsNone(self.cache.get("b"))    # Should be evicted
        self.assertEqual(self.cache.get("c"), 3)
        self.assertEqual(self.cache.get("d"), 4)
    
    def test_statistics_tracking(self):
        """Test statistics collection."""
        self.cache.put("a", 1)
        self.cache.get("a")  # Hit
        self.cache.get("b")  # Miss
        
        self.assertEqual(self.cache.stats['hits'], 1)
        self.assertEqual(self.cache.stats['misses'], 1)
        self.assertEqual(self.cache.stats['total_requests'], 2)
        self.assertEqual(self.cache.get_hit_ratio(), 0.5)
    
    def test_eviction_statistics(self):
        """Test eviction statistics tracking."""
        # Fill cache to capacity
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        self.cache.put("c", 3)
        
        # Add one more to trigger eviction
        self.cache.put("d", 4)
        
        self.assertEqual(self.cache.stats['evictions'], 1)
    
    def test_performance_benchmark(self):
        """Test performance with timing."""
        cache = LRUCacheDLL(1000)
        
        # Benchmark put operations
        put_time = timeit.timeit(
            lambda: [cache.put(f"key_{i}", f"value_{i}") for i in range(1000)],
            number=10
        )
        
        # Benchmark get operations
        get_time = timeit.timeit(
            lambda: [cache.get(f"key_{i}") for i in range(1000)],
            number=10
        )
        
        # Verify reasonable performance
        self.assertLess(put_time, 1.0)  # Less than 1 second for 10k operations
        self.assertLess(get_time, 1.0)  # Less than 1 second for 10k operations
    
    def test_memory_usage(self):
        """Test memory usage calculation."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        
        memory = self.cache.get_memory_usage()
        self.assertGreater(memory, 0)
        self.assertIsInstance(memory, int)
    
    def test_large_dataset(self):
        """Test with large dataset."""
        large_cache = LRUCacheDLL(1000)
        
        # Add many items
        for i in range(1500):  # More than capacity
            large_cache.put(f"key_{i}", f"value_{i}")
        
        # Should not exceed capacity
        self.assertLessEqual(len(large_cache), 1000)
        
        # Most recent items should still be present
        for i in range(1000, 1500):
            self.assertEqual(large_cache.get(f"key_{i}"), f"value_{i}")
    
    def test_different_data_types(self):
        """Test with various data types."""
        test_items = [
            ("string", "value"),
            (42, "number"),
            ((1, 2, 3), "tuple"),
            (frozenset([1, 2, 3]), "frozenset"),
            (None, "none_key"),
            ("", "empty_string")
        ]
        
        for key, value in test_items:
            self.cache.put(key, value)
            self.assertEqual(self.cache.get(key), value)
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Single item cache
        single_cache = LRUCacheDLL(1)
        single_cache.put("a", 1)
        single_cache.put("b", 2)  # Should evict "a"
        self.assertIsNone(single_cache.get("a"))
        self.assertEqual(single_cache.get("b"), 2)
        
        # Update existing key
        self.cache.put("a", 1)
        self.cache.put("a", 2)  # Update value
        self.assertEqual(self.cache.get("a"), 2)
    
    def test_clear_stats(self):
        """Test statistics clearing."""
        self.cache.put("a", 1)
        self.cache.get("a")
        self.cache.get("b")
        
        # Verify stats are populated
        self.assertGreater(self.cache.stats['total_requests'], 0)
        
        # Clear stats
        self.cache.clear_stats()
        
        # Verify stats are reset
        self.assertEqual(self.cache.stats['total_requests'], 0)
        self.assertEqual(self.cache.stats['hits'], 0)
        self.assertEqual(self.cache.stats['misses'], 0)
        self.assertEqual(self.cache.stats['evictions'], 0)
    
    def test_get_stats(self):
        """Test comprehensive statistics retrieval."""
        self.cache.put("a", 1)
        self.cache.get("a")
        self.cache.get("b")
        
        stats = self.cache.get_stats()
        
        # Verify all expected keys are present
        expected_keys = ['hits', 'misses', 'evictions', 'total_requests', 
                        'hit_ratio', 'size', 'capacity', 'memory_usage']
        for key in expected_keys:
            self.assertIn(key, stats)
        
        # Verify data types
        self.assertIsInstance(stats['hit_ratio'], float)
        self.assertIsInstance(stats['size'], int)
        self.assertIsInstance(stats['capacity'], int)
        self.assertIsInstance(stats['memory_usage'], int)
    
    def test_magic_methods(self):
        """Test magic methods."""
        self.cache.put("a", 1)
        self.cache.put("b", 2)
        
        # Test __len__
        self.assertEqual(len(self.cache), 2)
        
        # Test __contains__
        self.assertIn("a", self.cache)
        self.assertNotIn("c", self.cache)
        
        # Test __repr__
        repr_str = repr(self.cache)
        self.assertIn("LRUCacheDLL", repr_str)
        self.assertIn("capacity=3", repr_str)
        self.assertIn("size=2", repr_str)
    
    def test_concurrent_access_pattern(self):
        """Test realistic concurrent access patterns."""
        cache = LRUCacheDLL(10)
        
        # Simulate mixed read/write workload
        for i in range(100):
            # 70% reads, 30% writes
            if random.random() < 0.7:
                # Read operation
                key = f"key_{random.randint(0, 20)}"
                cache.get(key)
            else:
                # Write operation
                key = f"key_{random.randint(0, 20)}"
                value = f"value_{i}"
                cache.put(key, value)
        
        # Verify cache is still functional
        self.assertLessEqual(len(cache), 10)
        self.assertGreater(cache.stats['total_requests'], 0)

if __name__ == '__main__':
    unittest.main() 