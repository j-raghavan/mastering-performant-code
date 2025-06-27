"""
Tests for BSTNode class.

This module provides comprehensive tests for the BSTNode class with 100% code coverage.
"""

import pytest
from typing import Optional

from mastering_performant_code.chapter_06.bst_node import BSTNode


class TestBSTNode:
    """Test cases for BSTNode class."""
    
    def test_bst_node_creation(self):
        """Test basic BSTNode creation."""
        node = BSTNode(42)
        assert node.value == 42
        assert node.left is None
        assert node.right is None
        assert node.parent is None
    
    def test_bst_node_with_children(self):
        """Test BSTNode creation with children."""
        left_child = BSTNode(20)
        right_child = BSTNode(60)
        parent = BSTNode(40, left=left_child, right=right_child)
        
        assert parent.value == 40
        assert parent.left == left_child
        assert parent.right == right_child
        assert left_child.parent == parent
        assert right_child.parent == parent
    
    def test_bst_node_post_init(self):
        """Test that __post_init__ properly sets parent references."""
        parent = BSTNode(50)
        left_child = BSTNode(30)
        right_child = BSTNode(70)
        
        # Manually set children after creation
        parent.left = left_child
        parent.right = right_child
        
        # Call __post_init__ manually
        parent.__post_init__()
        
        assert left_child.parent == parent
        assert right_child.parent == parent
    
    def test_is_leaf(self):
        """Test is_leaf method."""
        # Leaf node
        leaf_node = BSTNode(42)
        assert leaf_node.is_leaf() is True
        
        # Node with left child
        node_with_left = BSTNode(50, left=BSTNode(30))
        assert node_with_left.is_leaf() is False
        
        # Node with right child
        node_with_right = BSTNode(50, right=BSTNode(70))
        assert node_with_right.is_leaf() is False
        
        # Node with both children
        node_with_both = BSTNode(50, left=BSTNode(30), right=BSTNode(70))
        assert node_with_both.is_leaf() is False
    
    def test_has_one_child(self):
        """Test has_one_child method."""
        # Node with no children
        no_children = BSTNode(42)
        assert no_children.has_one_child() is False
        
        # Node with left child only
        left_only = BSTNode(50, left=BSTNode(30))
        assert left_only.has_one_child() is True
        
        # Node with right child only
        right_only = BSTNode(50, right=BSTNode(70))
        assert right_only.has_one_child() is True
        
        # Node with both children
        both_children = BSTNode(50, left=BSTNode(30), right=BSTNode(70))
        assert both_children.has_one_child() is False
    
    def test_get_only_child(self):
        """Test get_only_child method."""
        # Node with no children
        no_children = BSTNode(42)
        assert no_children.get_only_child() is None
        
        # Node with left child only
        left_child = BSTNode(30)
        left_only = BSTNode(50, left=left_child)
        assert left_only.get_only_child() == left_child
        
        # Node with right child only
        right_child = BSTNode(70)
        right_only = BSTNode(50, right=right_child)
        assert right_only.get_only_child() == right_child
        
        # Node with both children
        both_children = BSTNode(50, left=BSTNode(30), right=BSTNode(70))
        assert both_children.get_only_child() is None
    
    def test_get_children_count(self):
        """Test get_children_count method."""
        # Node with no children
        no_children = BSTNode(42)
        assert no_children.get_children_count() == 0
        
        # Node with left child only
        left_only = BSTNode(50, left=BSTNode(30))
        assert left_only.get_children_count() == 1
        
        # Node with right child only
        right_only = BSTNode(50, right=BSTNode(70))
        assert right_only.get_children_count() == 1
        
        # Node with both children
        both_children = BSTNode(50, left=BSTNode(30), right=BSTNode(70))
        assert both_children.get_children_count() == 2
    
    def test_is_left_child(self):
        """Test is_left_child method."""
        parent = BSTNode(50)
        left_child = BSTNode(30, parent=parent)
        right_child = BSTNode(70, parent=parent)
        parent.left = left_child
        parent.right = right_child
        
        # Root node
        root_node = BSTNode(100)
        assert root_node.is_left_child() is False
        
        # Left child
        assert left_child.is_left_child() is True
        
        # Right child
        assert right_child.is_left_child() is False
    
    def test_is_right_child(self):
        """Test is_right_child method."""
        parent = BSTNode(50)
        left_child = BSTNode(30, parent=parent)
        right_child = BSTNode(70, parent=parent)
        parent.left = left_child
        parent.right = right_child
        
        # Root node
        root_node = BSTNode(100)
        assert root_node.is_right_child() is False
        
        # Left child
        assert left_child.is_right_child() is False
        
        # Right child
        assert right_child.is_right_child() is True
    
    def test_get_sibling(self):
        """Test get_sibling method."""
        parent = BSTNode(50)
        left_child = BSTNode(30, parent=parent)
        right_child = BSTNode(70, parent=parent)
        parent.left = left_child
        parent.right = right_child
        
        # Root node
        root_node = BSTNode(100)
        assert root_node.get_sibling() is None
        
        # Left child's sibling
        assert left_child.get_sibling() == right_child
        
        # Right child's sibling
        assert right_child.get_sibling() == left_child
    
    def test_get_sibling_no_sibling(self):
        """Test get_sibling when there is no sibling."""
        parent = BSTNode(50)
        only_child = BSTNode(30, parent=parent)
        parent.left = only_child
        
        assert only_child.get_sibling() is None
    
    def test_repr(self):
        """Test __repr__ method."""
        node = BSTNode(42)
        assert repr(node) == "BSTNode(value=42)"
        
        node_with_children = BSTNode(50, left=BSTNode(30), right=BSTNode(70))
        assert repr(node_with_children) == "BSTNode(value=50)"
    
    def test_memory_usage(self):
        """Test memory usage of BSTNode."""
        node = BSTNode(42)
        node_size = sys.getsizeof(node)
        
        # Node should use some memory
        assert node_size > 0
        
        # Node with children should use more memory
        node_with_children = BSTNode(50, left=BSTNode(30), right=BSTNode(70))
        node_with_children_size = sys.getsizeof(node_with_children)
        
        assert node_with_children_size >= node_size
    
    def test_complex_tree_structure(self):
        """Test complex tree structure with multiple levels."""
        # Create a complex tree structure
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
        
        # Test parent relationships
        assert leaf_10.parent == node_20
        assert leaf_25.parent == node_20
        assert node_20.parent == node_30
        assert leaf_40.parent == node_30
        assert node_30.parent == root
        assert leaf_60.parent == node_70
        assert leaf_80.parent == node_70
        assert node_70.parent == root
        
        # Test leaf detection
        assert leaf_10.is_leaf() is True
        assert leaf_25.is_leaf() is True
        assert leaf_40.is_leaf() is True
        assert leaf_60.is_leaf() is True
        assert leaf_80.is_leaf() is True
        assert node_20.is_leaf() is False
        assert node_30.is_leaf() is False
        assert node_70.is_leaf() is False
        assert root.is_leaf() is False
        
        # Test child counting
        assert leaf_10.get_children_count() == 0
        assert node_20.get_children_count() == 2
        assert node_30.get_children_count() == 2
        assert root.get_children_count() == 2
        
        # Test sibling relationships
        assert leaf_10.get_sibling() == leaf_25
        assert leaf_25.get_sibling() == leaf_10
        assert leaf_60.get_sibling() == leaf_80
        assert leaf_80.get_sibling() == leaf_60
        assert node_30.get_sibling() == node_70
        assert node_70.get_sibling() == node_30
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Node with zero value
        zero_node = BSTNode(0)
        assert zero_node.value == 0
        assert zero_node.is_leaf() is True
        
        # Node with negative value
        negative_node = BSTNode(-42)
        assert negative_node.value == -42
        assert negative_node.is_leaf() is True
        
        # Node with large value
        large_node = BSTNode(999999999)
        assert large_node.value == 999999999
        assert large_node.is_leaf() is True
        
        # Node with float value
        float_node = BSTNode(3.14)
        assert float_node.value == 3.14
        assert float_node.is_leaf() is True
        
        # Node with string value
        string_node = BSTNode("test")
        assert string_node.value == "test"
        assert string_node.is_leaf() is True
    
    def test_mutation_after_creation(self):
        """Test that nodes can be modified after creation."""
        node = BSTNode(50)
        
        # Initially no children
        assert node.is_leaf() is True
        assert node.get_children_count() == 0
        
        # Add left child
        left_child = BSTNode(30)
        node.left = left_child
        node.__post_init__()  # Update parent references
        
        assert node.is_leaf() is False
        assert node.get_children_count() == 1
        assert node.has_one_child() is True
        assert node.get_only_child() == left_child
        assert left_child.parent == node
        
        # Add right child
        right_child = BSTNode(70)
        node.right = right_child
        node.__post_init__()  # Update parent references
        
        assert node.is_leaf() is False
        assert node.get_children_count() == 2
        assert node.has_one_child() is False
        assert node.get_only_child() is None
        assert right_child.parent == node
        
        # Remove left child
        node.left = None
        assert node.get_children_count() == 1
        assert node.has_one_child() is True
        assert node.get_only_child() == right_child 