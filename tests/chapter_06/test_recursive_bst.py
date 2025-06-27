"""
Tests for RecursiveBST class.

This module provides comprehensive tests for the RecursiveBST class with 100% code coverage.
"""

import pytest
from typing import List, Optional

from mastering_performant_code.chapter_06.recursive_bst import RecursiveBST
from mastering_performant_code.chapter_06.bst_node import BSTNode


class TestRecursiveBST:
    """Test cases for RecursiveBST class."""
    
    def test_empty_bst(self):
        """Test empty BST initialization."""
        bst = RecursiveBST()
        assert len(bst) == 0
        assert bst.is_empty() is True
        assert bst._root is None
    
    def test_insert_single_element(self):
        """Test inserting a single element."""
        bst = RecursiveBST()
        bst.insert(42)
        
        assert len(bst) == 1
        assert bst.is_empty() is False
        assert bst._root is not None
        assert bst._root.value == 42
        assert bst._root.left is None
        assert bst._root.right is None
    
    def test_insert_multiple_elements(self):
        """Test inserting multiple elements."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        assert len(bst) == len(values)
        assert bst._root.value == 50
        assert bst._root.left.value == 30
        assert bst._root.right.value == 70
    
    def test_insert_duplicate_values(self):
        """Test inserting duplicate values."""
        bst = RecursiveBST()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        bst.insert(30)  # Duplicate
        bst.insert(70)  # Duplicate
        
        # Duplicates should be inserted to the right
        assert len(bst) == 5
        assert bst._root.left.value == 30
        assert bst._root.left.right.value == 30
        assert bst._root.right.value == 70
        assert bst._root.right.right.value == 70
    
    def test_search_existing_element(self):
        """Test searching for existing elements."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        for value in values:
            node = bst.search(value)
            assert node is not None
            assert node.value == value
    
    def test_search_nonexistent_element(self):
        """Test searching for non-existent elements."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        nonexistent_values = [10, 25, 35, 45, 55, 65, 75, 85, 100]
        for value in nonexistent_values:
            node = bst.search(value)
            assert node is None
    
    def test_search_empty_tree(self):
        """Test searching in empty tree."""
        bst = RecursiveBST()
        node = bst.search(42)
        assert node is None
    
    def test_contains(self):
        """Test contains method."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        for value in values:
            assert bst.contains(value) is True
        
        assert bst.contains(10) is False
        assert bst.contains(100) is False
    
    def test_delete_leaf_node(self):
        """Test deleting a leaf node."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        initial_size = len(bst)
        assert bst.delete(20) is True
        assert len(bst) == initial_size - 1
        assert bst.search(20) is None
        
        # Verify tree structure is maintained
        assert bst._root.left.left is None
    
    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        # Delete 20 (leaf), then 30 (has one child: 40)
        bst.delete(20)
        initial_size = len(bst)
        assert bst.delete(30) is True
        assert len(bst) == initial_size - 1
        assert bst.search(30) is None
        
        # Verify 40 is now the left child of root
        assert bst._root.left.value == 40
    
    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        initial_size = len(bst)
        assert bst.delete(30) is True
        assert len(bst) == initial_size - 1
        assert bst.search(30) is None
        
        # Verify successor (35) replaced 30
        assert bst._root.left.value == 35
    
    def test_delete_root_node(self):
        """Test deleting the root node."""
        bst = RecursiveBST()
        bst.insert(50)
        
        assert bst.delete(50) is True
        assert len(bst) == 0
        assert bst.is_empty() is True
        assert bst._root is None
    
    def test_delete_nonexistent_element(self):
        """Test deleting non-existent elements."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        initial_size = len(bst)
        assert bst.delete(100) is False
        assert len(bst) == initial_size
    
    def test_find_minimum(self):
        """Test finding minimum value."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        assert bst.find_minimum() == 10
    
    def test_find_minimum_empty_tree(self):
        """Test finding minimum in empty tree."""
        bst = RecursiveBST()
        assert bst.find_minimum() is None
    
    def test_find_maximum(self):
        """Test finding maximum value."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        assert bst.find_maximum() == 85
    
    def test_find_maximum_empty_tree(self):
        """Test finding maximum in empty tree."""
        bst = RecursiveBST()
        assert bst.find_maximum() is None
    
    def test_get_successor(self):
        """Test getting successor of a value."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        assert bst.get_successor(30) == 35
        assert bst.get_successor(50) == 55
        assert bst.get_successor(85) is None  # No successor for maximum
    
    def test_get_successor_nonexistent_value(self):
        """Test getting successor of non-existent value."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        assert bst.get_successor(100) is None
    
    def test_get_predecessor(self):
        """Test getting predecessor of a value."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        assert bst.get_predecessor(30) == 25
        assert bst.get_predecessor(50) == 45
        assert bst.get_predecessor(10) is None  # No predecessor for minimum
    
    def test_get_predecessor_nonexistent_value(self):
        """Test getting predecessor of non-existent value."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        assert bst.get_predecessor(100) is None
    
    def test_inorder_traversal(self):
        """Test inorder traversal."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        expected = sorted(values)
        result = list(bst.inorder_traversal())
        assert result == expected
    
    def test_inorder_traversal_empty_tree(self):
        """Test inorder traversal of empty tree."""
        bst = RecursiveBST()
        result = list(bst.inorder_traversal())
        assert result == []
    
    def test_preorder_traversal(self):
        """Test preorder traversal."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        # Expected preorder: 50, 30, 20, 40, 70, 60, 80
        expected = [50, 30, 20, 40, 70, 60, 80]
        result = list(bst.preorder_traversal())
        assert result == expected
    
    def test_postorder_traversal(self):
        """Test postorder traversal."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        # Expected postorder: 20, 40, 30, 60, 80, 70, 50
        expected = [20, 40, 30, 60, 80, 70, 50]
        result = list(bst.postorder_traversal())
        assert result == expected
    
    def test_level_order_traversal(self):
        """Test level-order traversal."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        # Expected level-order: 50, 30, 70, 20, 40, 60, 80
        expected = [50, 30, 70, 20, 40, 60, 80]
        result = list(bst.level_order_traversal())
        assert result == expected
    
    def test_level_order_traversal_empty_tree(self):
        """Test level-order traversal of empty tree."""
        bst = RecursiveBST()
        result = list(bst.level_order_traversal())
        assert result == []
    
    def test_get_sorted_list(self):
        """Test getting sorted list."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        expected = sorted(values)
        result = bst.get_sorted_list()
        assert result == expected
    
    def test_range_search(self):
        """Test range search functionality."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            bst.insert(value)
        
        # Test various ranges
        assert bst.range_search(25, 65) == [25, 30, 35, 40, 45, 50, 55, 60, 65]
        assert bst.range_search(10, 20) == [10, 20]
        assert bst.range_search(80, 85) == [80, 85]
        assert bst.range_search(0, 100) == sorted(values)
        assert bst.range_search(100, 200) == []
    
    def test_range_search_empty_tree(self):
        """Test range search on empty tree."""
        bst = RecursiveBST()
        result = bst.range_search(10, 50)
        assert result == []
    
    def test_get_height(self):
        """Test getting tree height."""
        bst = RecursiveBST()
        
        # Empty tree
        assert bst.get_height() == -1
        
        # Single node
        bst.insert(50)
        assert bst.get_height() == 0
        
        # Two levels
        bst.insert(30)
        bst.insert(70)
        assert bst.get_height() == 1
        
        # Three levels
        bst.insert(20)
        bst.insert(40)
        bst.insert(60)
        bst.insert(80)
        assert bst.get_height() == 2
    
    def test_is_balanced(self):
        """Test checking if tree is balanced."""
        bst = RecursiveBST()
        
        # Empty tree is balanced
        assert bst.is_balanced() is True
        
        # Single node is balanced
        bst.insert(50)
        assert bst.is_balanced() is True
        
        # Balanced tree
        values = [30, 70, 20, 40, 60, 80]  # Don't include 50 again
        for value in values:
            bst.insert(value)
        assert bst.is_balanced() is True
        
        # Unbalanced tree (linear)
        unbalanced_bst = RecursiveBST()
        for value in [50, 40, 30, 20, 10]:
            unbalanced_bst.insert(value)
        assert unbalanced_bst.is_balanced() is False
    
    def test_clear(self):
        """Test clearing the tree."""
        bst = RecursiveBST()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            bst.insert(value)
        
        assert len(bst) == len(values)
        assert bst.is_empty() is False
        
        bst.clear()
        assert len(bst) == 0
        assert bst.is_empty() is True
        assert bst._root is None
    
    def test_repr(self):
        """Test string representation."""
        bst = RecursiveBST()
        assert repr(bst) == "RecursiveBST()"
        
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        assert repr(bst) == "RecursiveBST([30, 50, 70])"
    
    def test_complex_operations(self):
        """Test complex sequence of operations."""
        bst = RecursiveBST()
        
        # Insert elements
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        for value in values:
            bst.insert(value)
        
        assert len(bst) == len(values)
        assert bst.find_minimum() == 10
        assert bst.find_maximum() == 85
        
        # Delete some elements
        delete_values = [20, 30, 50, 80]
        for value in delete_values:
            assert bst.delete(value) is True
        
        assert len(bst) == len(values) - len(delete_values)
        
        # Verify remaining elements
        remaining = [v for v in values if v not in delete_values]
        assert bst.get_sorted_list() == sorted(remaining)
        
        # Test range search on modified tree
        assert bst.range_search(25, 65) == [25, 35, 40, 45, 55, 60, 65]
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        bst = RecursiveBST()
        
        # Insert zero
        bst.insert(0)
        assert bst.find_minimum() == 0
        assert bst.find_maximum() == 0
        
        # Insert negative values
        bst.insert(-10)
        bst.insert(-5)
        assert bst.find_minimum() == -10
        assert bst.find_maximum() == 0
        
        # Insert large values
        bst.insert(1000)
        bst.insert(999999)
        assert bst.find_minimum() == -10
        assert bst.find_maximum() == 999999
        
        # Test with float values
        float_bst = RecursiveBST()
        float_values = [3.14, 2.71, 1.41, 2.23]
        for value in float_values:
            float_bst.insert(value)
        
        assert float_bst.find_minimum() == 1.41
        assert float_bst.find_maximum() == 3.14
        
        # Test with string values
        string_bst = RecursiveBST()
        string_values = ["apple", "banana", "cherry", "date"]
        for value in string_values:
            string_bst.insert(value)
        
        assert string_bst.find_minimum() == "apple"
        assert string_bst.find_maximum() == "date"
    
    def test_deletion_edge_cases(self):
        """Test edge cases for deletion."""
        bst = RecursiveBST()
        
        # Delete from empty tree
        assert bst.delete(42) is False
        
        # Delete root with one child
        bst.insert(50)
        bst.insert(30)
        assert bst.delete(50) is True
        assert bst._root.value == 30
        assert len(bst) == 1
        
        # Delete root with two children
        bst.clear()
        bst.insert(50)
        bst.insert(30)
        bst.insert(70)
        assert bst.delete(50) is True
        assert bst._root.value == 70
        assert len(bst) == 2
        
        # Delete node with successor that has right child
        bst.clear()
        values = [50, 30, 70, 20, 40, 60, 80, 35, 45]
        for value in values:
            bst.insert(value)
        
        assert bst.delete(30) is True
        assert bst._root.left.value == 35
        assert bst._root.left.right.value == 40 