"""
Unit tests for AVL Tree implementation.

This module provides comprehensive tests for the AVLTree class,
ensuring all operations work correctly and the tree maintains balance.
"""

import pytest
import os

from chapter_07.avl_tree import AVLTree

class TestAVLTree:
    """Test cases for AVLTree class."""
    
    def test_empty_tree(self):
        """Test empty tree properties."""
        tree = AVLTree()
        assert len(tree) == 0
        assert tree.is_empty() is True
        assert tree.height() == 0
        assert tree.is_balanced() is True
    
    def test_single_insertion(self):
        """Test inserting a single value."""
        tree = AVLTree()
        tree.insert(42)
        
        assert len(tree) == 1
        assert tree.is_empty() is False
        assert tree.height() == 1
        assert tree.is_balanced() is True
        
        # Check that the value is in the tree
        result = tree.search(42)
        assert result is not None
        assert result.value == 42
    
    def test_multiple_insertions(self):
        """Test inserting multiple values."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        assert len(tree) == 7
        assert tree.is_balanced() is True
        
        # Check all values are in the tree
        for value in values:
            result = tree.search(value)
            assert result is not None
            assert result.value == value
    
    def test_left_left_rotation(self):
        """Test left-left rotation scenario."""
        tree = AVLTree()
        # Insert in order that triggers LL rotation: 30, 20, 10
        tree.insert(30)
        tree.insert(20)
        tree.insert(10)
        
        assert tree.is_balanced() is True
        assert tree.height() <= 2  # Should be balanced after rotation
        
        # Check that all values are still in the tree
        assert tree.search(10) is not None
        assert tree.search(20) is not None
        assert tree.search(30) is not None
    
    def test_right_right_rotation(self):
        """Test right-right rotation scenario."""
        tree = AVLTree()
        # Insert in order that triggers RR rotation: 10, 20, 30
        tree.insert(10)
        tree.insert(20)
        tree.insert(30)
        
        assert tree.is_balanced() is True
        assert tree.height() <= 2  # Should be balanced after rotation
        
        # Check that all values are still in the tree
        assert tree.search(10) is not None
        assert tree.search(20) is not None
        assert tree.search(30) is not None
    
    def test_left_right_rotation(self):
        """Test left-right rotation scenario."""
        tree = AVLTree()
        # Insert in order that triggers LR rotation: 30, 10, 20
        tree.insert(30)
        tree.insert(10)
        tree.insert(20)
        
        assert tree.is_balanced() is True
        assert tree.height() <= 2  # Should be balanced after rotation
        
        # Check that all values are still in the tree
        assert tree.search(10) is not None
        assert tree.search(20) is not None
        assert tree.search(30) is not None
    
    def test_right_left_rotation(self):
        """Test right-left rotation scenario."""
        tree = AVLTree()
        # Insert in order that triggers RL rotation: 10, 30, 20
        tree.insert(10)
        tree.insert(30)
        tree.insert(20)
        
        assert tree.is_balanced() is True
        assert tree.height() <= 2  # Should be balanced after rotation
        
        # Check that all values are still in the tree
        assert tree.search(10) is not None
        assert tree.search(20) is not None
        assert tree.search(30) is not None
    
    def test_search_existing_values(self):
        """Test searching for existing values."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        for value in values:
            result = tree.search(value)
            assert result is not None
            assert result.value == value
    
    def test_search_non_existing_values(self):
        """Test searching for non-existing values."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        non_existing = [15, 25, 35, 45, 55, 65, 75, 85]
        for value in non_existing:
            result = tree.search(value)
            assert result is None
    
    def test_search_empty_tree(self):
        """Test searching in empty tree."""
        tree = AVLTree()
        result = tree.search(42)
        assert result is None
    
    def test_traversal_methods(self):
        """Test all traversal methods."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        # Test inorder traversal (should be sorted)
        inorder = list(tree.inorder_traversal())
        assert inorder == sorted(values)
        
        # Test preorder traversal
        preorder = list(tree.preorder_traversal())
        assert len(preorder) == len(values)
        assert set(preorder) == set(values)
        
        # Test postorder traversal
        postorder = list(tree.postorder_traversal())
        assert len(postorder) == len(values)
        assert set(postorder) == set(values)
        
        # Test level order traversal
        level_order = list(tree.level_order_traversal())
        assert len(level_order) > 0
        all_level_values = []
        for level in level_order:
            all_level_values.extend(level)
        assert set(all_level_values) == set(values)
    
    def test_get_sorted_values(self):
        """Test getting sorted values."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        sorted_values = tree.get_sorted_values()
        assert sorted_values == sorted(values)
    
    def test_successor_and_predecessor(self):
        """Test successor and predecessor operations."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        # Test successor
        assert tree.successor(20) == 30
        assert tree.successor(30) == 40
        assert tree.successor(40) == 50
        assert tree.successor(50) == 60
        assert tree.successor(60) == 70
        assert tree.successor(70) == 80
        assert tree.successor(80) is None  # No successor for max value
        
        # Test predecessor
        assert tree.predecessor(20) is None  # No predecessor for min value
        assert tree.predecessor(30) == 20
        assert tree.predecessor(40) == 30
        assert tree.predecessor(50) == 40
        assert tree.predecessor(60) == 50
        assert tree.predecessor(70) == 60
        assert tree.predecessor(80) == 70
    
    def test_successor_predecessor_non_existing(self):
        """Test successor and predecessor for non-existing values."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        # Test with non-existing values
        assert tree.successor(25) is None
        assert tree.predecessor(25) is None
        assert tree.successor(90) is None
        assert tree.predecessor(15) is None
    
    def test_delete_leaf_node(self):
        """Test deleting a leaf node."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        initial_size = len(tree)
        
        # Delete a leaf node
        result = tree.delete(20)
        assert result is True
        assert len(tree) == initial_size - 1
        assert tree.search(20) is None
        assert tree.is_balanced() is True
        
        # Verify other values are still there
        remaining_values = [30, 40, 50, 60, 70, 80]
        for value in remaining_values:
            assert tree.search(value) is not None
    
    def test_delete_node_with_one_child(self):
        """Test deleting a node with one child."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        initial_size = len(tree)
        
        # Delete a node with one child (after deleting 20, 30 will have only right child)
        tree.delete(20)
        result = tree.delete(30)
        assert result is True
        assert len(tree) == initial_size - 2
        assert tree.search(30) is None
        assert tree.is_balanced() is True
    
    def test_delete_node_with_two_children(self):
        """Test deleting a node with two children."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        initial_size = len(tree)
        
        # Delete root node (has two children)
        result = tree.delete(50)
        assert result is True
        assert len(tree) == initial_size - 1
        assert tree.search(50) is None
        assert tree.is_balanced() is True
        
        # The successor (60) should replace the deleted node
        assert tree.search(60) is not None
    
    def test_delete_non_existing_value(self):
        """Test deleting a non-existing value."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        initial_size = len(tree)
        
        # Try to delete non-existing value
        result = tree.delete(25)
        assert result is False
        assert len(tree) == initial_size  # Size should not change
    
    def test_delete_from_empty_tree(self):
        """Test deleting from empty tree."""
        tree = AVLTree()
        result = tree.delete(42)
        assert result is False
    
    def test_delete_all_values(self):
        """Test deleting all values from the tree."""
        tree = AVLTree()
        values = [50, 30, 70, 20, 40, 60, 80]
        
        for value in values:
            tree.insert(value)
        
        # Delete all values
        for value in values:
            result = tree.delete(value)
            assert result is True
        
        assert len(tree) == 0
        assert tree.is_empty() is True
        assert tree.height() == 0
    
    def test_complex_balance_scenarios(self):
        """Test complex balancing scenarios."""
        tree = AVLTree()
        
        # Insert values that will trigger multiple rotations
        values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
        
        for value in values:
            tree.insert(value)
            # Tree should remain balanced after each insertion
            assert tree.is_balanced() is True
        
        assert len(tree) == len(values)
        
        # Delete values and ensure tree remains balanced
        delete_values = [30, 50, 70]
        for value in delete_values:
            tree.delete(value)
            assert tree.is_balanced() is True
    
    def test_tree_repr(self):
        """Test tree string representation."""
        tree = AVLTree()
        values = [50, 30, 70]
        
        for value in values:
            tree.insert(value)
        
        repr_str = repr(tree)
        assert "AVLTree" in repr_str
        assert "50" in repr_str
        assert "30" in repr_str
        assert "70" in repr_str
    
    def test_large_tree_performance(self):
        """Test performance with larger tree."""
        tree = AVLTree()
        values = list(range(1000))
        
        # Insert 1000 values
        for value in values:
            tree.insert(value)
        
        assert len(tree) == 1000
        assert tree.is_balanced() is True
        
        # Verify height is logarithmic
        assert tree.height() <= 20  # log2(1000) ≈ 10, but AVL allows slightly more
        
        # Test search performance
        for i in range(0, 1000, 100):
            result = tree.search(i)
            assert result is not None
            assert result.value == i
    
    def test_duplicate_values(self):
        """Test handling of duplicate values."""
        tree = AVLTree()
        values = [50, 30, 70, 30, 50, 70]  # Duplicates
        
        for value in values:
            tree.insert(value)
        
        # Tree should handle duplicates (insert to right subtree)
        assert len(tree) == 6
        assert tree.is_balanced() is True
        
        # All values should be searchable
        for value in set(values):
            result = tree.search(value)
            assert result is not None
    
    def test_different_data_types(self):
        """Test tree with different data types."""
        tree = AVLTree()
        
        # Test with strings
        string_values = ["apple", "banana", "cherry", "date"]
        for value in string_values:
            tree.insert(value)
        
        assert len(tree) == 4
        assert tree.is_balanced() is True
        
        for value in string_values:
            result = tree.search(value)
            assert result is not None
            assert result.value == value
        
        # Test with floats
        tree_float = AVLTree()
        float_values = [3.14, 2.71, 1.41, 2.23]
        for value in float_values:
            tree_float.insert(value)
        
        assert len(tree_float) == 4
        assert tree_float.is_balanced() is True
    
    def test_edge_cases(self):
        """Test various edge cases."""
        tree = AVLTree()
        
        # Test with negative numbers
        negative_values = [-50, -30, -70, -20, -40]
        for value in negative_values:
            tree.insert(value)
        
        assert len(tree) == 5
        assert tree.is_balanced() is True
        
        # Test with zero
        tree.insert(0)
        assert tree.search(0) is not None
        
        # Test with very large numbers
        tree.insert(1000000)
        assert tree.search(1000000) is not None 