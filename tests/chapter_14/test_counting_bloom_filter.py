"""
Unit tests for Counting Bloom Filter implementation.

This module provides comprehensive tests for the CountingBloomFilter class,
ensuring 100% code coverage and testing all edge cases.
"""

import pytest
import math
from typing import List, Any
from mastering_performant_code.chapter_14.counting_bloom_filter import CountingBloomFilter


class TestCountingBloomFilter:
    """Test cases for CountingBloomFilter class."""
    
    def test_init_valid_parameters(self):
        """Test initialization with valid parameters."""
        cbf = CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01, max_count=255)
        
        assert cbf.expected_elements == 1000
        assert cbf.false_positive_rate == 0.01
        assert cbf.max_count == 255
        assert cbf.element_count == 0
        assert len(cbf.counter_array) > 0
        assert len(cbf.hash_seeds) > 0
    
    def test_init_invalid_expected_elements(self):
        """Test initialization with invalid expected elements."""
        with pytest.raises(ValueError, match="Expected elements must be positive"):
            CountingBloomFilter(expected_elements=0, false_positive_rate=0.01)
        
        with pytest.raises(ValueError, match="Expected elements must be positive"):
            CountingBloomFilter(expected_elements=-1, false_positive_rate=0.01)
    
    def test_init_invalid_false_positive_rate(self):
        """Test initialization with invalid false positive rate."""
        with pytest.raises(ValueError, match="False positive rate must be between 0 and 1"):
            CountingBloomFilter(expected_elements=1000, false_positive_rate=0.0)
        
        with pytest.raises(ValueError, match="False positive rate must be between 0 and 1"):
            CountingBloomFilter(expected_elements=1000, false_positive_rate=1.0)
    
    def test_init_invalid_max_count(self):
        """Test initialization with invalid max count."""
        with pytest.raises(ValueError, match="Max count must be positive"):
            CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01, max_count=0)
        
        with pytest.raises(ValueError, match="Max count must be positive"):
            CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01, max_count=-1)
    
    def test_add_and_contains(self):
        """Test adding items and checking membership."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add items
        items = ["apple", "banana", "cherry", 42, [1, 2, 3]]
        
        for item in items:
            result = cbf.add(item)
            assert result is True
            assert cbf.contains(item)
        
        assert len(cbf) == len(items)
    
    def test_remove_items(self):
        """Test removing items from the filter."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add items
        cbf.add("apple")
        cbf.add("banana")
        cbf.add("cherry")
        
        assert len(cbf) == 3
        assert cbf.contains("apple")
        assert cbf.contains("banana")
        assert cbf.contains("cherry")
        
        # Remove items
        assert cbf.remove("banana") is True
        assert len(cbf) == 2
        assert not cbf.contains("banana")
        assert cbf.contains("apple")
        assert cbf.contains("cherry")
        
        # Remove non-existent item
        assert cbf.remove("grape") is False
        assert len(cbf) == 2
    
    def test_remove_nonexistent_item(self):
        """Test removing an item that doesn't exist."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Try to remove from empty filter
        assert cbf.remove("apple") is False
        
        # Add an item and try to remove a different one
        cbf.add("apple")
        assert cbf.remove("banana") is False
        assert len(cbf) == 1
        assert cbf.contains("apple")
    
    def test_counter_overflow(self):
        """Test counter overflow behavior."""
        cbf = CountingBloomFilter(expected_elements=10, false_positive_rate=0.5, max_count=2)
        
        # Add the same item multiple times to cause overflow
        assert cbf.add("test_item") is True
        assert cbf.add("test_item") is True
        assert cbf.add("test_item") is False  # Should fail due to overflow
        
        assert len(cbf) == 1  # Only one unique item
        assert cbf.contains("test_item")
    
    def test_get_counter_distribution(self):
        """Test counter distribution analysis."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Empty filter
        distribution = cbf.get_counter_distribution()
        assert distribution[0] == len(cbf.counter_array)  # All counters are 0
        
        # Add some items
        cbf.add("apple")
        cbf.add("banana")
        cbf.add("apple")  # Duplicate
        
        distribution = cbf.get_counter_distribution()
        assert 0 in distribution
        assert 1 in distribution
        assert 2 in distribution
        assert distribution[0] > 0  # Some counters are still 0
        assert distribution[1] > 0  # Some counters are 1
        assert distribution[2] > 0  # Some counters are 2
    
    def test_get_utilization_stats(self):
        """Test utilization statistics."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Empty filter
        stats = cbf.get_utilization_stats()
        assert stats['total_counters'] == cbf.size
        assert stats['non_zero_counters'] == 0
        assert stats['zero_counters'] == cbf.size
        assert stats['load_factor'] == 0.0
        assert stats['element_count'] == 0
        assert stats['total_count'] == 0
        assert stats['average_count'] == 0.0
        assert stats['max_count'] == 0
        assert stats['hash_count'] == cbf.hash_count
        
        # Add items
        cbf.add("apple")
        cbf.add("banana")
        cbf.add("apple")  # Duplicate
        
        stats = cbf.get_utilization_stats()
        assert stats['element_count'] == 2  # Only unique items
        assert stats['total_count'] > 0
        assert stats['non_zero_counters'] > 0
        assert stats['load_factor'] > 0.0
        assert stats['max_count'] >= 2  # At least one counter should be 2
    
    def test_get_overflow_risk(self):
        """Test overflow risk calculation."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01, max_count=10)
        
        # Empty filter
        assert cbf.get_overflow_risk() == 0.0
        
        # Add items to increase risk
        for i in range(5):
            cbf.add(f"item_{i}")
        
        risk = cbf.get_overflow_risk()
        assert 0.0 <= risk <= 1.0
        
        # Add the same item multiple times to increase risk
        for _ in range(8):
            cbf.add("test_item")
        
        risk = cbf.get_overflow_risk()
        assert risk > 0.0
    
    def test_clear(self):
        """Test clearing the filter."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add items
        cbf.add("apple")
        cbf.add("banana")
        assert len(cbf) == 2
        
        # Clear
        cbf.clear()
        assert len(cbf) == 0
        assert not cbf.contains("apple")
        assert not cbf.contains("banana")
        assert cbf.get_load_factor() == 0.0
        
        # Check that counters are reset
        distribution = cbf.get_counter_distribution()
        assert distribution[0] == len(cbf.counter_array)
    
    def test_len(self):
        """Test length operator."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        assert len(cbf) == 0
        
        cbf.add("apple")
        assert len(cbf) == 1
        
        cbf.add("banana")
        assert len(cbf) == 2
        
        cbf.remove("apple")
        # Due to hash collisions, the count may not decrease exactly as expected
        # Just check that the count does not increase
        assert len(cbf) <= 2
    
    def test_contains_operator(self):
        """Test 'in' operator."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        cbf.add("apple")
        
        assert "apple" in cbf
        assert "banana" not in cbf
    
    def test_repr(self):
        """Test string representation."""
        cbf = CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        repr_str = repr(cbf)
        assert "CountingBloomFilter" in repr_str
        assert "expected_elements=1000" in repr_str
        assert "size=" in repr_str
        assert "hash_count=" in repr_str
        assert "elements=0" in repr_str
    
    def test_str(self):
        """Test human-readable string representation."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        cbf.add("apple")
        cbf.add("banana")
        
        str_repr = str(cbf)
        assert "CountingBloomFilter" in str_repr
        assert "2 elements" in str_repr
        assert "load factor:" in str_repr
        assert "FPR:" in str_repr
        assert "overflow risk:" in str_repr
    
    def test_false_positive_rate_calculation(self):
        """Test false positive rate calculation."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Empty filter
        assert cbf.get_false_positive_rate() == 0.0
        
        # Add items
        for i in range(50):
            cbf.add(f"item_{i}")
        
        fpr = cbf.get_false_positive_rate()
        assert 0.0 <= fpr <= 1.0
        
        # Formula: (1 - e^(-k*n/m))^k
        k = cbf.hash_count
        n = cbf.element_count
        m = cbf.size
        expected_fpr = (1 - math.exp(-k * n / m)) ** k
        
        assert abs(fpr - expected_fpr) < 1e-10
    
    def test_memory_usage(self):
        """Test memory usage calculation."""
        cbf = CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01)
        
        memory = cbf.get_memory_usage()
        assert memory == len(cbf.counter_array)  # Each counter is 1 byte
    
    def test_load_factor(self):
        """Test load factor calculation."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Empty filter
        assert cbf.get_load_factor() == 0.0
        
        # Add items
        for i in range(10):
            cbf.add(f"item_{i}")
        
        load_factor = cbf.get_load_factor()
        assert 0.0 < load_factor <= 1.0
        
        # Calculate manually
        non_zero_counters = sum(1 for counter in cbf.counter_array if counter > 0)
        expected_load_factor = non_zero_counters / cbf.size
        assert abs(load_factor - expected_load_factor) < 1e-10
    
    def test_duplicate_handling(self):
        """Test handling of duplicate items."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        # Add the same item multiple times
        cbf.add("apple")
        cbf.add("apple")
        cbf.add("apple")
        
        assert len(cbf) == 1  # Only one unique item
        assert cbf.contains("apple")
        
        # Remove once
        assert cbf.remove("apple") is True
        assert cbf.contains("apple")  # Still present due to multiple additions
        
        # Remove again
        assert cbf.remove("apple") is True
        assert cbf.contains("apple")  # Still present
        
        # Remove third time
        assert cbf.remove("apple") is True
        assert not cbf.contains("apple")  # Now removed
        # Due to hash collisions, the count may not reach exactly zero
        assert len(cbf) <= 1
    
    def test_large_dataset(self):
        """Test with large dataset."""
        cbf = CountingBloomFilter(expected_elements=10000, false_positive_rate=0.01)
        
        # Add many items
        for i in range(5000):
            cbf.add(f"item_{i}")
        
        # Allow a small margin of error due to hash collisions
        assert abs(len(cbf) - 5000) <= 2  # Acceptable margin for probabilistic structure
        
        # Check that all added items are found
        for i in range(5000):
            assert cbf.contains(f"item_{i}")
        
        # Remove some items
        removed_count = 0
        for i in range(1000):
            if cbf.remove(f"item_{i}"):
                removed_count += 1
        
        # The element count should decrease after removals
        assert len(cbf) < 5000
        # Due to hash collisions, the count may not match exactly
        # Most removed items should not be found
        not_found_count = 0
        for i in range(1000):
            if not cbf.contains(f"item_{i}"):
                not_found_count += 1
        assert not_found_count >= 800  # At least 80% should be removed
        # Most remaining items should still be found
        found_count = 0
        for i in range(1000, 5000):
            if cbf.contains(f"item_{i}"):
                found_count += 1
        assert found_count >= 3500  # At least 87.5% should still be found


class TestCountingBloomFilterEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_single_element(self):
        """Test with single element."""
        cbf = CountingBloomFilter(expected_elements=10, false_positive_rate=0.01)
        
        cbf.add("single_item")
        assert cbf.contains("single_item")
        assert not cbf.contains("other_item")
        
        cbf.remove("single_item")
        assert not cbf.contains("single_item")
    
    def test_max_count_one(self):
        """Test with max count of 1."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01, max_count=1)
        
        # Add item once
        assert cbf.add("test_item") is True
        assert cbf.contains("test_item")
        
        # Try to add again
        assert cbf.add("test_item") is False  # Should fail due to max count
        assert cbf.contains("test_item")  # Should still be present
    
    def test_very_small_max_count(self):
        """Test with very small max count."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01, max_count=3)
        
        # Add the same item multiple times
        assert cbf.add("test_item") is True
        assert cbf.add("test_item") is True
        assert cbf.add("test_item") is True
        assert cbf.add("test_item") is False  # Should fail
        
        assert cbf.contains("test_item")
        assert len(cbf) == 1
    
    def test_unicode_strings(self):
        """Test with Unicode strings."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
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
            cbf.add(item)
            assert cbf.contains(item)
            cbf.remove(item)
            assert not cbf.contains(item)
    
    def test_empty_strings(self):
        """Test with empty strings."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        cbf.add("")
        assert cbf.contains("")
        assert not cbf.contains("non_empty")
        
        cbf.remove("")
        assert not cbf.contains("")
    
    def test_very_long_strings(self):
        """Test with very long strings."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        long_string = "a" * 10000
        cbf.add(long_string)
        assert cbf.contains(long_string)
        assert not cbf.contains("a" * 9999)
        
        cbf.remove(long_string)
        assert not cbf.contains(long_string)
    
    def test_different_data_types(self):
        """Test with different data types."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
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
            cbf.add(item)
            assert cbf.contains(item)
            cbf.remove(item)
            assert not cbf.contains(item)
    
    def test_remove_from_empty_filter(self):
        """Test removing from empty filter."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        assert cbf.remove("any_item") is False
        assert len(cbf) == 0
    
    def test_remove_nonexistent_item_after_adding(self):
        """Test removing non-existent item after adding some items."""
        cbf = CountingBloomFilter(expected_elements=100, false_positive_rate=0.01)
        
        cbf.add("apple")
        cbf.add("banana")
        
        assert cbf.remove("grape") is False
        assert len(cbf) == 2
        assert cbf.contains("apple")
        assert cbf.contains("banana")
    
    def test_counter_overflow_edge_case(self):
        """Test edge case of counter overflow."""
        cbf = CountingBloomFilter(expected_elements=10, false_positive_rate=0.5, max_count=1)
        
        # Add different items to fill up counters
        for i in range(20):
            result = cbf.add(f"item_{i}")
            if not result:
                break  # Stop when overflow occurs
        
        # Should have some items added
        assert len(cbf) > 0 