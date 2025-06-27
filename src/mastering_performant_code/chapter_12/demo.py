"""
Demo module for Chapter 12: Disjoint-Set (Union-Find) with Path Compression.

This module provides demonstration functions and benchmarking tools
for the Union-Find implementations.
"""

import timeit
import sys
from typing import Dict, List, Optional, Tuple

from .disjoint_set import DisjointSet
from .optimized_disjoint_set import OptimizedDisjointSet
from .memory_tracked_disjoint_set import MemoryTrackedDisjointSet
from .network_connectivity import NetworkConnectivity
from .image_segmentation import ImageSegmentation
from .analyzer import UnionFindAnalyzer


def benchmark_comparison():
    """Compare performance of different Union-Find implementations."""
    print("=== Union-Find Performance Comparison ===\n")
    
    # Test with different data sizes
    sizes = [100, 1000, 10000, 100000]
    
    for size in sizes:
        print(f"Performance with {size} elements:")
        print("-" * 40)
        
        # Basic DisjointSet
        basic_make = timeit.timeit(
            f"ds.make_set(i) for i in range({size})",
            setup="from chapter_12 import DisjointSet; ds = DisjointSet()",
            number=1
        )
        
        basic_find = timeit.timeit(
            f"ds.find(i) for i in range({size})",
            setup=f"from chapter_12 import DisjointSet; ds = DisjointSet(); [ds.make_set(i) for i in range({size})]",
            number=1
        )
        
        basic_union = timeit.timeit(
            f"ds.union(i, (i+1)%{size}) for i in range({size})",
            setup=f"from chapter_12 import DisjointSet; ds = DisjointSet(); [ds.make_set(i) for i in range({size})]",
            number=1
        )
        
        # Optimized DisjointSet
        opt_make = timeit.timeit(
            f"ds.make_set(i) for i in range({size})",
            setup="from chapter_12 import OptimizedDisjointSet; ds = OptimizedDisjointSet()",
            number=1
        )
        
        opt_find = timeit.timeit(
            f"ds.find(i) for i in range({size})",
            setup=f"from chapter_12 import OptimizedDisjointSet; ds = OptimizedDisjointSet(); [ds.make_set(i) for i in range({size})]",
            number=1
        )
        
        opt_union = timeit.timeit(
            f"ds.union(i, (i+1)%{size}) for i in range({size})",
            setup=f"from chapter_12 import OptimizedDisjointSet; ds = OptimizedDisjointSet(); [ds.make_set(i) for i in range({size})]",
            number=1
        )
        
        print(f"Make Set {size} elements:")
        print(f"  Basic:      {basic_make:.6f} seconds")
        print(f"  Optimized:  {opt_make:.6f} seconds")
        print(f"  Ratio:      {basic_make/opt_make:.2f}x")
        
        print(f"Find {size} elements:")
        print(f"  Basic:      {basic_find:.6f} seconds")
        print(f"  Optimized:  {opt_find:.6f} seconds")
        print(f"  Ratio:      {basic_find/opt_find:.2f}x")
        
        print(f"Union {size} elements:")
        print(f"  Basic:      {basic_union:.6f} seconds")
        print(f"  Optimized:  {opt_union:.6f} seconds")
        print(f"  Ratio:      {basic_union/opt_union:.2f}x")
        
        print()


def memory_usage_comparison():
    """Compare memory usage of different Union-Find implementations."""
    print("=== Memory Usage Comparison ===\n")
    
    # Test with different data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"Memory usage with {size} elements:")
        print("-" * 40)
        
        # Basic DisjointSet
        basic_ds = DisjointSet()
        for i in range(size):
            basic_ds.make_set(i)
        for i in range(size - 1):
            basic_ds.union(i, i + 1)
        
        basic_memory = sys.getsizeof(basic_ds) + sys.getsizeof(basic_ds.parents) + sys.getsizeof(basic_ds.ranks)
        
        # Optimized DisjointSet
        opt_ds = OptimizedDisjointSet()
        for i in range(size):
            opt_ds.make_set(i)
        for i in range(size - 1):
            opt_ds.union(i, i + 1)
        
        opt_memory = sys.getsizeof(opt_ds) + sys.getsizeof(opt_ds.parents) + sys.getsizeof(opt_ds.ranks) + sys.getsizeof(opt_ds.sizes)
        
        # Memory-tracked version
        tracked_ds = MemoryTrackedDisjointSet()
        for i in range(size):
            tracked_ds.make_set(i)
        for i in range(size - 1):
            tracked_ds.union(i, i + 1)
        
        tracked_memory = tracked_ds.get_memory_info().total_size
        
        print(f"Basic DisjointSet:     {basic_memory} bytes")
        print(f"Optimized DisjointSet: {opt_memory} bytes")
        print(f"Memory-tracked:        {tracked_memory} bytes")
        print(f"Optimized/Basic ratio: {opt_memory/basic_memory:.2f}x")
        print(f"Tracked/Basic ratio:   {tracked_memory/basic_memory:.2f}x")
        print()


def real_world_application_demo():
    """Demonstrate real-world applications of Union-Find."""
    print("=== Real-World Application Demo ===\n")
    
    # Network connectivity example
    print("1. Network Connectivity Analysis:")
    network = NetworkConnectivity()
    
    # Add some connections
    connections = [(1, 2), (2, 3), (4, 5), (5, 6), (3, 4), (7, 8), (8, 9)]
    for u, v in connections:
        network.add_connection(u, v)
    
    print(f"Total networks: {len(network.get_all_networks())}")
    print(f"Networks: {network.get_all_networks()}")
    print(f"Are 1 and 6 connected? {network.are_connected(1, 6)}")
    print(f"Are 1 and 7 connected? {network.are_connected(1, 7)}")
    print(f"Size of network containing 1: {network.get_network_size(1)}")
    
    # Get network statistics
    stats = network.get_network_statistics()
    print(f"Network statistics: {stats}")
    
    # Image segmentation example
    print("\n2. Image Segmentation:")
    img = ImageSegmentation(5, 5)
    
    # Create a simple pattern
    pattern = [
        [1, 1, 0, 2, 2],
        [1, 1, 0, 2, 2],
        [0, 0, 0, 0, 0],
        [3, 3, 0, 4, 4],
        [3, 3, 0, 4, 4]
    ]
    
    for y in range(5):
        for x in range(5):
            img.set_pixel(x, y, pattern[y][x])
    
    print(f"Number of segments: {img.count_segments()}")
    print(f"Segments: {img.get_segments()}")
    print(f"Size of segment at (0,0): {img.get_segment_size(0, 0)}")
    print(f"Size of segment at (3,3): {img.get_segment_size(3, 3)}")
    
    # Get segment statistics
    segment_stats = img.get_segment_statistics()
    print(f"Segment statistics: {segment_stats}")


def tree_structure_analysis_demo():
    """Demonstrate tree structure analysis."""
    print("=== Tree Structure Analysis Demo ===\n")
    
    # Create an optimized disjoint set
    ds = OptimizedDisjointSet()
    
    # Add elements and perform unions
    for i in range(10):
        ds.make_set(i)
    
    # Create some unions to form a tree structure
    unions = [(0, 1), (1, 2), (2, 3), (4, 5), (5, 6), (7, 8), (8, 9), (3, 4), (6, 7)]
    
    for u, v in unions:
        ds.union(u, v)
    
    # Analyze the tree structure
    analysis = UnionFindAnalyzer.analyze_tree_structure(ds)
    
    print("Tree Structure Analysis:")
    print(f"Average path length: {analysis['avg_path_length']:.2f}")
    print(f"Maximum path length: {analysis['max_path_length']}")
    print(f"Average set size: {analysis['avg_set_size']:.2f}")
    print(f"Maximum set size: {analysis['max_set_size']}")
    print(f"Number of sets: {analysis['num_sets']}")
    print(f"Compression efficiency: {analysis['compression_efficiency']:.2f}")
    print(f"Balance factor: {analysis['balance_factor']:.2f}")
    
    # Show the sets
    print(f"\nSets: {ds.get_sets()}")


def memory_tracking_demo():
    """Demonstrate memory tracking capabilities."""
    print("=== Memory Tracking Demo ===\n")
    
    # Create a memory-tracked disjoint set
    ds = MemoryTrackedDisjointSet()
    
    # Add elements and perform operations
    for i in range(100):
        ds.make_set(i)
    
    for i in range(50):
        ds.union(i, i + 1)
    
    # Get memory information
    memory_info = ds.get_memory_info()
    print("Memory Information:")
    print(f"Object size: {memory_info.object_size} bytes")
    print(f"Total size: {memory_info.total_size} bytes")
    print(f"Memory overhead: {memory_info.overhead} bytes")
    print(f"Elements: {memory_info.elements}")
    print(f"Sets: {memory_info.sets}")
    
    # Generate memory efficiency report
    print("\nMemory Efficiency Report:")
    print(ds.memory_efficiency_report())
    
    # Get memory breakdown
    breakdown = ds.get_memory_breakdown()
    print("\nMemory Breakdown:")
    for component, size in breakdown.items():
        print(f"  {component}: {size} bytes")
    
    # Get optimization suggestions
    optimizations = ds.optimize_memory()
    print("\nOptimization Suggestions:")
    print(f"Current memory: {optimizations['current_memory']} bytes")
    print(f"Potential savings: {optimizations['potential_savings']:.0f} bytes")
    print(f"Savings percentage: {optimizations['savings_percentage']:.1f}%")


def stress_test_demo():
    """Demonstrate stress testing capabilities."""
    print("=== Stress Test Demo ===\n")
    
    # Test different implementations
    implementations = [DisjointSet, OptimizedDisjointSet]
    
    for impl_class in implementations:
        print(f"Stress testing {impl_class.__name__}:")
        
        # Perform stress test
        results = UnionFindAnalyzer.stress_test(impl_class, num_operations=5000)
        
        print(f"  Total time: {results['total_time']:.6f} seconds")
        print(f"  Operations per second: {results['operations_per_second']:.0f}")
        print(f"  Final sets: {results['final_sets']}")
        print(f"  Final elements: {results['final_elements']}")
        print()


def scalability_analysis_demo():
    """Demonstrate scalability analysis."""
    print("=== Scalability Analysis Demo ===\n")
    
    # Analyze scalability of optimized implementation
    scalability_data = UnionFindAnalyzer.analyze_scalability(
        OptimizedDisjointSet, 
        max_size=5000, 
        step=500
    )
    
    print("Scalability Analysis Results:")
    print(f"Tested sizes: {scalability_data['sizes']}")
    print(f"Make set times: {[f'{t:.6f}' for t in scalability_data['make_set_times']]}")
    print(f"Find times: {[f'{t:.6f}' for t in scalability_data['find_times']]}")
    print(f"Union times: {[f'{t:.6f}' for t in scalability_data['union_times']]}")
    
    # Calculate complexity ratios
    ratios = UnionFindAnalyzer.calculate_complexity_ratios(
        OptimizedDisjointSet, 
        [100, 500, 1000, 2000, 5000]
    )
    
    print("\nComplexity Ratios (time[i]/time[i-1]):")
    for operation, ratio_list in ratios.items():
        print(f"  {operation}: {[f'{r:.2f}' for r in ratio_list]}")


def comprehensive_demo():
    """Run a comprehensive demonstration of all features."""
    print("Chapter 12: Disjoint-Set (Union-Find) with Path Compression")
    print("=" * 70)
    print()
    
    # Run all demos
    benchmark_comparison()
    memory_usage_comparison()
    real_world_application_demo()
    tree_structure_analysis_demo()
    memory_tracking_demo()
    stress_test_demo()
    scalability_analysis_demo()
    
    print("Demo completed successfully!")


if __name__ == "__main__":
    comprehensive_demo() 