"""
Unit tests for skip list analyzer.

This module provides comprehensive tests for the SkipListAnalyzer class,
ensuring correct analysis and benchmarking functionality.
"""

import pytest
import sys
from src.chapter_05.analyzer import SkipListAnalyzer, SkipListMemoryInfo
from src.chapter_05.skip_list import SkipList


class TestSkipListMemoryInfo:
    """Test cases for SkipListMemoryInfo."""
    
    def test_memory_info_creation(self):
        """Test SkipListMemoryInfo creation."""
        memory_info = SkipListMemoryInfo(
            object_size=100,
            total_size=500,
            overhead=50,
            node_count=10,
            average_height=2.5,
            level_distribution=[5, 3, 2, 0]
        )
        
        assert memory_info.object_size == 100
        assert memory_info.total_size == 500
        assert memory_info.overhead == 50
        assert memory_info.node_count == 10
        assert memory_info.average_height == 2.5
        assert memory_info.level_distribution == [5, 3, 2, 0]


class TestSkipListAnalyzer:
    """Test cases for SkipListAnalyzer."""
    
    def test_analyze_memory_empty(self):
        """Test memory analysis of empty skip list."""
        skip_list = SkipList()
        memory_info = SkipListAnalyzer.analyze_memory(skip_list)
        
        assert memory_info.object_size > 0
        assert memory_info.total_size > 0
        assert memory_info.node_count == 0
        assert memory_info.average_height == 0
        assert len(memory_info.level_distribution) == 16  # max_height
    
    def test_analyze_memory_with_data(self):
        """Test memory analysis of skip list with data."""
        skip_list = SkipList()
        
        # Add some elements
        for i in range(10):
            skip_list.insert(i)
        
        memory_info = SkipListAnalyzer.analyze_memory(skip_list)
        
        assert memory_info.object_size > 0
        assert memory_info.total_size > memory_info.object_size
        assert memory_info.node_count == 10
        assert memory_info.average_height > 0
        assert sum(memory_info.level_distribution) == 10
    
    def test_analyze_memory_large_dataset(self):
        """Test memory analysis with larger dataset."""
        skip_list = SkipList()
        
        # Add 1000 elements
        for i in range(1000):
            skip_list.insert(i)
        
        memory_info = SkipListAnalyzer.analyze_memory(skip_list)
        
        assert memory_info.node_count == 1000
        assert memory_info.average_height > 0
        assert sum(memory_info.level_distribution) == 1000
        
        # Memory usage should be reasonable
        assert memory_info.total_size < 1024 * 1024  # Less than 1MB
    
    def test_benchmark_operations(self):
        """Test benchmarking operations."""
        skip_list = SkipList()
        
        # Add some data for benchmarking
        for i in range(100):
            skip_list.insert(i)
        
        operations = ["search", "insert", "delete"]
        results = SkipListAnalyzer.benchmark_operations(skip_list, operations, iterations=10)
        
        assert "search" in results
        assert "insert" in results
        assert "delete" in results
        
        # All operations should take some time
        for operation, time_taken in results.items():
            assert time_taken > 0
    
    def test_analyze_height_distribution(self):
        """Test height distribution analysis."""
        skip_list = SkipList(max_height=4, probability=0.5)
        
        distribution = SkipListAnalyzer.analyze_height_distribution(skip_list, num_samples=1000)
        
        # Should have distribution for different heights
        assert len(distribution) > 0
        
        # Probabilities should sum to 1
        total_probability = sum(distribution.values())
        assert abs(total_probability - 1.0) < 0.01
        
        # All probabilities should be positive
        for probability in distribution.values():
            assert probability > 0
    
    def test_compare_with_alternatives(self):
        """Test comparison with alternative data structures."""
        skip_list = SkipList()
        test_data = list(range(100))
        
        results = SkipListAnalyzer.compare_with_alternatives(skip_list, test_data)
        
        assert "skip_list" in results
        assert "list" in results
        assert "set" in results
        
        for structure, times in results.items():
            assert "insert" in times
            assert "search" in times
            assert "delete" in times
            
            for operation, time_taken in times.items():
                assert time_taken > 0
    
    def test_analyze_memory_comparison(self):
        """Test memory comparison with alternatives."""
        skip_list = SkipList()
        test_data = list(range(100))
        
        results = SkipListAnalyzer.analyze_memory_comparison(skip_list, test_data)
        
        assert "skip_list" in results
        assert "list" in results
        assert "set" in results
        
        for structure, info in results.items():
            assert "total_size" in info
            assert "node_count" in info
            assert "average_height" in info
            assert "overhead" in info
            
            assert info["total_size"] > 0
            assert info["node_count"] >= 0
            assert info["average_height"] >= 0
    
    def test_generate_performance_report(self):
        """Test performance report generation."""
        skip_list = SkipList()
        test_data = list(range(100))
        
        # Add data to skip list
        for item in test_data:
            skip_list.insert(item)
        
        report = SkipListAnalyzer.generate_performance_report(skip_list, test_data)
        
        # Report should be a string
        assert isinstance(report, str)
        assert len(report) > 0
        
        # Should contain expected sections
        assert "Memory Analysis:" in report
        assert "Level Distribution:" in report
        assert "Performance Comparison:" in report
        assert "Memory Comparison:" in report
    
    def test_benchmark_operations_empty_list(self):
        """Test benchmarking with empty skip list."""
        skip_list = SkipList()
        
        operations = ["insert"]
        results = SkipListAnalyzer.benchmark_operations(skip_list, operations, iterations=5)
        
        assert "insert" in results
        assert results["insert"] > 0
    
    def test_analyze_height_distribution_edge_cases(self):
        """Test height distribution analysis with edge cases."""
        # Test with probability 0 (all nodes height 1)
        skip_list = SkipList(max_height=4, probability=0.0)
        distribution = SkipListAnalyzer.analyze_height_distribution(skip_list, num_samples=100)
        
        assert 1 in distribution
        assert distribution[1] == 1.0  # All nodes should be height 1
        
        # Test with probability 1 (nodes can reach max height)
        skip_list = SkipList(max_height=4, probability=1.0)
        distribution = SkipListAnalyzer.analyze_height_distribution(skip_list, num_samples=100)
        
        # Should have nodes at max height
        assert 4 in distribution
        assert distribution[4] > 0
    
    def test_memory_analysis_edge_cases(self):
        """Test memory analysis with edge cases."""
        # Test with single element
        skip_list = SkipList()
        skip_list.insert(42)
        
        memory_info = SkipListAnalyzer.analyze_memory(skip_list)
        assert memory_info.node_count == 1
        assert memory_info.average_height > 0
        
        # Test with maximum height constraint
        skip_list = SkipList(max_height=2)
        for i in range(10):
            skip_list.insert(i)
        
        memory_info = SkipListAnalyzer.analyze_memory(skip_list)
        assert memory_info.node_count == 10
        assert memory_info.average_height <= 2
    
    def test_benchmark_operations_invalid_operation(self):
        """Test benchmarking with invalid operation."""
        skip_list = SkipList()
        
        operations = ["invalid_operation"]
        results = SkipListAnalyzer.benchmark_operations(skip_list, operations, iterations=5)
        
        # Should not contain invalid operation
        assert "invalid_operation" not in results
        assert len(results) == 0
    
    def test_performance_report_empty_list(self):
        """Test performance report with empty skip list."""
        skip_list = SkipList()
        test_data = []
        
        report = SkipListAnalyzer.generate_performance_report(skip_list, test_data)
        
        assert isinstance(report, str)
        assert "Memory Analysis:" in report
        assert "node count: 0" in report.lower()
    
    def test_memory_comparison_empty_data(self):
        """Test memory comparison with empty data."""
        skip_list = SkipList()
        test_data = []
        
        results = SkipListAnalyzer.analyze_memory_comparison(skip_list, test_data)
        
        assert "skip_list" in results
        assert "list" in results
        assert "set" in results
        
        for structure, info in results.items():
            assert info["node_count"] == 0


if __name__ == "__main__":
    pytest.main([__file__]) 