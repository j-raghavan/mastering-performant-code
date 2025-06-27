"""
Unit tests for AVL Node implementation.

This module provides comprehensive tests for the AVLNode class,
ensuring all methods work correctly and edge cases are handled.
"""

import pytest

from mastering_performant_code.chapter_07.avl_node import AVLNode

class TestAVLNode:
    """Test cases for AVLNode class."""
    
    def test_node_creation(self):
        """Test basic node creation."""
        node = AVLNode(42)
        assert node.value == 42
        assert node.left is None
        assert node.right is None
        assert node.parent is None
        assert node.height == 1
    
    def test_node_with_children(self):
        """Test node creation with children."""
        left_child = AVLNode(20)
        right_child = AVLNode(60)
        node = AVLNode(40, left=left_child, right=right_child)
        
        assert node.value == 40
        assert node.left == left_child
        assert node.right == right_child
        assert node.height == 1
        assert left_child.parent == node
        assert right_child.parent == node
    
    def test_is_leaf(self):
        """Test is_leaf method."""
        # Leaf node
        leaf_node = AVLNode(42)
        assert leaf_node.is_leaf() is True
        
        # Node with left child
        left_child = AVLNode(20)
        node_with_left = AVLNode(40, left=left_child)
        assert node_with_left.is_leaf() is False
        
        # Node with right child
        right_child = AVLNode(60)
        node_with_right = AVLNode(40, right=right_child)
        assert node_with_right.is_leaf() is False
        
        # Node with both children
        node_with_both = AVLNode(40, left=left_child, right=right_child)
        assert node_with_both.is_leaf() is False
    
    def test_has_one_child(self):
        """Test has_one_child method."""
        # Leaf node
        leaf_node = AVLNode(42)
        assert leaf_node.has_one_child() is False
        
        # Node with left child only
        left_child = AVLNode(20)
        node_with_left = AVLNode(40, left=left_child)
        assert node_with_left.has_one_child() is True
        
        # Node with right child only
        right_child = AVLNode(60)
        node_with_right = AVLNode(40, right=right_child)
        assert node_with_right.has_one_child() is True
        
        # Node with both children
        node_with_both = AVLNode(40, left=left_child, right=right_child)
        assert node_with_both.has_one_child() is False
    
    def test_get_only_child(self):
        """Test get_only_child method."""
        # Leaf node
        leaf_node = AVLNode(42)
        assert leaf_node.get_only_child() is None
        
        # Node with left child only
        left_child = AVLNode(20)
        node_with_left = AVLNode(40, left=left_child)
        assert node_with_left.get_only_child() == left_child
        
        # Node with right child only
        right_child = AVLNode(60)
        node_with_right = AVLNode(40, right=right_child)
        assert node_with_right.get_only_child() == right_child
        
        # Node with both children
        node_with_both = AVLNode(40, left=left_child, right=right_child)
        assert node_with_both.get_only_child() is None
    
    def test_get_balance_factor(self):
        """Test get_balance_factor method."""
        # Leaf node
        leaf_node = AVLNode(42)
        assert leaf_node.get_balance_factor() == 0
        
        # Node with left child only
        left_child = AVLNode(20)
        left_child.height = 2
        node_with_left = AVLNode(40, left=left_child)
        assert node_with_left.get_balance_factor() == -2
        
        # Node with right child only
        right_child = AVLNode(60)
        right_child.height = 3
        node_with_right = AVLNode(40, right=right_child)
        assert node_with_right.get_balance_factor() == 3
        
        # Node with both children
        left_child.height = 2
        right_child.height = 1
        node_with_both = AVLNode(40, left=left_child, right=right_child)
        assert node_with_both.get_balance_factor() == -1
    
    def test_update_height(self):
        """Test update_height method."""
        # Leaf node
        leaf_node = AVLNode(42)
        leaf_node.update_height()
        assert leaf_node.height == 1
        
        # Node with left child
        left_child = AVLNode(20)
        left_child.height = 2
        node_with_left = AVLNode(40, left=left_child)
        node_with_left.update_height()
        assert node_with_left.height == 3
        
        # Node with right child
        right_child = AVLNode(60)
        right_child.height = 3
        node_with_right = AVLNode(40, right=right_child)
        node_with_right.update_height()
        assert node_with_right.height == 4
        
        # Node with both children (left taller)
        left_child.height = 4
        right_child.height = 2
        node_with_both = AVLNode(40, left=left_child, right=right_child)
        node_with_both.update_height()
        assert node_with_both.height == 5
        
        # Node with both children (right taller)
        left_child.height = 2
        right_child.height = 4
        node_with_both.update_height()
        assert node_with_both.height == 5
    
    def test_post_init_parent_assignment(self):
        """Test that __post_init__ correctly assigns parent references."""
        # Create children first
        left_child = AVLNode(20)
        right_child = AVLNode(60)
        
        # Create parent with children
        parent = AVLNode(40, left=left_child, right=right_child)
        
        # Check that parent references are set
        assert left_child.parent == parent
        assert right_child.parent == parent
    
    def test_node_with_different_data_types(self):
        """Test node creation with different data types."""
        # String value
        string_node = AVLNode("test")
        assert string_node.value == "test"
        
        # Float value
        float_node = AVLNode(3.14)
        assert float_node.value == 3.14
        
        # Complex object
        class TestObject:
            def __init__(self, value):
                self.value = value
        
        obj = TestObject(42)
        obj_node = AVLNode(obj)
        assert obj_node.value == obj
        assert obj_node.value.value == 42
    
    def test_node_equality_and_comparison(self):
        """Test node comparison behavior."""
        node1 = AVLNode(10)
        node2 = AVLNode(20)
        node3 = AVLNode(10)
        
        # Test comparison based on values
        assert node1.value < node2.value
        assert node2.value > node1.value
        assert node1.value == node3.value
        
        # Test that nodes with same value but different children are equal in value comparison
        left_child = AVLNode(5)
        node1_with_child = AVLNode(10, left=left_child)
        assert node1.value == node1_with_child.value
    
    def test_node_repr_and_str(self):
        """Test node string representation."""
        node = AVLNode(42)
        # Test that node can be converted to string (basic functionality)
        str_repr = str(node)
        assert "42" in str_repr or "AVLNode" in str_repr
    
    def test_complex_tree_structure(self):
        """Test complex tree structure with multiple levels."""
        # Create a small tree: root(50) -> left(30) -> left(20), right(40)
        #                                    -> right(70) -> left(60), right(80)
        
        # Create leaf nodes
        node_20 = AVLNode(20)
        node_40 = AVLNode(40)
        node_60 = AVLNode(60)
        node_80 = AVLNode(80)
        
        # Create intermediate nodes
        node_30 = AVLNode(30, left=node_20, right=node_40)
        node_70 = AVLNode(70, left=node_60, right=node_80)
        
        # Create root node
        root = AVLNode(50, left=node_30, right=node_70)
        
        # Test structure
        assert root.value == 50
        assert root.left == node_30
        assert root.right == node_70
        assert node_30.parent == root
        assert node_70.parent == root
        assert node_20.parent == node_30
        assert node_40.parent == node_30
        assert node_60.parent == node_70
        assert node_80.parent == node_70
        
        # Test leaf detection
        assert node_20.is_leaf() is True
        assert node_40.is_leaf() is True
        assert node_60.is_leaf() is True
        assert node_80.is_leaf() is True
        assert node_30.is_leaf() is False
        assert node_70.is_leaf() is False
        assert root.is_leaf() is False
        
        # Test height calculation - update from bottom up
        node_20.update_height()
        node_40.update_height()
        node_60.update_height()
        node_80.update_height()
        node_30.update_height()
        node_70.update_height()
        root.update_height()
        
        assert node_20.height == 1
        assert node_40.height == 1
        assert node_60.height == 1
        assert node_80.height == 1
        assert node_30.height == 2
        assert node_70.height == 2
        # The root height should be 3 (max of children heights + 1)
        assert root.height == 3
        
        # Test balance factors
        assert node_20.get_balance_factor() == 0
        assert node_40.get_balance_factor() == 0
        assert node_30.get_balance_factor() == 0
        assert node_70.get_balance_factor() == 0
        assert root.get_balance_factor() == 0 