"""
Scalable Bloom Filter Implementation

This module provides a Bloom filter that can grow dynamically to accommodate
more elements while maintaining good space efficiency.
"""

import math
import hashlib
from typing import Any, List, Optional, Tuple, Dict
from .bloom_filter import BloomFilter

class ScalableBloomFilter:
    """
    A Bloom filter that can grow dynamically to accommodate more elements.
    
    This implementation maintains multiple Bloom filters with increasing
    false positive rates, providing better space efficiency for growing datasets.
    
    Attributes:
        initial_capacity (int): Initial expected number of elements
        initial_false_positive_rate (float): Initial false positive rate
        growth_factor (float): Factor by which capacity grows
        scale_factor (float): Factor by which false positive rate decreases
        filters (List[BloomFilter]): List of Bloom filters
        current_capacity (int): Current capacity for new filters
        current_false_positive_rate (float): Current false positive rate for new filters
    """
    
    def __init__(self, initial_capacity: int = 1000, false_positive_rate: float = 0.01,
                 growth_factor: float = 2.0, scale_factor: float = 0.8):
        """
        Initialize a scalable Bloom filter.
        
        Args:
            initial_capacity: Initial expected number of elements
            false_positive_rate: Initial false positive rate
            growth_factor: Factor by which capacity grows
            scale_factor: Factor by which false positive rate decreases
            
        Raises:
            ValueError: If any parameter is invalid
        """
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("False positive rate must be between 0 and 1")
        if growth_factor <= 1:
            raise ValueError("Growth factor must be greater than 1")
        if not 0 < scale_factor < 1:
            raise ValueError("Scale factor must be between 0 and 1")
        
        self.initial_capacity = initial_capacity
        self.initial_false_positive_rate = false_positive_rate
        self.growth_factor = growth_factor
        self.scale_factor = scale_factor
        
        # Initialize filter list
        self.filters = []
        self.current_capacity = initial_capacity
        self.current_false_positive_rate = false_positive_rate
        
        # Create first filter
        self._add_filter()
    
    def _add_filter(self) -> None:
        """Add a new Bloom filter to the scalable filter."""
        filter_bf = BloomFilter(
            expected_elements=self.current_capacity,
            false_positive_rate=self.current_false_positive_rate
        )
        self.filters.append(filter_bf)
    
    def _should_add_filter(self) -> bool:
        """
        Check if we should add a new filter.
        
        Returns:
            True if current filter is 90% full
        """
        if not self.filters:
            return True
        
        # Add new filter when current one is 90% full
        current_filter = self.filters[-1]
        return len(current_filter) >= current_filter.expected_elements * 0.9
    
    def add(self, item: Any) -> None:
        """
        Add an item to the scalable Bloom filter.
        
        Args:
            item: Item to add
        """
        # Check if we need to add a new filter
        if self._should_add_filter():
            self.current_capacity = int(self.current_capacity * self.growth_factor)
            self.current_false_positive_rate *= self.scale_factor
            self._add_filter()
        
        # Add to the last (most recent) filter
        self.filters[-1].add(item)
    
    def contains(self, item: Any) -> bool:
        """
        Check if an item is in the scalable Bloom filter.
        
        Args:
            item: Item to check
            
        Returns:
            True if item is probably in any of the filters
        """
        return any(bf.contains(item) for bf in self.filters)
    
    def get_false_positive_rate(self) -> float:
        """
        Calculate overall false positive rate.
        
        Formula: 1 - (1 - p1) * (1 - p2) * ... * (1 - pn)
        where pi is the false positive rate of filter i
        
        Returns:
            Overall false positive rate
        """
        if not self.filters:
            return 0.0
        
        # Calculate probability of false positive across all filters
        prob_no_false_positive = 1.0
        for bf in self.filters:
            prob_no_false_positive *= (1 - bf.get_false_positive_rate())
        
        return 1 - prob_no_false_positive
    
    def get_memory_usage(self) -> int:
        """
        Get total memory usage in bytes.
        
        Returns:
            Total memory usage across all filters
        """
        return sum(bf.get_memory_usage() for bf in self.filters)
    
    def get_total_elements(self) -> int:
        """
        Get total number of elements across all filters.
        
        Returns:
            Total number of elements
        """
        return sum(len(bf) for bf in self.filters)
    
    def get_filter_stats(self) -> List[Dict[str, Any]]:
        """
        Get statistics for each filter.
        
        Returns:
            List of dictionaries with filter statistics
        """
        stats = []
        for i, bf in enumerate(self.filters):
            stats.append({
                'filter_index': i,
                'expected_elements': bf.expected_elements,
                'actual_elements': len(bf),
                'false_positive_rate': bf.get_false_positive_rate(),
                'memory_usage': bf.get_memory_usage(),
                'load_factor': bf.get_load_factor(),
                'size': bf.size,
                'hash_count': bf.hash_count
            })
        return stats
    
    def get_utilization_stats(self) -> dict:
        """
        Get overall utilization statistics.
        
        Returns:
            Dictionary with overall statistics
        """
        total_elements = self.get_total_elements()
        total_memory = self.get_memory_usage()
        total_fpr = self.get_false_positive_rate()
        
        return {
            'total_filters': len(self.filters),
            'total_elements': total_elements,
            'total_memory': total_memory,
            'overall_false_positive_rate': total_fpr,
            'average_elements_per_filter': total_elements / max(1, len(self.filters)),
            'average_memory_per_filter': total_memory / max(1, len(self.filters)),
            'growth_factor': self.growth_factor,
            'scale_factor': self.scale_factor,
            'current_capacity': self.current_capacity,
            'current_false_positive_rate': self.current_false_positive_rate
        }
    
    def get_efficiency_metrics(self) -> dict:
        """
        Get efficiency metrics for the scalable filter.
        
        Returns:
            Dictionary with efficiency metrics
        """
        total_elements = self.get_total_elements()
        total_memory = self.get_memory_usage()
        
        if total_elements == 0:
            return {
                'memory_per_element': 0,
                'filters_per_element': 0,
                'efficiency_score': 0
            }
        
        # Calculate efficiency metrics
        memory_per_element = total_memory / total_elements
        filters_per_element = len(self.filters) / total_elements
        
        # Efficiency score (lower is better)
        efficiency_score = memory_per_element * filters_per_element
        
        return {
            'memory_per_element': memory_per_element,
            'filters_per_element': filters_per_element,
            'efficiency_score': efficiency_score
        }
    
    def clear(self) -> None:
        """Clear all elements from the scalable Bloom filter."""
        self.filters = []
        self.current_capacity = self.initial_capacity
        self.current_false_positive_rate = self.initial_false_positive_rate
        self._add_filter()
    
    def __len__(self) -> int:
        """Return the total number of elements in the scalable Bloom filter."""
        return self.get_total_elements()
    
    def __contains__(self, item: Any) -> bool:
        """Check if an item is in the scalable Bloom filter using 'in' operator."""
        return self.contains(item)
    
    def __repr__(self) -> str:
        """String representation of the scalable Bloom filter."""
        return (f"ScalableBloomFilter(filters={len(self.filters)}, "
                f"total_elements={self.get_total_elements()}, "
                f"memory={self.get_memory_usage()} bytes)")
    
    def __str__(self) -> str:
        """Human-readable string representation."""
        stats = self.get_utilization_stats()
        return (f"ScalableBloomFilter with {stats['total_elements']} elements "
                f"across {stats['total_filters']} filters "
                f"(FPR: {stats['overall_false_positive_rate']:.4f}, "
                f"memory: {stats['total_memory']} bytes)") 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running scalable_bloom_filter demonstration...")
    print("=" * 50)

    # Create instance of ScalableBloomFilter
    try:
        instance = ScalableBloomFilter()
        print(f"✓ Created ScalableBloomFilter instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating ScalableBloomFilter instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
