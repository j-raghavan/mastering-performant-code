"""
Unit tests for Bloom Filter implementation.

This module provides comprehensive tests for the BloomFilter class,
ensuring 100% code coverage and testing all edge cases.
"""

import pytest
import math
import sys
from typing import List, Any
from src.chapter_14.bloom_filter import BloomFilter


class TestBloomFilter:
    """Test cases for BloomFilter class."""
    
    def test_init_valid_parameters(self):
        """Test initialization with valid parameters."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        assert bf.expected_elements == 1000
        assert bf.false_positive_rate == 0.01
        assert bf.element_count == 0
        assert len(bf.bit_array) > 0
        assert len(bf.hash_seeds) > 0
    
    def test_init_invalid_expected_elements(self):
        """Test initialization with invalid expected elements."""
        with pytest.raises(ValueError, match="Expected elements must be positive"):
            BloomFilter(expected_elements=0, false_positive_rate=0.01)
        
        with pytest.raises(ValueError, match="Expected elements must be positive"):
            BloomFilter(expected_elements=-1, false_positive_rate=0.01)
    
    def test_init_invalid_false_positive_rate(self):
        """Test initialization with invalid false positive rate."""
        with pytest.raises(ValueError, match="False positive rate must be between 0 and 1"):
            BloomFilter(expected_elements=1000, false_positive_rate=0.0)
        
        with pytest.raises(ValueError, match="False positive rate must be between 0 and 1"):
            BloomFilter(expected_elements=1000, false_positive_rate=1.0)
        
        with pytest.raises(ValueError, match="False positive rate must be between 0 and 1"):
            BloomFilter(expected_elements=1000, false_positive_rate=1.5)
    
    def test_calculate_optimal_size(self):
        """Test optimal size calculation."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        # Test the formula: m = -n * ln(p) / (ln(2)^2)
        expected_size = int(-1000 * math.log(0.01) / (math.log(2) ** 2))
        assert bf.size == expected_size
    
    def test_calculate_optimal_hash_count(self):
        """Test optimal hash count calculation."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        # Test the formula: k = (m/n) * ln(2)
        expected_hash_count = max(1, int((bf.size / 1000) * math.log(2)))
        assert bf.hash_count == expected_hash_count
    
    def test_generate_hash_seeds(self):
        """Test hash seed generation."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        assert len(bf.hash_seeds) == bf.hash_count
        assert all(isinstance(seed, int) for seed in bf.hash_seeds)
        
        # Test that seeds are different
        assert len(set(bf.hash_seeds)) == len(bf.hash_seeds)
    
    def test_hash_functions(self):
        """Test hash function application."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        # Test with string
        positions = bf._hash_functions("test_item")
        assert len(positions) == bf.hash_count
        assert all(0 <= pos < bf.size for pos in positions)
        
        # Test with integer
        positions_int = bf._hash_functions(42)
        assert len(positions_int) == bf.hash_count
        assert all(0 <= pos < bf.size for pos in positions_int)
        
        # Test with list
        positions_list = bf._hash_functions([1, 2, 3])
        assert len(positions_list) == bf.hash_count
        assert all(0 <= pos < bf.size for pos in positions_list)
    
    def test_add_and_contains(self):
        """Test adding items and checking membership."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add items
        items = ["apple", "banana", "cherry", 42, [1, 2, 3]]
        
        for item in items:
            bf.add(item)
            assert bf.contains(item)
        
        assert len(bf) == len(items)
    
    def test_contains_nonexistent_items(self):
        """Test checking membership of items not in the filter."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add some items
        bf.add("apple")
        bf.add("banana")
        
        # Check non-existent items
        assert not bf.contains("grape")
        assert not bf.contains("orange")
        assert not bf.contains(42)
    
    def test_false_positives(self):
        """Test false positive behavior."""
        bf = BloomFilter(expected_elements=10, false_positive_rate=0.5)  # High FPR for testing
        
        # Add items
        test_items = [f"item_{i}" for i in range(5)]
        for item in test_items:
            bf.add(item)
        
        # Test non-member items
        non_member_items = [f"non_member_{i}" for i in range(20)]
        false_positives = sum(1 for item in non_member_items if bf.contains(item))
        
        # With high FPR, we expect some false positives
        assert false_positives > 0
    
    def test_get_false_positive_rate_empty(self):
        """Test false positive rate calculation for empty filter."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        assert bf.get_false_positive_rate() == 0.0
    
    def test_get_false_positive_rate_with_items(self):
        """Test false positive rate calculation with items."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add items
        for i in range(50):
            bf.add(f"item_{i}")
        
        fpr = bf.get_false_positive_rate()
        assert 0.0 <= fpr <= 1.0
        
        # Formula: (1 - e^(-k*n/m))^k
        k = bf.hash_count
        n = bf.element_count
        m = bf.size
        expected_fpr = (1 - math.exp(-k * n / m)) ** k
        
        assert abs(fpr - expected_fpr) < 1e-10
    
    def test_get_memory_usage(self):
        """Test memory usage calculation."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        memory = bf.get_memory_usage()
        assert memory > 0
        assert memory <= len(bf.bit_array) // 8 + 1
    
    def test_get_load_factor(self):
        """Test load factor calculation."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Empty filter
        assert bf.get_load_factor() == 0.0
        
        # Add items
        for i in range(10):
            bf.add(f"item_{i}")
        
        load_factor = bf.get_load_factor()
        assert 0.0 < load_factor <= 1.0
        
        # Calculate manually
        set_bits = sum(1 for bit in bf.bit_array if bit)
        expected_load_factor = set_bits / bf.size
        assert abs(load_factor - expected_load_factor) < 1e-10
    
    def test_get_utilization_stats(self):
        """Test utilization statistics."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Empty filter
        stats = bf.get_utilization_stats()
        assert stats['total_bits'] == bf.size
        assert stats['set_bits'] == 0
        assert stats['unset_bits'] == bf.size
        assert stats['load_factor'] == 0.0
        assert stats['element_count'] == 0
        assert stats['hash_count'] == bf.hash_count
        
        # Add items
        for i in range(10):
            bf.add(f"item_{i}")
        
        stats = bf.get_utilization_stats()
        assert stats['element_count'] == 10
        assert stats['set_bits'] > 0
        assert stats['unset_bits'] >= 0
        assert stats['load_factor'] > 0.0
        assert stats['bits_per_element'] == bf.size / 10
    
    def test_clear(self):
        """Test clearing the filter."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add items
        bf.add("apple")
        bf.add("banana")
        assert len(bf) == 2
        
        # Clear
        bf.clear()
        assert len(bf) == 0
        assert not bf.contains("apple")
        assert not bf.contains("banana")
        assert bf.get_load_factor() == 0.0
    
    def test_len(self):
        """Test length operator."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        assert len(bf) == 0
        
        bf.add("apple")
        assert len(bf) == 1
        
        bf.add("banana")
        assert len(bf) == 2
    
    def test_contains_operator(self):
        """Test 'in' operator."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("apple")
        
        assert "apple" in bf
        assert "banana" not in bf
    
    def test_repr(self):
        """Test string representation."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        repr_str = repr(bf)
        assert "BloomFilter" in repr_str
        assert "expected_elements=1000" in repr_str
        assert "size=" in repr_str
        assert "hash_count=" in repr_str
        assert "elements=0" in repr_str
    
    def test_str(self):
        """Test human-readable string representation."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("apple")
        bf.add("banana")
        
        str_repr = str(bf)
        assert "BloomFilter" in str_repr
        assert "2 elements" in str_repr
        assert "load factor:" in str_repr
        assert "FPR:" in str_repr
    
    def test_large_dataset(self):
        """Test with large dataset."""
        bf = BloomFilter(expected_elements=10000, false_positive_rate=0.1)  # Higher FPR to ensure false positives
        
        # Add many items
        for i in range(5000):
            bf.add(f"item_{i}")
        
        assert len(bf) == 5000
        
        # Check that all added items are found
        for i in range(5000):
            assert bf.contains(f"item_{i}")
        
        # Check some non-existent items
        false_positives = 0
        for i in range(1000):
            if bf.contains(f"non_existent_{i}"):
                false_positives += 1
        
        # With 10% FPR, we expect some false positives
        assert false_positives > 0
    
    def test_different_data_types(self):
        """Test with different data types."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Test various data types
        test_items = [
            "string",
            42,
            3.14,
            True,
            False,
            None,
            [1, 2, 3],
            {"key": "value"},
            (1, 2, 3),
            set([1, 2, 3])
        ]
        
        for item in test_items:
            bf.add(item)
            assert bf.contains(item)
    
    def test_hash_collision_handling(self):
        """Test handling of hash collisions."""
        bf = BloomFilter(expected_elements=10, false_positive_rate=0.5)  # Small size to force collisions
        
        # Add items that might cause collisions
        for i in range(20):
            bf.add(f"item_{i}")
        
        # All added items should still be found
        for i in range(20):
            assert bf.contains(f"item_{i}")
    
    def test_memory_efficiency(self):
        """Test memory efficiency compared to set."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        # Add items to Bloom filter
        items = [f"item_{i}" for i in range(500)]
        for item in items:
            bf.add(item)
        
        bloom_memory = bf.get_memory_usage()
        
        # Compare with Python set
        test_set = set(items)
        set_memory = sys.getsizeof(test_set) + sum(sys.getsizeof(item) for item in test_set)
        
        # Bloom filter should use less memory
        assert bloom_memory < set_memory
    
    def test_performance_characteristics(self):
        """Test basic performance characteristics."""
        bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        # Test add performance
        import time
        start_time = time.time()
        for i in range(1000):
            bf.add(f"item_{i}")
        add_time = time.time() - start_time
        
        # Test contains performance
        start_time = time.time()
        for i in range(1000):
            bf.contains(f"item_{i}")
        contains_time = time.time() - start_time
        
        # Operations should be reasonably fast
        assert add_time < 1.0  # Less than 1 second for 1000 adds
        assert contains_time < 1.0  # Less than 1 second for 1000 contains


class TestBloomFilterEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_single_element(self):
        """Test with single element."""
        bf = BloomFilter(expected_elements=1, false_positive_rate=0.01)
        
        bf.add("single_item")
        assert bf.contains("single_item")
        assert not bf.contains("other_item")
    
    def test_very_small_false_positive_rate(self):
        """Test with very small false positive rate."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.001)
        
        for i in range(50):
            bf.add(f"item_{i}")
        
        # Should have very few false positives
        false_positives = sum(1 for i in range(100) if bf.contains(f"non_existent_{i}"))
        assert false_positives < 10  # Less than 10% false positives
    
    def test_very_large_expected_elements(self):
        """Test with very large expected elements."""
        bf = BloomFilter(expected_elements=1000000, false_positive_rate=0.01)
        
        # Should still work with reasonable memory usage
        assert bf.size > 0
        assert bf.hash_count > 0
        assert bf.get_memory_usage() < 2000000  # Less than 2MB (more realistic for large datasets)
    
    def test_unicode_strings(self):
        """Test with Unicode strings."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        unicode_items = [
            "café",
            "naïve",
            "résumé",
            "über",
            "🎉",
            "🚀",
            "你好",
            "こんにちは"
        ]
        
        for item in unicode_items:
            bf.add(item)
            assert bf.contains(item)
    
    def test_empty_strings(self):
        """Test with empty strings."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        bf.add("")
        assert bf.contains("")
        assert not bf.contains("non_empty")
    
    def test_very_long_strings(self):
        """Test with very long strings."""
        bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        long_string = "a" * 10000
        bf.add(long_string)
        assert bf.contains(long_string)
        assert not bf.contains("a" * 9999) 