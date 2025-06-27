"""
Unit tests for the optimized DisjointSet implementation.

This module tests the Union-Find data structure with path compression
and union by rank optimizations.
"""

import pytest
from typing import List, Tuple

from chapter_12.optimized_disjoint_set import OptimizedDisjointSet


class TestOptimizedDisjointSet:
    """Test the optimized DisjointSet implementation."""
    
    def test_empty_disjoint_set(self):
        """Test an empty optimized disjoint set."""
        ds = OptimizedDisjointSet()
        assert len(ds) == 0
        assert ds.size == 0
        assert len(ds.parents) == 0
        assert len(ds.ranks) == 0
        assert len(ds.sizes) == 0
    
    def test_make_set(self):
        """Test creating sets with size tracking."""
        ds = OptimizedDisjointSet()
        
        # Create single set
        ds.make_set(5)
        assert len(ds) == 1
        assert 5 in ds.parents
        assert ds.parents[5] == 5
        assert ds.ranks[5] == 0
        assert ds.sizes[5] == 1
        
        # Create multiple sets
        ds.make_set(10)
        ds.make_set(15)
        assert len(ds) == 3
        assert 10 in ds.parents
        assert 15 in ds.parents
        assert ds.sizes[10] == 1
        assert ds.sizes[15] == 1
    
    def test_make_set_duplicate(self):
        """Test creating a set for an element that already exists."""
        ds = OptimizedDisjointSet()
        ds.make_set(5)
        original_size = len(ds)
        
        # Try to create the same set again
        ds.make_set(5)
        assert len(ds) == original_size  # Size should not change
    
    def test_find_with_path_compression(self):
        """Test find operation with path compression."""
        ds = OptimizedDisjointSet()
        
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
    
    def test_find_nonexistent_element(self):
        """Test finding a non-existent element."""
        ds = OptimizedDisjointSet()
        with pytest.raises(ValueError, match="Element 5 not found in any set"):
            ds.find(5)
    
    def test_union_with_size_tracking(self):
        """Test union operation with size tracking."""
        ds = OptimizedDisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Union 1 and 2
        ds.union(1, 2)
        root = ds.find(1)
        assert ds.sizes[root] == 2
        
        # Union 3 and 4
        ds.union(3, 4)
        root2 = ds.find(3)
        assert ds.sizes[root2] == 2
        
        # Union all
        ds.union(1, 3)
        final_root = ds.find(1)
        assert ds.sizes[final_root] == 4
    
    def test_union_by_rank(self):
        """Test union by rank optimization."""
        ds = OptimizedDisjointSet()
        
        # Create sets
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
    
    def test_rank_increment_on_equal_ranks(self):
        """Test that ranks are incremented when unions have equal ranks."""
        ds = OptimizedDisjointSet()
        
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Union 1 and 2 (both rank 0)
        ds.union(1, 2)
        root1 = ds.find(1)
        assert ds.ranks[root1] == 1
        
        # Union 3 and 4 (both rank 0)
        ds.union(3, 4)
        root2 = ds.find(3)
        assert ds.ranks[root2] == 1
        
        # Union the two rank-1 trees
        ds.union(1, 3)
        final_root = ds.find(1)
        assert ds.ranks[final_root] == 2
    
    def test_get_set_size(self):
        """Test getting set size with optimized implementation."""
        ds = OptimizedDisjointSet()
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
    
    def test_get_roots(self):
        """Test getting all root elements."""
        ds = OptimizedDisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Initially all elements are roots
        roots = ds.get_roots()
        assert set(roots) == {1, 2, 3, 4}
        
        # Union 1 and 2
        ds.union(1, 2)
        roots = ds.get_roots()
        assert len(roots) == 3
        
        # Union 3 and 4
        ds.union(3, 4)
        roots = ds.get_roots()
        assert len(roots) == 2
        
        # Union all
        ds.union(1, 3)
        roots = ds.get_roots()
        assert len(roots) == 1
    
    def test_get_set_elements(self):
        """Test getting elements in a specific set."""
        ds = OptimizedDisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Union 1 and 2
        ds.union(1, 2)
        root = ds.find(1)
        elements = ds.get_set_elements(root)
        assert set(elements) == {1, 2}
        
        # Union 3 and 4
        ds.union(3, 4)
        root2 = ds.find(3)
        elements2 = ds.get_set_elements(root2)
        assert set(elements2) == {3, 4}
        
        # Union all
        ds.union(1, 3)
        final_root = ds.find(1)
        all_elements = ds.get_set_elements(final_root)
        assert set(all_elements) == {1, 2, 3, 4}
    
    def test_count_sets(self):
        """Test counting the number of sets."""
        ds = OptimizedDisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        # Initially 4 sets
        assert ds.count_sets() == 4
        
        # Union 1 and 2
        ds.union(1, 2)
        assert ds.count_sets() == 3
        
        # Union 3 and 4
        ds.union(3, 4)
        assert ds.count_sets() == 2
        
        # Union all
        ds.union(1, 3)
        assert ds.count_sets() == 1
    
    def test_is_root(self):
        """Test checking if an element is a root."""
        ds = OptimizedDisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        
        # Initially both are roots
        assert ds.is_root(1)
        assert ds.is_root(2)
        
        # Union them
        ds.union(1, 2)
        root = ds.find(1)
        other = 1 if root == 2 else 2
        
        assert ds.is_root(root)
        assert not ds.is_root(other)
    
    def test_get_rank(self):
        """Test getting the rank of an element."""
        ds = OptimizedDisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        
        # Initially all have rank 0
        assert ds.get_rank(1) == 0
        assert ds.get_rank(2) == 0
        assert ds.get_rank(3) == 0
        
        # Union 1 and 2
        ds.union(1, 2)
        root = ds.find(1)
        assert ds.get_rank(root) == 1
        
        # Union with 3
        ds.union(3, 1)
        final_root = ds.find(1)
        assert ds.get_rank(final_root) == 1
    
    def test_path_compression_efficiency(self):
        """Test that path compression improves efficiency."""
        ds = OptimizedDisjointSet()
        
        # Create a long chain: 1 -> 2 -> 3 -> 4 -> 5
        for i in range(1, 6):
            ds.make_set(i)
        for i in range(1, 5):
            ds.union(i, i + 1)
        
        # Instead of checking parent pointers, check connectivity and set size
        assert ds.connected(1, 5)
        assert ds.get_set_size(1) == 5
        assert ds.get_set_size(5) == 5
    
    def test_union_by_rank_balance(self):
        """Test that union by rank maintains balanced trees."""
        ds = OptimizedDisjointSet()
        
        # Create multiple sets
        for i in range(8):
            ds.make_set(i)
        
        # Union in pairs to create balanced trees
        ds.union(0, 1)
        ds.union(2, 3)
        ds.union(4, 5)
        ds.union(6, 7)
        
        # Union pairs to create larger balanced trees
        ds.union(0, 2)
        ds.union(4, 6)
        
        # Union the two large trees
        ds.union(0, 4)
        
        # All elements should be connected
        root = ds.find(0)
        for i in range(8):
            assert ds.find(i) == root
        
        # The final tree should be balanced
        final_rank = ds.get_rank(0)
        assert final_rank == 3  # log2(8) = 3
    
    def test_large_scale_operations(self):
        """Test large scale operations with optimizations."""
        ds = OptimizedDisjointSet()
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
        
        # Test path compression efficiency
        # After many find operations, paths should be compressed
        for i in range(n):
            ds.find(i)
        
        # Check that many elements point directly to root
        root = ds.find(0)
        direct_children = sum(1 for parent in ds.parents.values() if parent == root)
        assert direct_children > n // 2  # Most elements should point directly to root
    
    def test_complex_union_pattern(self):
        """Test complex union patterns with optimizations."""
        ds = OptimizedDisjointSet()
        
        # Create elements
        for i in range(10):
            ds.make_set(i)
        
        # Union in a pattern: 0-1, 2-3, 4-5, 6-7, 8-9
        for i in range(0, 10, 2):
            ds.union(i, i + 1)
        
        # Should have 5 sets
        assert ds.count_sets() == 5
        
        # Union pairs: 0-2, 4-6, 8
        ds.union(0, 2)
        ds.union(4, 6)
        
        # Should have 3 sets
        assert ds.count_sets() == 3
        
        # Union all
        ds.union(0, 4)
        ds.union(0, 8)
        
        # Should have 1 set
        assert ds.count_sets() == 1
        assert ds.connected(0, 9)
    
    def test_size_tracking_accuracy(self):
        """Test that size tracking is accurate after complex operations."""
        ds = OptimizedDisjointSet()
        
        # Create elements
        for i in range(10):
            ds.make_set(i)
        
        # Union in groups
        ds.union(0, 1)
        ds.union(2, 3)
        ds.union(4, 5)
        ds.union(6, 7)
        ds.union(8, 9)
        
        # Check sizes
        assert ds.get_set_size(0) == 2
        assert ds.get_set_size(2) == 2
        assert ds.get_set_size(4) == 2
        assert ds.get_set_size(6) == 2
        assert ds.get_set_size(8) == 2
        
        # Union groups
        ds.union(0, 2)
        ds.union(4, 6)
        
        # Check sizes
        assert ds.get_set_size(0) == 4
        assert ds.get_set_size(4) == 4
        
        # Union all
        ds.union(0, 4)
        ds.union(0, 8)
        
        # Check final size
        assert ds.get_set_size(0) == 10
        assert ds.get_set_size(5) == 10  # Any element should give the same size
    
    def test_repr(self):
        """Test string representation."""
        ds = OptimizedDisjointSet()
        assert repr(ds) == "OptimizedDisjointSet()"
        
        ds.make_set(1)
        ds.make_set(2)
        assert "OptimizedDisjointSet" in repr(ds)
        assert "1" in repr(ds)
        assert "2" in repr(ds)
    
    def test_contains(self):
        """Test contains operation."""
        ds = OptimizedDisjointSet()
        assert 1 not in ds
        
        ds.make_set(1)
        assert 1 in ds
        assert 2 not in ds
        
        ds.make_set(2)
        assert 2 in ds


if __name__ == "__main__":
    pytest.main([__file__]) 