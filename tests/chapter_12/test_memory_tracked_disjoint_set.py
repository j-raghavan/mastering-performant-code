"""
Unit tests for the memory-tracked DisjointSet implementation.

This module tests the Union-Find data structure with memory tracking
capabilities.
"""

import pytest
from typing import List, Tuple

from mastering_performant_code.chapter_12.memory_tracked_disjoint_set import MemoryTrackedDisjointSet, MemoryInfo


class TestMemoryInfo:
    """Test the MemoryInfo dataclass."""
    
    def test_memory_info_creation(self):
        """Test creating a MemoryInfo object."""
        info = MemoryInfo(
            object_size=100,
            total_size=500,
            overhead=50,
            elements=10,
            sets=3
        )
        assert info.object_size == 100
        assert info.total_size == 500
        assert info.overhead == 50
        assert info.elements == 10
        assert info.sets == 3


class TestMemoryTrackedDisjointSet:
    """Test the memory-tracked DisjointSet implementation."""
    
    def test_empty_memory_tracked_disjoint_set(self):
        """Test an empty memory-tracked disjoint set."""
        ds = MemoryTrackedDisjointSet()
        assert len(ds) == 0
        assert ds.size == 0
        assert len(ds.parents) == 0
        assert len(ds.ranks) == 0
        assert len(ds.sizes) == 0
        assert ds._memory_tracking is True
    
    def test_make_set(self):
        """Test creating sets with memory tracking."""
        ds = MemoryTrackedDisjointSet()
        
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
    
    def test_get_memory_info(self):
        """Test getting memory information."""
        ds = MemoryTrackedDisjointSet()
        
        # Empty set
        info = ds.get_memory_info()
        assert isinstance(info, MemoryInfo)
        assert info.elements == 0
        assert info.sets == 0
        assert info.total_size > 0  # Should have some overhead
        
        # Add elements
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        
        info = ds.get_memory_info()
        assert info.elements == 2
        assert info.sets == 1
        assert info.total_size > info.object_size
    
    def test_memory_efficiency_report(self):
        """Test memory efficiency report generation."""
        ds = MemoryTrackedDisjointSet()
        
        # Empty set
        report = ds.memory_efficiency_report()
        assert "Memory Efficiency Report" in report
        assert "Total elements: 0" in report
        
        # Add elements
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.union(1, 2)
        
        report = ds.memory_efficiency_report()
        assert "Total elements: 3" in report
        assert "Number of sets: 2" in report
        assert "Memory efficiency" in report
        assert "Tree structure analysis" in report
    
    def test_calculate_variance(self):
        """Test variance calculation."""
        ds = MemoryTrackedDisjointSet()
        
        # Test with empty list
        variance = ds._calculate_variance([])
        assert variance == 0.0
        
        # Test with single value
        variance = ds._calculate_variance([5])
        assert variance == 0.0
        
        # Test with multiple values
        variance = ds._calculate_variance([1, 2, 3, 4, 5])
        assert variance > 0.0
        assert variance == 2.0  # Variance of [1,2,3,4,5] is 2.0
    
    def test_analyze_tree_structure(self):
        """Test tree structure analysis."""
        ds = MemoryTrackedDisjointSet()
        
        # Empty set
        analysis = ds._analyze_tree_structure()
        assert analysis['avg_path_length'] == 0.0
        assert analysis['max_path_length'] == 0
        assert analysis['compression_efficiency'] == 1.0
        assert analysis['balance_factor'] == 1.0
        
        # Add elements and create a tree
        ds.make_set(1)
        ds.make_set(2)
        ds.make_set(3)
        ds.make_set(4)
        
        ds.union(1, 2)
        ds.union(2, 3)
        ds.union(3, 4)
        
        analysis = ds._analyze_tree_structure()
        assert analysis['avg_path_length'] > 0.0
        assert analysis['max_path_length'] > 0
        assert 0.0 <= analysis['compression_efficiency'] <= 1.0
        assert analysis['balance_factor'] > 0.0
    
    def test_get_memory_breakdown(self):
        """Test memory breakdown analysis."""
        ds = MemoryTrackedDisjointSet()
        
        # Empty set
        breakdown = ds.get_memory_breakdown()
        assert 'object_overhead' in breakdown
        assert 'parents_dict' in breakdown
        assert 'ranks_dict' in breakdown
        assert 'sizes_dict' in breakdown
        assert 'total' in breakdown
        assert breakdown['total'] > 0
        
        # Add elements
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        
        breakdown = ds.get_memory_breakdown()
        assert breakdown['total'] > breakdown['object_overhead']
        assert breakdown['parents_dict'] > 0
        assert breakdown['ranks_dict'] > 0
        assert breakdown['sizes_dict'] > 0
    
    def test_optimize_memory(self):
        """Test memory optimization analysis."""
        ds = MemoryTrackedDisjointSet()
        
        # Add some elements
        for i in range(100):
            ds.make_set(i)
        
        for i in range(50):
            ds.union(i, i + 1)
        
        optimizations = ds.optimize_memory()
        assert 'current_memory' in optimizations
        assert 'potential_savings' in optimizations
        assert 'savings_percentage' in optimizations
        assert 'slots_savings' in optimizations
        assert 'array_savings' in optimizations
        
        assert optimizations['current_memory'] > 0
        assert optimizations['potential_savings'] >= 0
        assert 0.0 <= optimizations['savings_percentage'] <= 100.0
    
    def test_repr_with_memory_info(self):
        """Test string representation with memory information."""
        ds = MemoryTrackedDisjointSet()
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        
        repr_str = repr(ds)
        assert "MemoryTrackedDisjointSet" in repr_str
        assert "Memory:" in repr_str
        assert "bytes" in repr_str
    
    def test_inheritance_from_optimized(self):
        """Test that memory-tracked version inherits all optimized functionality."""
        ds = MemoryTrackedDisjointSet()
        
        # Test basic operations
        ds.make_set(1)
        ds.make_set(2)
        ds.union(1, 2)
        
        assert ds.connected(1, 2)
        assert ds.get_set_size(1) == 2
        assert ds.count_sets() == 1
        
        # Test path compression
        ds.make_set(3)
        ds.make_set(4)
        ds.union(3, 4)
        ds.union(1, 3)
        
        # After find operations, paths should be compressed
        ds.find(4)
        assert ds.parents[4] == ds.find(1)  # Should point directly to root
    
    def test_memory_tracking_accuracy(self):
        """Test that memory tracking provides accurate information."""
        ds = MemoryTrackedDisjointSet()
        
        # Track memory before and after operations
        initial_info = ds.get_memory_info()
        
        # Add elements
        for i in range(10):
            ds.make_set(i)
        
        after_make_info = ds.get_memory_info()
        assert after_make_info.elements == 10
        assert after_make_info.total_size > initial_info.total_size
        
        # Perform unions
        for i in range(5):
            ds.union(i, i + 1)
        
        after_union_info = ds.get_memory_info()
        assert after_union_info.elements == 10
        assert after_union_info.sets == 5  # 5 sets remaining after unions
    
    def test_large_scale_memory_tracking(self):
        """Test memory tracking with large datasets."""
        ds = MemoryTrackedDisjointSet()
        
        # Add many elements
        n = 1000
        for i in range(n):
            ds.make_set(i)
        
        memory_info = ds.get_memory_info()
        assert memory_info.elements == n
        assert memory_info.sets == n
        
        # Perform unions
        for i in range(n - 1):
            ds.union(i, i + 1)
        
        memory_info = ds.get_memory_info()
        assert memory_info.elements == n
        assert memory_info.sets == 1
        
        # Memory should be reasonable (relaxed threshold for Python dicts)
        assert memory_info.total_size < n * 200  # Should not be excessive
    
    def test_memory_efficiency_calculation(self):
        """Test memory efficiency calculation."""
        ds = MemoryTrackedDisjointSet()
        
        # Add elements
        for i in range(100):
            ds.make_set(i)
        
        memory_info = ds.get_memory_info()
        
        # Efficiency should be between 0 and 1
        efficiency = 1.0 - (memory_info.overhead / memory_info.total_size)
        assert 0.0 <= efficiency <= 1.0
        
        # Report should contain efficiency information
        report = ds.memory_efficiency_report()
        assert "Memory efficiency:" in report
        assert "%" in report


if __name__ == "__main__":
    pytest.main([__file__]) 