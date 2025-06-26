"""
Unit tests for optimized node classes and node pool.

This module provides comprehensive tests for the optimized node implementations
and the node pool functionality for memory efficiency.
"""

import pytest
import sys
from typing import List

from src.chapter_04.nodes import (
    OptimizedSinglyNode, 
    OptimizedDoublyNode, 
    NodePool,
    DoublyNode,
    SinglyNode
)


class TestOptimizedSinglyNode:
    """Test cases for OptimizedSinglyNode class."""
    
    def test_init(self):
        """Test initialization of OptimizedSinglyNode."""
        node = OptimizedSinglyNode(42)
        assert node.data == 42
        assert node.next is None
    
    def test_memory_optimization(self):
        """Test that __slots__ provides memory optimization."""
        regular_node = SinglyNode(42)
        optimized_node = OptimizedSinglyNode(42)
        
        # Both should work correctly
        assert regular_node.data == optimized_node.data
        assert regular_node.next is None
        assert optimized_node.next is None
        
        # Check that optimized node has __slots__
        assert hasattr(OptimizedSinglyNode, '__slots__')
        assert 'data' in OptimizedSinglyNode.__slots__
        assert 'next' in OptimizedSinglyNode.__slots__
    
    def test_attribute_assignment(self):
        """Test that attributes can be assigned correctly."""
        node = OptimizedSinglyNode(10)
        node.data = 20
        node.next = OptimizedSinglyNode(30)
        
        assert node.data == 20
        assert node.next.data == 30


class TestOptimizedDoublyNode:
    """Test cases for OptimizedDoublyNode class."""
    
    def test_init(self):
        """Test initialization of OptimizedDoublyNode."""
        node = OptimizedDoublyNode(42)
        assert node.data == 42
        assert node.prev is None
        assert node.next is None
    
    def test_memory_optimization(self):
        """Test that __slots__ provides memory optimization."""
        regular_node = DoublyNode(42)
        optimized_node = OptimizedDoublyNode(42)
        
        # Both should work correctly
        assert regular_node.data == optimized_node.data
        assert regular_node.prev is None
        assert optimized_node.prev is None
        assert regular_node.next is None
        assert optimized_node.next is None
        
        # Check that optimized node has __slots__
        assert hasattr(OptimizedDoublyNode, '__slots__')
        assert 'data' in OptimizedDoublyNode.__slots__
        assert 'prev' in OptimizedDoublyNode.__slots__
        assert 'next' in OptimizedDoublyNode.__slots__
    
    def test_attribute_assignment(self):
        """Test that attributes can be assigned correctly."""
        node = OptimizedDoublyNode(10)
        node.data = 20
        node.prev = OptimizedDoublyNode(5)
        node.next = OptimizedDoublyNode(30)
        
        assert node.data == 20
        assert node.prev.data == 5
        assert node.next.data == 30


class TestNodePool:
    """Test cases for NodePool class."""
    
    def test_init_default_size(self):
        """Test initialization with default size."""
        pool = NodePool()
        assert pool.pool_size() == 100  # Default size
    
    def test_init_custom_size(self):
        """Test initialization with custom size."""
        pool = NodePool(50)
        assert pool.pool_size() == 50
    
    def test_get_node_from_pool(self):
        """Test getting a node from the pool."""
        pool = NodePool(10)
        
        node = pool.get_node(42)
        assert node.data == 42
        assert node.prev is None
        assert node.next is None
        assert pool.pool_size() == 9  # One less in pool
    
    def test_get_node_when_pool_empty(self):
        """Test getting a node when pool is empty."""
        pool = NodePool(1)
        
        # Get the only node in pool
        node1 = pool.get_node(10)
        assert pool.pool_size() == 0
        
        # Get another node (should create new one)
        node2 = pool.get_node(20)
        assert node2.data == 20
        assert pool.pool_size() == 0
    
    def test_return_node_to_pool(self):
        """Test returning a node to the pool."""
        pool = NodePool(5)
        initial_size = pool.pool_size()
        
        node = pool.get_node(42)
        pool.return_node(node)
        
        assert pool.pool_size() == initial_size
    
    def test_return_node_max_size_limit(self):
        """Test that pool doesn't exceed max size."""
        pool = NodePool(1)
        max_size = pool._max_size
        
        # Fill pool to max size
        for i in range(max_size + 10):
            node = DoublyNode(i)
            pool.return_node(node)
        
        assert pool.pool_size() <= max_size
    
    def test_clear_pool(self):
        """Test clearing the pool."""
        pool = NodePool(10)
        assert pool.pool_size() == 10
        
        pool.clear_pool()
        assert pool.pool_size() == 0
    
    def test_node_reuse(self):
        """Test that nodes are properly reused."""
        pool = NodePool(5)
        
        # Get a node and return it
        node1 = pool.get_node(10)
        node1_id = id(node1)
        pool.return_node(node1)
        
        # Get another node (should be the same object)
        node2 = pool.get_node(20)
        assert id(node2) == node1_id
        assert node2.data == 20  # Data should be updated
    
    def test_memory_cleanup(self):
        """Test that returned nodes are properly cleaned up."""
        pool = NodePool(5)
        
        node = pool.get_node(10)
        node.prev = DoublyNode(5)
        node.next = DoublyNode(15)
        
        pool.return_node(node)
        
        # Node should be cleaned up
        assert node.data is None
        assert node.prev is None
        assert node.next is None
    
    def test_pool_size_accuracy(self):
        """Test that pool size is accurate."""
        pool = NodePool(3)
        assert pool.pool_size() == 3
        
        # Get nodes
        node1 = pool.get_node(10)
        node2 = pool.get_node(20)
        assert pool.pool_size() == 1
        
        # Return nodes
        pool.return_node(node1)
        pool.return_node(node2)
        assert pool.pool_size() == 3 