"""
Chapter 12: Disjoint-Set (Union-Find) with Path Compression

This module contains implementations of Union-Find data structures
with various optimizations and real-world applications.
"""

from chapter_12.disjoint_set import DisjointSet, UnionFindNode
from chapter_12.optimized_disjoint_set import OptimizedDisjointSet
from chapter_12.memory_tracked_disjoint_set import MemoryTrackedDisjointSet, MemoryInfo
from chapter_12.graph_union_find import GraphUnionFind, Edge
from chapter_12.network_connectivity import NetworkConnectivity
from chapter_12.image_segmentation import ImageSegmentation
from chapter_12.analyzer import UnionFindAnalyzer
from chapter_12.demo import benchmark_comparison, memory_usage_comparison, real_world_application_demo

__all__ = [
    'DisjointSet',
    'UnionFindNode',
    'OptimizedDisjointSet',
    'MemoryTrackedDisjointSet',
    'MemoryInfo',
    'GraphUnionFind',
    'Edge',
    'NetworkConnectivity',
    'ImageSegmentation',
    'UnionFindAnalyzer',
    'benchmark_comparison',
    'memory_usage_comparison',
    'real_world_application_demo'
] 