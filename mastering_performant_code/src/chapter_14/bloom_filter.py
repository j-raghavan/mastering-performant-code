"""
Basic Bloom Filter Implementation

This module provides a space-efficient probabilistic data structure for membership testing.
The Bloom filter provides fast membership testing with a small probability of false positives.
"""

import math
import hashlib
from typing import Any, List, Optional, Tuple
import timeit

class BloomFilter:
    """
    A space-efficient probabilistic data structure for membership testing.
    
    This implementation provides:
    - Configurable false positive rate
    - Optimal hash function count
    - Memory-efficient bit array storage
    - Comprehensive performance analysis
    
    Attributes:
        expected_elements (int): Expected number of elements to be inserted
        false_positive_rate (float): Desired false positive rate
        size (int): Size of the bit array
        hash_count (int): Number of hash functions
        bit_array (List[bool]): Internal bit array
        element_count (int): Number of elements currently in the filter
        hash_seeds (List[int]): Seeds for hash functions
    """
    
    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01):
        """
        Initialize a Bloom filter with optimal parameters.
        
        Args:
            expected_elements: Expected number of elements to be inserted
            false_positive_rate: Desired false positive rate (0.0 to 1.0)
            
        Raises:
            ValueError: If expected_elements <= 0 or false_positive_rate not in (0, 1)
        """
        if expected_elements <= 0:
            raise ValueError("Expected elements must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("False positive rate must be between 0 and 1")
        
        self.expected_elements = expected_elements
        self.false_positive_rate = false_positive_rate
        
        # Calculate optimal parameters
        self.size = self._calculate_optimal_size(expected_elements, false_positive_rate)
        self.hash_count = self._calculate_optimal_hash_count(expected_elements, self.size)
        
        # Initialize bit array
        self.bit_array = [False] * self.size
        self.element_count = 0
        
        # Pre-compute hash function seeds
        self.hash_seeds = self._generate_hash_seeds(self.hash_count)
    
    def _calculate_optimal_size(self, n: int, p: float) -> int:
        """
        Calculate optimal bit array size for given parameters.
        
        Formula: m = -n * ln(p) / (ln(2)^2)
        
        Args:
            n: Expected number of elements
            p: Desired false positive rate
            
        Returns:
            Optimal size of the bit array
        """
        return int(-n * math.log(p) / (math.log(2) ** 2))
    
    def _calculate_optimal_hash_count(self, n: int, m: int) -> int:
        """
        Calculate optimal number of hash functions.
        
        Formula: k = (m/n) * ln(2)
        
        Args:
            n: Expected number of elements
            m: Size of bit array
            
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
        return [hash(f"bloom_seed_{i}") for i in range(count)]
    
    def _hash_functions(self, item: Any) -> List[int]:
        """
        Apply multiple hash functions to an item.
        
        Returns list of bit positions to set/check.
        
        Args:
            item: Item to hash
            
        Returns:
            List of bit positions
        """
        # Convert item to string for hashing
        item_str = str(item)
        
        positions = []
        for seed in self.hash_seeds:
            # Create hash object with seed
            hash_obj = hashlib.md5()
            hash_obj.update(f"{seed}:{item_str}".encode())
            hash_value = int(hash_obj.hexdigest(), 16)
            positions.append(hash_value % self.size)
        
        return positions
    
    def add(self, item: Any) -> None:
        """
        Add an item to the Bloom filter.
        
        Args:
            item: Item to add (will be converted to string for hashing)
        """
        positions = self._hash_functions(item)
        for pos in positions:
            self.bit_array[pos] = True
        self.element_count += 1
    
    def contains(self, item: Any) -> bool:
        """
        Check if an item is in the Bloom filter.
        
        Args:
            item: Item to check
            
        Returns:
            True if item is probably in the set, False if definitely not
        """
        positions = self._hash_functions(item)
        return all(self.bit_array[pos] for pos in positions)
    
    def get_false_positive_rate(self) -> float:
        """
        Calculate current false positive rate.
        
        Formula: (1 - e^(-k*n/m))^k
        
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
            Approximate memory usage in bytes
        """
        # Each boolean in Python is typically 24 bytes, but we'll use a more realistic estimate
        # for a bit array implementation
        return len(self.bit_array) // 8  # 8 bits per byte
    
    def get_load_factor(self) -> float:
        """
        Get current load factor (fraction of bits set).
        
        Returns:
            Load factor as a float between 0 and 1
        """
        set_bits = sum(1 for bit in self.bit_array if bit)
        return set_bits / self.size
    
    def get_utilization_stats(self) -> dict:
        """
        Get detailed utilization statistics.
        
        Returns:
            Dictionary with utilization statistics
        """
        set_bits = sum(1 for bit in self.bit_array if bit)
        return {
            'total_bits': self.size,
            'set_bits': set_bits,
            'unset_bits': self.size - set_bits,
            'load_factor': set_bits / self.size,
            'element_count': self.element_count,
            'bits_per_element': self.size / max(1, self.element_count),
            'hash_count': self.hash_count
        }
    
    def clear(self) -> None:
        """Clear all elements from the Bloom filter."""
        self.bit_array = [False] * self.size
        self.element_count = 0
    
    def __len__(self) -> int:
        """Return the number of elements in the Bloom filter."""
        return self.element_count
    
    def __contains__(self, item: Any) -> bool:
        """Check if an item is in the Bloom filter using 'in' operator."""
        return self.contains(item)
    
    def __repr__(self) -> str:
        """String representation of the Bloom filter."""
        return (f"BloomFilter(expected_elements={self.expected_elements}, "
                f"size={self.size}, hash_count={self.hash_count}, "
                f"elements={self.element_count})")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        stats = self.get_utilization_stats()
        return (f"BloomFilter with {self.element_count} elements "
                f"(load factor: {stats['load_factor']:.2%}, "
                f"FPR: {self.get_false_positive_rate():.4f})") 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running bloom_filter demonstration...")
    print("=" * 50)

    # Create instance of BloomFilter
    try:
        instance = BloomFilter()
        print(f"✓ Created BloomFilter instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating BloomFilter instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
