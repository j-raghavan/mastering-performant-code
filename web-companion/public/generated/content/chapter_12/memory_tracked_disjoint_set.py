"""
Memory-tracked Union-Find (Disjoint-Set) implementation.

This module provides a Union-Find implementation that tracks memory usage
for performance profiling and optimization analysis.
"""

from typing import Dict, List, Optional, Tuple
import sys
from dataclasses import dataclass

from src.chapter_12.optimized_disjoint_set import OptimizedDisjointSet


@dataclass
class MemoryInfo:
    """Information about memory usage of the Union-Find data structure."""
    object_size: int
    total_size: int
    overhead: int
    elements: int
    sets: int


class MemoryTrackedDisjointSet(OptimizedDisjointSet):
    """
    A Union-Find implementation that tracks memory usage.
    
    This extends the optimized implementation with memory analysis
    capabilities for performance profiling and optimization.
    
    Additional Features:
    - Memory usage tracking
    - Memory efficiency reporting
    - Performance analysis tools
    """
    
    def __init__(self) -> None:
        super().__init__()
        self._memory_tracking = True
    
    def get_memory_info(self) -> MemoryInfo:
        """
        Get detailed memory usage information.
        
        Returns:
            MemoryInfo object containing memory usage statistics
            
        Time Complexity: O(n)
        """
        object_size = sys.getsizeof(self)
        
        # Calculate memory usage for parents dictionary
        parents_size = sys.getsizeof(self.parents)
        # Estimate item size more conservatively
        parents_items_size = len(self.parents) * 16  # Estimate 8 bytes per key + 8 bytes per value
        
        # Calculate memory usage for ranks dictionary
        ranks_size = sys.getsizeof(self.ranks)
        ranks_items_size = len(self.ranks) * 16  # Estimate 8 bytes per key + 8 bytes per value
        
        # Calculate memory usage for sizes dictionary
        sizes_size = sys.getsizeof(self.sizes)
        sizes_items_size = len(self.sizes) * 16  # Estimate 8 bytes per key + 8 bytes per value
        
        total_size = object_size + parents_size + parents_items_size + ranks_size + ranks_items_size + sizes_size + sizes_items_size
        
        # Estimate overhead more conservatively
        # Theoretical minimum: 3 integers per element (parent, rank, size) + basic dict overhead
        theoretical_minimum = len(self.parents) * 24  # 3 * 8 bytes per integer + basic overhead
        overhead = max(0, total_size - theoretical_minimum)
        
        return MemoryInfo(
            object_size=object_size,
            total_size=total_size,
            overhead=overhead,
            elements=len(self.parents),
            sets=len(self.get_sets())
        )
    
    def memory_efficiency_report(self) -> str:
        """
        Generate a comprehensive memory efficiency report.
        
        Returns:
            Formatted string containing memory usage analysis
            
        Time Complexity: O(n * α(n)) amortized
        """
        info = self.get_memory_info()
        sets = self.get_sets()
        
        # Handle empty case
        if info.elements == 0:
            return """
Memory Efficiency Report:
=======================
Total elements: 0
Number of sets: 0
Object size: 0 bytes
Total memory: 0 bytes
Memory overhead: 0 bytes
Average memory per element: 0.00 bytes
Memory efficiency: 100.0%
            """
        
        report = f"""
Memory Efficiency Report:
=======================
Total elements: {info.elements}
Number of sets: {info.sets}
Object size: {info.object_size} bytes
Total memory: {info.total_size} bytes
Memory overhead: {info.overhead} bytes
Average memory per element: {info.total_size / info.elements:.2f} bytes
Memory efficiency: {(1 - info.overhead / info.total_size) * 100:.1f}%
        """
        
        if sets:
            set_sizes = [len(s) for s in sets.values()]
            report += f"""
Set size statistics:
- Largest set: {max(set_sizes)} elements
- Smallest set: {min(set_sizes)} elements
- Average set size: {sum(set_sizes) / len(set_sizes):.2f} elements
- Set size variance: {self._calculate_variance(set_sizes):.2f}
            """
        
        # Add tree structure analysis
        tree_info = self._analyze_tree_structure()
        report += f"""
Tree structure analysis:
- Average path length: {tree_info['avg_path_length']:.2f}
- Maximum path length: {tree_info['max_path_length']}
- Path compression efficiency: {tree_info['compression_efficiency']:.2f}
- Tree balance factor: {tree_info['balance_factor']:.2f}
        """
        
        return report
    
    def _calculate_variance(self, values: List[int]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def _analyze_tree_structure(self) -> Dict[str, float]:
        """
        Analyze the tree structure for performance insights.
        
        Returns:
            Dictionary containing tree structure metrics
        """
        if not self.parents:
            return {
                'avg_path_length': 0.0,
                'max_path_length': 0,
                'compression_efficiency': 1.0,
                'balance_factor': 1.0
            }
        
        # Calculate path lengths
        path_lengths = []
        for element in self.parents:
            path_length = 0
            current = element
            while self.parents[current] != current:
                current = self.parents[current]
                path_length += 1
            path_lengths.append(path_length)
        
        avg_path_length = sum(path_lengths) / len(path_lengths)
        max_path_length = max(path_lengths)
        
        # Calculate compression efficiency
        compression_efficiency = 1.0 - (avg_path_length / max_path_length) if max_path_length > 0 else 1.0
        
        # Calculate balance factor (ratio of largest to smallest set)
        sets = self.get_sets()
        if sets:
            set_sizes = [len(s) for s in sets.values()]
            balance_factor = max(set_sizes) / min(set_sizes) if min(set_sizes) > 0 else float('inf')
        else:
            balance_factor = 1.0
        
        return {
            'avg_path_length': avg_path_length,
            'max_path_length': max_path_length,
            'compression_efficiency': compression_efficiency,
            'balance_factor': balance_factor
        }
    
    def get_memory_breakdown(self) -> Dict[str, int]:
        """
        Get detailed breakdown of memory usage by component.
        
        Returns:
            Dictionary mapping component names to their memory usage in bytes
        """
        object_size = sys.getsizeof(self)
        
        # Parents dictionary
        parents_size = sys.getsizeof(self.parents)
        parents_items_size = sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.parents.items())
        
        # Ranks dictionary
        ranks_size = sys.getsizeof(self.ranks)
        ranks_items_size = sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.ranks.items())
        
        # Sizes dictionary
        sizes_size = sys.getsizeof(self.sizes)
        sizes_items_size = sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in self.sizes.items())
        
        return {
            'object_overhead': object_size,
            'parents_dict': parents_size + parents_items_size,
            'ranks_dict': ranks_size + ranks_items_size,
            'sizes_dict': sizes_size + sizes_items_size,
            'total': object_size + parents_size + parents_items_size + ranks_size + ranks_items_size + sizes_size + sizes_items_size
        }
    
    def optimize_memory(self) -> Dict[str, float]:
        """
        Analyze potential memory optimizations.
        
        Returns:
            Dictionary containing optimization suggestions and potential savings
        """
        info = self.get_memory_info()
        breakdown = self.get_memory_breakdown()
        
        # Calculate potential savings from using __slots__
        slots_savings = breakdown['object_overhead'] - 56  # Approximate size with __slots__
        
        # Calculate potential savings from using arrays instead of dictionaries
        array_savings = breakdown['parents_dict'] + breakdown['ranks_dict'] + breakdown['sizes_dict']
        # Assuming we know the maximum element value, we could use arrays
        # This is a rough estimate
        
        total_potential_savings = max(0, slots_savings) + array_savings * 0.3  # 30% savings estimate
        
        return {
            'current_memory': info.total_size,
            'potential_savings': total_potential_savings,
            'savings_percentage': (total_potential_savings / info.total_size) * 100,
            'slots_savings': max(0, slots_savings),
            'array_savings': array_savings * 0.3
        }
    
    def __repr__(self) -> str:
        """String representation with memory information."""
        info = self.get_memory_info()
        sets = self.get_sets()
        sets_str = ", ".join(f"{{{', '.join(map(str, elements))}}}" for elements in sets.values())
        return f"MemoryTrackedDisjointSet({sets_str}) [Memory: {info.total_size} bytes]" 