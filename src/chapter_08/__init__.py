"""
Chapter 8: Red-Black Tree Implementation

This module contains the complete implementation of Red-Black trees,
including the core data structure, performance analysis, and real-world applications.

Classes:
    - Color: Enumeration for node colors
    - RedBlackNode: Node implementation for Red-Black trees
    - RedBlackTree: Complete Red-Black tree implementation
    - DatabaseIndex: Database indexing application
    - PriorityQueue: Priority queue implementation
    - SymbolTable: Symbol table for compilers

Functions:
    - red_black_height_analysis: Analyze height bounds
    - benchmark_red_black_tree_operations: Performance benchmarking
    - analyze_red_black_properties: Property validation
"""

from .red_black_tree import (
    Color,
    RedBlackNode,
    RedBlackTree,
    red_black_height_analysis,
    benchmark_red_black_tree_operations,
    analyze_red_black_properties
)

from .applications import (
    DatabaseIndex,
    PriorityQueue,
    SymbolTable
)

__all__ = [
    'Color',
    'RedBlackNode', 
    'RedBlackTree',
    'red_black_height_analysis',
    'benchmark_red_black_tree_operations',
    'analyze_red_black_properties',
    'DatabaseIndex',
    'PriorityQueue',
    'SymbolTable'
] 