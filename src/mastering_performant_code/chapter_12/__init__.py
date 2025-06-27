"""
Chapter 12: Disjoint-Set (Union-Find) with Path Compression

This module contains implementations of Union-Find data structures
with various optimizations and real-world applications.
"""

from .disjoint_set import DisjointSet, UnionFindNode
from .optimized_disjoint_set import OptimizedDisjointSet
from .memory_tracked_disjoint_set import MemoryTrackedDisjointSet, MemoryInfo
from .graph_union_find import GraphUnionFind, Edge
from .network_connectivity import NetworkConnectivity
from .image_segmentation import ImageSegmentation
from .analyzer import UnionFindAnalyzer
from .demo import benchmark_comparison, memory_usage_comparison, real_world_application_demo

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