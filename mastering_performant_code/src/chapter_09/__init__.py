"""
Chapter 9: B-Tree Fundamentals

This module provides a comprehensive implementation of B-Trees, including:
- BTreeNode: Individual node structure for B-Trees
- BTree: Complete B-Tree implementation with all operations
- BTreeAnalyzer: Performance analysis and benchmarking tools
- DatabaseIndex: Real-world application using B-Trees

B-Trees are fundamental data structures designed for systems that read and write
large blocks of data, such as databases and file systems. They provide efficient
external storage with guaranteed O(log n) performance for all operations.

Author: Advanced Python Data Structures Book
Version: 1.0
"""

from .btree_node import BTreeNode
from .btree import BTree
from .analyzer import BTreeAnalyzer, BTreeStats, b_tree_height_analysis
from .database_index import DatabaseIndex, IndexEntry, MultiValueIndex, TimestampedIndex

__version__ = "1.0"
__author__ = "Advanced Python Data Structures Book"

__all__ = [
    'BTreeNode',
    'BTree', 
    'BTreeAnalyzer',
    'BTreeStats',
    'b_tree_height_analysis',
    'DatabaseIndex',
    'IndexEntry',
    'MultiValueIndex',
    'TimestampedIndex'
] 