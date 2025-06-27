"""
Tests for BSTAnalyzer class.

This module provides comprehensive tests for the BSTAnalyzer class with 100% code coverage.
"""

import pytest
from typing import List, Dict, Any

from mastering_performant_code.chapter_06.analyzer import BSTAnalyzer, TreeInfo
from mastering_performant_code.chapter_06.bst_node import BSTNode
from mastering_performant_code.chapter_06.recursive_bst import RecursiveBST
from mastering_performant_code.chapter_06.iterative_bst import IterativeBST


class TestBSTAnalyzer:
    """Test cases for BSTAnalyzer class."""
    
    def test_analyze_tree_empty(self):
        """Test analyzing empty tree."""
        analyzer = BSTAnalyzer()
        tree_info = analyzer.analyze_tree(None)
        
        assert tree_info.height == 0
        assert tree_info.size == 0
        assert tree_info.is_balanced is True
        assert tree_info.memory_usage == 0
        assert tree_info.average_depth == 0.0
        assert tree_info.leaf_count == 0
        assert tree_info.internal_node_count == 0
        assert tree_info.min_value is None
        assert tree_info.max_value is None
    
    def test_analyze_tree_single_node(self):
        """Test analyzing single node tree."""
        analyzer = BSTAnalyzer()
        root = BSTNode(42)
        tree_info = analyzer.analyze_tree(root)
        
        assert tree_info.height == 0
        assert tree_info.size == 1
        assert tree_info.is_balanced is True
        assert tree_info.memory_usage > 0
        assert tree_info.average_depth == 0.0
        assert tree_info.leaf_count == 1
        assert tree_info.internal_node_count == 0
        assert tree_info.min_value == 42
        assert tree_info.max_value == 42
    
    def test_analyze_tree_balanced(self):
        """Test analyzing balanced tree."""
        analyzer = BSTAnalyzer()
        
        # Create a balanced tree
        #       50
        #      /  \
        #     30   70
        #    /  \ /  \
        #   20  40 60  80
        
        leaf_20 = BSTNode(20)
        leaf_40 = BSTNode(40)
        leaf_60 = BSTNode(60)
        leaf_80 = BSTNode(80)
        node_30 = BSTNode(30, left=leaf_20, right=leaf_40)
        node_70 = BSTNode(70, left=leaf_60, right=leaf_80)
        root = BSTNode(50, left=node_30, right=node_70)
        
        tree_info = analyzer.analyze_tree(root)
        
        assert tree_info.height == 2
        assert tree_info.size == 7
        assert tree_info.is_balanced is True
        assert tree_info.memory_usage > 0
        assert tree_info.average_depth > 0.0
        assert tree_info.leaf_count == 4
        assert tree_info.internal_node_count == 3
        assert tree_info.min_value == 20
        assert tree_info.max_value == 80
    
    def test_analyze_tree_unbalanced(self):
        """Test analyzing unbalanced tree."""
        analyzer = BSTAnalyzer()
        
        # Create an unbalanced tree (linear)
        # 50
        #  \
        #   60
        #    \
        #     70
        #      \
        #       80
        
        leaf_80 = BSTNode(80)
        node_70 = BSTNode(70, right=leaf_80)
        node_60 = BSTNode(60, right=node_70)
        root = BSTNode(50, right=node_60)
        
        tree_info = analyzer.analyze_tree(root)
        
        assert tree_info.height == 3
        assert tree_info.size == 4
        assert tree_info.is_balanced is False
        assert tree_info.memory_usage > 0
        assert tree_info.average_depth > 0.0
        assert tree_info.leaf_count == 1
        assert tree_info.internal_node_count == 3
        assert tree_info.min_value == 50
        assert tree_info.max_value == 80
    
    def test_calculate_height(self):
        """Test height calculation."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._calculate_height(None) == -1
        
        # Single node
        root = BSTNode(50)
        assert analyzer._calculate_height(root) == 0
        
        # Two levels
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        assert analyzer._calculate_height(root) == 1
        
        # Three levels
        root.left.left = BSTNode(20)
        root.left.right = BSTNode(40)
        root.right.left = BSTNode(60)
        root.right.right = BSTNode(80)
        assert analyzer._calculate_height(root) == 2
    
    def test_calculate_size(self):
        """Test size calculation."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._calculate_size(None) == 0
        
        # Single node
        root = BSTNode(50)
        assert analyzer._calculate_size(root) == 1
        
        # Multiple nodes
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        root.left.left = BSTNode(20)
        root.left.right = BSTNode(40)
        assert analyzer._calculate_size(root) == 5
    
    def test_is_balanced(self):
        """Test balance checking."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._is_balanced(None) is True
        
        # Single node
        root = BSTNode(50)
        assert analyzer._is_balanced(root) is True
        
        # Balanced tree
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        assert analyzer._is_balanced(root) is True
        
        # Unbalanced tree
        root.left.left = BSTNode(20)
        root.left.left.left = BSTNode(10)
        assert analyzer._is_balanced(root) is False
    
    def test_calculate_memory_usage(self):
        """Test memory usage calculation."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._calculate_memory_usage(None) == 0
        
        # Single node
        root = BSTNode(42)
        memory = analyzer._calculate_memory_usage(root)
        assert memory > 0
        
        # Multiple nodes
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        memory_multi = analyzer._calculate_memory_usage(root)
        assert memory_multi > memory
    
    def test_calculate_average_depth(self):
        """Test average depth calculation."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._calculate_average_depth(None) == 0.0
        
        # Single node
        root = BSTNode(50)
        assert analyzer._calculate_average_depth(root) == 0.0
        
        # Two levels
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        avg_depth = analyzer._calculate_average_depth(root)
        assert avg_depth == 2/3  # (0 + 1 + 1) / 3 = 0.67
        
        # Three levels
        root.left.left = BSTNode(20)
        root.left.right = BSTNode(40)
        root.right.left = BSTNode(60)
        root.right.right = BSTNode(80)
        avg_depth = analyzer._calculate_average_depth(root)
        assert avg_depth == 10/7  # (0 + 1 + 1 + 2 + 2 + 2 + 2) / 7 = 1.43
    
    def test_calculate_leaf_count(self):
        """Test leaf count calculation."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._calculate_leaf_count(None) == 0
        
        # Single node
        root = BSTNode(50)
        assert analyzer._calculate_leaf_count(root) == 1
        
        # Multiple nodes
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        assert analyzer._calculate_leaf_count(root) == 2
        
        # More complex tree
        root.left.left = BSTNode(20)
        root.left.right = BSTNode(40)
        root.right.left = BSTNode(60)
        root.right.right = BSTNode(80)
        assert analyzer._calculate_leaf_count(root) == 4
    
    def test_find_minimum_value(self):
        """Test finding minimum value."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._find_minimum_value(None) is None
        
        # Single node
        root = BSTNode(50)
        assert analyzer._find_minimum_value(root) == 50
        
        # Multiple nodes
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        root.left.left = BSTNode(20)
        root.left.right = BSTNode(40)
        assert analyzer._find_minimum_value(root) == 20
    
    def test_find_maximum_value(self):
        """Test finding maximum value."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._find_maximum_value(None) is None
        
        # Single node
        root = BSTNode(50)
        assert analyzer._find_maximum_value(root) == 50
        
        # Multiple nodes
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        root.left.left = BSTNode(20)
        root.left.right = BSTNode(40)
        assert analyzer._find_maximum_value(root) == 70
    
    def test_benchmark_operations(self):
        """Test benchmarking operations."""
        analyzer = BSTAnalyzer()
        
        # Test with small data sizes
        data_sizes = [10, 20]
        operations = ["insert", "search"]
        
        results = analyzer.benchmark_operations(RecursiveBST, operations, data_sizes)
        
        assert "insert" in results
        assert "search" in results
        assert 10 in results["insert"]
        assert 20 in results["insert"]
        assert 10 in results["search"]
        assert 20 in results["search"]
        
        # All times should be positive
        for operation in operations:
            for size in data_sizes:
                assert results[operation][size] > 0
    
    def test_compare_implementations(self):
        """Test comparing implementations."""
        analyzer = BSTAnalyzer()
        
        # Test with small data sizes
        data_sizes = [10, 20]
        
        results = analyzer.compare_implementations(RecursiveBST, IterativeBST, data_sizes)
        
        assert "insert" in results
        assert "search" in results
        assert "delete" in results
        assert "traversal" in results
        assert "range_search" in results
        
        for operation in results:
            for size in data_sizes:
                operation_result = results[operation][size]
                assert "recursive" in operation_result
                assert "iterative" in operation_result
                assert "ratio" in operation_result
                assert operation_result["recursive"] > 0
                assert operation_result["iterative"] > 0
                assert operation_result["ratio"] > 0
    
    def test_get_operation_stmt(self):
        """Test getting operation statements."""
        analyzer = BSTAnalyzer()
        
        assert analyzer._get_operation_stmt("insert", 100) == "[bst.insert(i) for i in range(100)]"
        assert analyzer._get_operation_stmt("search", 100) == "[bst.search(i) for i in range(100)]"
        assert analyzer._get_operation_stmt("delete", 100) == "[bst.delete(i) for i in range(100)]"
        assert analyzer._get_operation_stmt("traversal", 100) == "list(bst.inorder_traversal())"
        assert analyzer._get_operation_stmt("range_search", 100) == "bst.range_search(25, 75)"
        assert analyzer._get_operation_stmt("unknown", 100) == ""
    
    def test_analyze_tree_structure(self):
        """Test tree structure analysis."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        structure = analyzer.analyze_tree_structure(None)
        assert structure["type"] == "empty"
        assert structure["height"] == 0
        assert structure["size"] == 0
        
        # Single node
        root = BSTNode(50)
        structure = analyzer.analyze_tree_structure(root)
        assert structure["type"] == "binary_search_tree"
        assert structure["height"] == 0
        assert structure["size"] == 1
        assert structure["structure"] == "single_node"
        assert structure["is_balanced"] is True
        
        # Balanced tree
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        structure = analyzer.analyze_tree_structure(root)
        assert structure["type"] == "binary_search_tree"
        assert structure["height"] == 1
        assert structure["size"] == 3
        assert structure["structure"] == "balanced"
        assert structure["is_balanced"] is True
        
        # Linear tree
        linear_root = BSTNode(50)
        linear_root.right = BSTNode(60)
        linear_root.right.right = BSTNode(70)
        linear_root.right.right.right = BSTNode(80)
        structure = analyzer.analyze_tree_structure(linear_root)
        assert structure["type"] == "binary_search_tree"
        assert structure["height"] == 3
        assert structure["size"] == 4
        assert structure["structure"] == "linear"
        assert structure["is_balanced"] is False
    
    def test_get_tree_visualization(self):
        """Test tree visualization."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        viz = analyzer.get_tree_visualization(None)
        assert viz == "Empty tree"
        
        # Single node
        root = BSTNode(50)
        viz = analyzer.get_tree_visualization(root)
        assert "50" in viz
        
        # Simple tree
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        viz = analyzer.get_tree_visualization(root, max_depth=2)
        assert "50" in viz
        assert "30" in viz
        assert "70" in viz
    
    def test_memory_efficiency_analysis(self):
        """Test memory efficiency analysis."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        analysis = analyzer.memory_efficiency_analysis(None)
        assert analysis["total_memory"] == 0
        assert analysis["node_memory"] == 0
        assert analysis["value_memory"] == 0
        assert analysis["overhead_memory"] == 0
        assert analysis["memory_per_node"] == 0
        assert analysis["efficiency_score"] == 0.0
        
        # Single node
        root = BSTNode(42)
        analysis = analyzer.memory_efficiency_analysis(root)
        assert analysis["total_memory"] > 0
        assert analysis["node_memory"] > 0
        assert analysis["value_memory"] > 0
        assert analysis["memory_per_node"] > 0
        assert 0.0 <= analysis["efficiency_score"] <= 1.0
        
        # Multiple nodes
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        analysis_multi = analyzer.memory_efficiency_analysis(root)
        assert analysis_multi["total_memory"] > analysis["total_memory"]
        assert analysis_multi["memory_per_node"] > 0
    
    def test_calculate_value_memory(self):
        """Test value memory calculation."""
        analyzer = BSTAnalyzer()
        
        # Empty tree
        assert analyzer._calculate_value_memory(None) == 0
        
        # Single node
        root = BSTNode(42)
        value_memory = analyzer._calculate_value_memory(root)
        assert value_memory > 0
        
        # Multiple nodes
        root.left = BSTNode(30)
        root.right = BSTNode(70)
        value_memory_multi = analyzer._calculate_value_memory(root)
        assert value_memory_multi > value_memory
    
    def test_complex_tree_analysis(self):
        """Test analysis of complex tree structure."""
        analyzer = BSTAnalyzer()
        
        # Create a complex tree
        #       50
        #      /  \
        #     30   70
        #    /  \ /  \
        #   20  40 60  80
        #  /  \
        # 10   25
        
        leaf_10 = BSTNode(10)
        leaf_25 = BSTNode(25)
        leaf_40 = BSTNode(40)
        leaf_60 = BSTNode(60)
        leaf_80 = BSTNode(80)
        
        node_20 = BSTNode(20, left=leaf_10, right=leaf_25)
        node_30 = BSTNode(30, left=node_20, right=leaf_40)
        node_70 = BSTNode(70, left=leaf_60, right=leaf_80)
        root = BSTNode(50, left=node_30, right=node_70)
        
        # Analyze the tree
        tree_info = analyzer.analyze_tree(root)
        structure_info = analyzer.analyze_tree_structure(root)
        memory_info = analyzer.memory_efficiency_analysis(root)
        
        # Verify tree info
        assert tree_info.height == 3
        assert tree_info.size == 9  # 9 nodes: 50, 30, 70, 20, 40, 60, 80, 10, 25
        assert tree_info.is_balanced is True  # Actually balanced
        assert tree_info.leaf_count == 5
        assert tree_info.internal_node_count == 4  # 9 - 5 = 4
        assert tree_info.min_value == 10
        assert tree_info.max_value == 80
        
        # Verify structure info
        assert structure_info["type"] == "binary_search_tree"
        assert structure_info["height"] == 3
        assert structure_info["size"] == 9
        assert structure_info["is_balanced"] is True
        assert structure_info["balance_factor"] == -1  # Left subtree is deeper
        
        # Verify memory info
        assert memory_info["total_memory"] > 0
        assert memory_info["node_memory"] > 0
        assert memory_info["value_memory"] > 0
        assert memory_info["memory_per_node"] > 0
        assert 0.0 <= memory_info["efficiency_score"] <= 1.0
    
    def test_edge_cases_analysis(self):
        """Test analysis edge cases."""
        analyzer = BSTAnalyzer()
        
        # Tree with zero value
        root_zero = BSTNode(0)
        tree_info = analyzer.analyze_tree(root_zero)
        assert tree_info.min_value == 0
        assert tree_info.max_value == 0
        
        # Tree with negative values
        root_neg = BSTNode(-10)
        root_neg.left = BSTNode(-20)
        root_neg.right = BSTNode(-5)
        tree_info = analyzer.analyze_tree(root_neg)
        assert tree_info.min_value == -20
        assert tree_info.max_value == -5
        
        # Tree with float values
        root_float = BSTNode(2.71)
        root_float.left = BSTNode(1.41)  # Less than parent
        root_float.right = BSTNode(3.14)  # Greater than parent
        tree_info = analyzer.analyze_tree(root_float)
        assert tree_info.min_value == 1.41
        assert tree_info.max_value == 3.14
        
        # Tree with string values
        root_string = BSTNode("banana")
        root_string.left = BSTNode("apple")  # Less than parent
        root_string.right = BSTNode("zebra")  # Greater than parent
        tree_info = analyzer.analyze_tree(root_string)
        assert tree_info.min_value == "apple"
        assert tree_info.max_value == "zebra" 