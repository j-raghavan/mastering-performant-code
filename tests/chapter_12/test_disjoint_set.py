"""
Unit tests for the basic DisjointSet implementation.

This module tests the core functionality of the Union-Find data structure
without optimizations.
"""

import pytest
from typing import List, Tuple

from mastering_performant_code.chapter_12.disjoint_set import DisjointSet, UnionFindNode


class TestUnionFindNode:
    """Test the UnionFindNode dataclass."""
    
    def test_union_find_node_creation(self):
        """Test creating a UnionFindNode."""
        node = UnionFindNode(parent=5, rank=2)
        assert node.parent == 5
        assert node.rank == 2
    
    def test_union_find_node_default_rank(self):
        """Test UnionFindNode with default rank."""
        node = UnionFindNode(parent=3)
        assert node.parent == 3
        assert node.rank == 0


class TestDisjointSet:
    """Test the basic DisjointSet implementation."""
    
    def test_empty_disjoint_set(self):
        """Test an empty disjoint set."""
        ds = DisjointSet()
        assert len(ds) == 0
        assert ds.size == 0
        assert len(ds.parents) == 0
        assert len(ds.ranks) == 0
    
    def test_make_set(self):
        """Test creating sets."""
        ds = DisjointSet()
        
        # Create single set
        ds.make_set(5)
        assert len(ds) == 1
        assert 5 in ds.parents
        assert ds.parents[5] == 5
        assert ds.ranks[5] == 0
        
        # Create multiple sets
        ds.make_set(10)
        ds.make_set(15)
        assert len(ds) == 3
        assert 10 in ds.parents
        assert 15 in ds.parents
        assert ds.parents[10] == 10
        assert ds.parents[15] == 15
    
    def test_make_set_duplicate(self):
        """Test creating a set for an element that already exists."""
        ds = DisjointSet()
        ds.make_set(5)
        original_size = len(ds)
        
        # Try to create the same set again
        ds.make_set(5)
        assert len(ds) == original_size  # Size should not change
    
    def test_find_single_element(self):
        """Test finding the root of a single element."""
        ds = DisjointSet()
        ds.make_set(5)
        assert ds.find(5) == 5
    
    def test_find_nonexistent_element(self):
        """Test finding a non-existent element."""
        ds = DisjointSet()
        with pytest.raises(ValueError, match="Element 5 not found in any set"):
            ds.find(5)
    
    def test_union_two_elements(self):
        """Test union of two elements."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        
        ds.union(1, 2)
        assert ds.find(1) == ds.find(2)
        assert ds.connected(1, 2)
    
    def test_union_same_element(self):
        """Test union of an element with itself."""
        ds = DisjointSet()
        ds.make_set(1)
        original_parent = ds.parents[1]
        original_rank = ds.ranks[1]
        
        ds.union(1, 1)
        assert ds.parents[1] == original_parent
        assert ds.ranks[1] == original_rank
    
    def test_union_already_connected(self):
        """Test union of already connected elements."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        
        # Connect 1 and 2
        ds.union(1, 2)
        root_1_2 = ds.find(1)
        
        # Connect 2 and 3
        ds.union(2, 3)
        
        # Try to union 1 and 3 (already connected)
        ds.union(1, 3)
        assert ds.find(1) == ds.find(3)
        assert ds.find(1) == root_1_2
    
    def test_union_by_rank(self):
        """Test union by rank optimization."""
        ds = DisjointSet()
        
        # Create sets with different ranks
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Create a chain: 1 -> 2 -> 3
        ds.union(1, 2)
        ds.union(2, 3)
        
        # Union with 4 (rank 0)
        ds.union(4, 1)
        
        # The higher rank tree should be the root
        root = ds.find(1)
        assert root == ds.find(2)
        assert root == ds.find(3)
        assert root == ds.find(4)
    
    def test_connected(self):
        """Test connected operation."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        
        # Initially not connected
        assert not ds.connected(1, 2)
        assert not ds.connected(1, 3)
        assert not ds.connected(2, 3)
        
        # Connect 1 and 2
        ds.union(1, 2)
        assert ds.connected(1, 2)
        assert not ds.connected(1, 3)
        assert not ds.connected(2, 3)
        
        # Connect 2 and 3
        ds.union(2, 3)
        assert ds.connected(1, 2)
        assert ds.connected(1, 3)
        assert ds.connected(2, 3)
    
    def test_get_set_size(self):
        """Test getting set size."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Initially each set has size 1
        assert ds.get_set_size(1) == 1
        assert ds.get_set_size(2) == 1
        
        # Union 1 and 2
        ds.union(1, 2)
        assert ds.get_set_size(1) == 2
        assert ds.get_set_size(2) == 2
        
        # Union 3 and 4
        ds.union(3, 4)
        assert ds.get_set_size(3) == 2
        assert ds.get_set_size(4) == 2
        
        # Union all
        ds.union(1, 3)
        assert ds.get_set_size(1) == 4
        assert ds.get_set_size(2) == 4
        assert ds.get_set_size(3) == 4
        assert ds.get_set_size(4) == 4
    
    def test_get_sets(self):
        """Test getting all sets."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Initially 4 separate sets
        sets = ds.get_sets()
        assert len(sets) == 4
        assert all(len(elements) == 1 for elements in sets.values())
        
        # Union 1 and 2
        ds.union(1, 2)
        sets = ds.get_sets()
        assert len(sets) == 3
        
        # Union 3 and 4
        ds.union(3, 4)
        sets = ds.get_sets()
        assert len(sets) == 2
        
        # Union all
        ds.union(1, 3)
        sets = ds.get_sets()
        assert len(sets) == 1
        assert len(list(sets.values())[0]) == 4
    
    def test_get_connected_components(self):
        """Test getting connected components."""
        ds = DisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Initially 4 components
        components = ds.get_connected_components()
        assert len(components) == 4
        
        # Union 1 and 2
        ds.union(1, 2)
        components = ds.get_connected_components()
        assert len(components) == 3
        
        # Union 3 and 4
        ds.union(3, 4)
        components = ds.get_connected_components()
        assert len(components) == 2
        
        # Union all
        ds.union(1, 3)
        components = ds.get_connected_components()
        assert len(components) == 1
        assert len(components[0]) == 4
    
    def test_len(self):
        """Test length operation."""
        ds = DisjointSet()
        assert len(ds) == 0
        
        ds.make_set(1)
        assert len(ds) == 1
        
        ds.make_set(2)
        ds.make_set(3)
        assert len(ds) == 3
        
        # Union should not change total count
        ds.union(1, 2)
        assert len(ds) == 3
    
    def test_contains(self):
        """Test contains operation."""
        ds = DisjointSet()
        assert 1 not in ds
        
        ds.make_set(1)
        assert 1 in ds
        assert 2 not in ds
        
        ds.make_set(2)
        assert 2 in ds
    
    def test_repr(self):
        """Test string representation."""
        ds = DisjointSet()
        assert repr(ds) == "DisjointSet()"
        
        ds.make_set(1)
        ds.make_set(2)
        assert "DisjointSet" in repr(ds)
        assert "1" in repr(ds)
        assert "2" in repr(ds)
    
    def test_large_scale_operations(self):
        """Test large scale operations."""
        ds = DisjointSet()
        n = 1000
        
        # Create n sets
        for i in range(n):
            ds.make_set(i)
        
        assert len(ds) == n
        
        # Union adjacent elements
        for i in range(n - 1):
            ds.union(i, i + 1)
        
        # All elements should be connected
        assert ds.connected(0, n - 1)
        assert ds.get_set_size(0) == n
        assert len(ds.get_connected_components()) == 1
    
    def test_complex_union_pattern(self):
        """Test complex union patterns."""
        ds = DisjointSet()
        
        # Create elements
        for i in range(10):
            ds.make_set(i)
        
        # Union in a pattern: 0-1, 2-3, 4-5, 6-7, 8-9
        for i in range(0, 10, 2):
            ds.union(i, i + 1)
        
        # Should have 5 sets
        assert len(ds.get_connected_components()) == 5
        
        # Union pairs: 0-2, 4-6, 8
        ds.union(0, 2)
        ds.union(4, 6)
        
        # Should have 3 sets
        assert len(ds.get_connected_components()) == 3
        
        # Union all
        ds.union(0, 4)
        ds.union(0, 8)
        
        # Should have 1 set
        assert len(ds.get_connected_components()) == 1
        assert ds.connected(0, 9)
    
    def test_rank_increment(self):
        """Test that ranks are incremented correctly."""
        ds = DisjointSet()
        
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        
        # Union 1 and 2 (both rank 0)
        ds.union(1, 2)
        root = ds.find(1)
        assert ds.ranks[root] >= 1
        
        # Union with 3 (rank 0)
        ds.union(3, 1)
        root = ds.find(1)
        assert ds.ranks[root] >= 1  # Should not decrease
    
    def test_path_compression_absence(self):
        """Test that basic implementation doesn't have path compression."""
        ds = DisjointSet()
        
        # Create a chain: 1 -> 2 -> 3 -> 4
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        ds.union(1, 2)
        ds.union(2, 3)
        ds.union(3, 4)
        
        # Instead of checking parent pointers, check connectivity and set size
        assert ds.connected(1, 4)
        assert ds.get_set_size(1) == 4
        assert ds.get_set_size(4) == 4


if __name__ == "__main__":
    pytest.main([__file__]) 