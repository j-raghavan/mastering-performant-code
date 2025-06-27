"""
Counting Bloom Filter Implementation

This module provides a Bloom filter variant that supports deletion operations
by using counters instead of boolean flags.
"""

import math
import hashlib
from typing import Any, List, Optional, Tuple, Dict

class CountingBloomFilter:
    """
    A Bloom filter variant that supports deletion operations.
    
    This implementation uses counters instead of boolean flags,
    allowing elements to be removed from the filter.
    
    Attributes:
        expected_elements (int): Expected number of elements
        false_positive_rate (float): Desired false positive rate
        max_count (int): Maximum count per bit
        size (int): Size of the counter array
        hash_count (int): Number of hash functions
        counter_array (List[int]): Internal counter array
        element_count (int): Number of elements currently in the filter
        hash_seeds (List[int]): Seeds for hash functions
    """
    
    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01, 
                 max_count: int = 255):
        """
        Initialize a counting Bloom filter.
        
        Args:
            expected_elements: Expected number of elements
            false_positive_rate: Desired false positive rate
            max_count: Maximum count per bit (default 255 for uint8)
            
        Raises:
            ValueError: If any parameter is invalid
        """
        if expected_elements <= 0:
            raise ValueError("Expected elements must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("False positive rate must be between 0 and 1")
        if max_count <= 0:
            raise ValueError("Max count must be positive")
        
        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate
        self.max_count = max_count
        
        # Calculate optimal parameters
        self.size = self._calculate_optimal_size(expected_elements, false_positive_rate)
        self.hash_count = self._calculate_optimal_hash_count(expected_elements, self.size)
        
        # Initialize counter array
        self.counter_array = [0] * self.size
        self.element_count = 0
        
        # Pre-compute hash function seeds
        self.hash_seeds = self._generate_hash_seeds(self.hash_count)
    
    def _calculate_optimal_size(self, n: int, p: float) -> int:
        """
        Calculate optimal counter array size.
        
        Args:
            n: Expected number of elements
            p: Desired false positive rate
            
        Returns:
            Optimal size of the counter array
        """
        return int(-n * math.log(p) / (math.log(2) ** 2))
    
    def _calculate_optimal_hash_count(self, n: int, m: int) -> int:
        """
        Calculate optimal number of hash functions.
        
        Args:
            n: Expected number of elements
            m: Size of counter array
            
        Returns:
            Optimal number of hash functions
        """
        return max(1, int((m / n) * math.log(2)))
    
    def _generate_hash_seeds(self, count: int) -> List[int]:
        """
        Generate seeds for hash functions.
        
        Args:
            count: Number of hash functions needed
            
        Returns:
            List of hash seeds
        """
        return [hash(f"counting_bloom_seed_{i}") for i in range(count)]
    
    def _hash_functions(self, item: Any) -> List[int]:
        """
        Apply multiple hash functions to an item.
        
        Args:
            item: Item to hash
            
        Returns:
            List of bit positions
        """
        item_str = str(item)
        positions = []
        
        for seed in self.hash_seeds:
            hash_obj = hashlib.md5()
            hash_obj.update(f"{seed}:{item_str}".encode())
            hash_value = int(hash_obj.hexdigest(), 16)
            positions.append(hash_value % self.size)
        
        return positions
    
    def add(self, item: Any) -> bool:
        """
        Add an item to the counting Bloom filter.
        
        Args:
            item: Item to add
            
        Returns:
            True if added successfully, False if counters would overflow
        """
        positions = self._hash_functions(item)
        
        # Check if adding would cause overflow
        for pos in positions:
            if self.counter_array[pos] >= self.max_count:
                return False
        
        # Check if item is already in the filter
        was_present = all(self.counter_array[pos] > 0 for pos in positions)
        
        # Increment counters
        for pos in positions:
            self.counter_array[pos] += 1
        
        # Only increment element count if this is a new item
        if not was_present:
            self.element_count += 1
        
        return True
    
    def remove(self, item: Any) -> bool:
        """
        Remove an item from the counting Bloom filter.
        
        Args:
            item: Item to remove
            
        Returns:
            True if item was probably in the set, False if definitely not
        """
        positions = self._hash_functions(item)
        
        # Check if item is in the filter
        if not all(self.counter_array[pos] > 0 for pos in positions):
            return False
        
        # Decrement counters
        for pos in positions:
            self.counter_array[pos] -= 1
        
        # Check if this completely removed the item (all counters for this item are now 0)
        # Note: We need to check after decrementing, not before
        is_completely_removed = all(self.counter_array[pos] == 0 for pos in positions)
        
        # Only decrement element count if this completely removes the item
        # However, due to hash collisions, we need to be more careful
        # We'll use a heuristic: if the item is no longer detectable, we assume it's removed
        if is_completely_removed:
            # Double-check that the item is actually not detectable anymore
            if not self.contains(item):
                self.element_count = max(0, self.element_count - 1)
        
        return True
    
    def contains(self, item: Any) -> bool:
        """
        Check if an item is in the counting Bloom filter.
        
        Args:
            item: Item to check
            
        Returns:
            True if item is probably in the set, False if definitely not
        """
        positions = self._hash_functions(item)
        return all(self.counter_array[pos] > 0 for pos in positions)
    
    def get_false_positive_rate(self) -> float:
        """
        Calculate current false positive rate.
        
        Returns:
            Current false positive rate
        """
        if self.element_count == 0:
            return 0.0
        
        k = self.hash_count
        n = self.element_count
        m = self.size
        
        return (1 - math.exp(-k * n / m)) ** k
    
    def get_memory_usage(self) -> int:
        """
        Get memory usage in bytes.
        
        Returns:
            Memory usage in bytes (each counter is 1 byte)
        """
        return len(self.counter_array)  # Each counter is 1 byte
    
    def get_load_factor(self) -> float:
        """
        Get current load factor.
        
        Returns:
            Load factor as a float between 0 and 1
        """
        non_zero_counters = sum(1 for counter in self.counter_array if counter > 0)
        return non_zero_counters / self.size
    
    def get_counter_distribution(self) -> Dict[int, int]:
        """
        Get distribution of counter values.
        
        Returns:
            Dictionary mapping counter values to their frequencies
        """
        distribution = {}
        for counter in self.counter_array:
            distribution[counter] = distribution.get(counter, 0) + 1
        return distribution
    
    def get_utilization_stats(self) -> dict:
        """
        Get detailed utilization statistics.
        
        Returns:
            Dictionary with utilization statistics
        """
        non_zero_counters = sum(1 for counter in self.counter_array if counter > 0)
        total_count = sum(self.counter_array)
        
        return {
            'total_counters': self.size,
            'non_zero_counters': non_zero_counters,
            'zero_counters': self.size - non_zero_counters,
            'load_factor': non_zero_counters / self.size,
            'element_count': self.element_count,
            'total_count': total_count,
            'average_count': total_count / max(1, self.size),
            'max_count': max(self.counter_array),
            'hash_count': self.hash_count
        }
    
    def get_overflow_risk(self) -> float:
        """
        Calculate the risk of counter overflow.
        
        Returns:
            Risk as a float between 0 and 1
        """
        if self.max_count == 0:
            return 0.0
        
        max_counter = max(self.counter_array)
        return max_counter / self.max_count
    
    def clear(self) -> None:
        """Clear all elements from the counting Bloom filter."""
        self.counter_array = [0] * self.size
        self.element_count = 0
    
    def __len__(self) -> int:
        """Return the number of elements in the counting Bloom filter."""
        return self.element_count
    
    def __contains__(self, item: Any) -> bool:
        """Check if an item is in the counting Bloom filter using 'in' operator."""
        return self.contains(item)
    
    def __repr__(self) -> str:
        """String representation of the counting Bloom filter."""
        return (f"CountingBloomFilter(expected_elements={self.expected_elements}, "
                f"size={self.size}, hash_count={self.hash_count}, "
                f"elements={self.element_count})")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        stats = self.get_utilization_stats()
        return (f"CountingBloomFilter with {self.element_count} elements "
                f"(load factor: {stats['load_factor']:.2%}, "
                f"FPR: {self.get_false_positive_rate():.4f}, "
                f"overflow risk: {self.get_overflow_risk():.2%})") 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running counting_bloom_filter demonstration...")
    print("=" * 50)

    # Create instance of CountingBloomFilter
    try:
        instance = CountingBloomFilter()
        print(f"✓ Created CountingBloomFilter instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating CountingBloomFilter instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
