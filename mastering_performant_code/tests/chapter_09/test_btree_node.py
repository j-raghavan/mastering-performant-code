"""
Unit tests for BTreeNode class.

This module provides comprehensive tests for the BTreeNode class,
ensuring all methods work correctly and handle edge cases properly.
"""

import pytest
import sys
from typing import List, Optional

# Add the parent directory to the path to import the chapter modules
import sys
sys.path.append('.')

from src.chapter_09.btree_node import BTreeNode


class TestBTreeNode:
    """Test cases for BTreeNode class."""
    
    def test_create_leaf_node(self):
        """Test creating a leaf node."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        assert node.is_leaf is True
        assert node.children is None
        assert node.num_keys == 3
        assert node.keys == [1, 2, 3]
    
    def test_create_internal_node(self):
        """Test creating an internal node."""
        keys = [1, 2, 3]
        children = [None, None, None, None]  # 4 children for 3 keys
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        assert node.is_leaf is False
        assert node.children == children
        assert node.num_keys == 3
        assert node.keys == [1, 2, 3]
    
    def test_leaf_node_with_children_raises_error(self):
        """Test that leaf nodes cannot have children."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        
        with pytest.raises(ValueError, match="Leaf nodes cannot have children"):
            BTreeNode(keys=keys, children=children, is_leaf=True, num_keys=3)
    
    def test_internal_node_without_children_raises_error(self):
        """Test that internal nodes must have children."""
        keys = [1, 2, 3]
        
        with pytest.raises(ValueError, match="Non-leaf nodes must have children"):
            BTreeNode(keys=keys, children=None, is_leaf=False, num_keys=3)
    
    def test_keys_count_mismatch_raises_error(self):
        """Test that num_keys cannot exceed the length of keys."""
        keys = [1, 2]  # Only 2 keys in array
        
        with pytest.raises(ValueError, match="num_keys cannot exceed keys array size"):
            BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)  # Try to use 3 keys
    
    def test_children_count_mismatch_raises_error(self):
        """Test that internal nodes must have sufficient children array size."""
        keys = [1, 2, 3]
        children = [None, None]  # Only 2 children, need 4 for 3 keys
        
        with pytest.raises(ValueError, match="Insufficient children array size"):
            BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
    
    def test_repr_leaf_node(self):
        """Test string representation of a leaf node."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        expected = "BTreeNode(keys=[1, 2, 3], is_leaf=True)"
        assert repr(node) == expected
    
    def test_repr_internal_node(self):
        """Test string representation of an internal node."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        expected = "BTreeNode(keys=[1, 2, 3], is_leaf=False)"
        assert repr(node) == expected
    
    def test_get_memory_size_leaf_node(self):
        """Test memory size calculation for leaf node."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        memory_size = node.get_memory_size()
        assert memory_size > 0
        assert isinstance(memory_size, int)
    
    def test_get_memory_size_internal_node(self):
        """Test memory size calculation for internal node."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        memory_size = node.get_memory_size()
        assert memory_size > 0
        assert isinstance(memory_size, int)
    
    def test_is_full(self):
        """Test is_full method."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        assert node.is_full(3) is True
        assert node.is_full(4) is False
        assert node.is_full(5) is False
    
    def test_is_underflow(self):
        """Test is_underflow method."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        assert node.is_underflow(2) is False
        assert node.is_underflow(3) is False
        assert node.is_underflow(4) is True
    
    def test_insert_key(self):
        """Test inserting a key at a specific index."""
        keys = [1, 2, 3]  # Only num_keys elements at init
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        # Add extra capacity for insertion
        node.keys.extend([None, None])
        node.insert_key(5, 1)  # Insert at index 1
        assert node.num_keys == 4
        assert node.keys[:4] == [1, 5, 2, 3]
    
    def test_insert_key_invalid_index(self):
        """Test inserting a key at an invalid index."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        with pytest.raises(IndexError, match="Invalid index for key insertion"):
            node.insert_key(5, 4)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid index for key insertion"):
            node.insert_key(5, -1)  # Negative index
    
    def test_remove_key(self):
        """Test removing a key at a specific index."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        removed_key = node.remove_key(1)  # Remove key at index 1
        
        assert removed_key == 2
        assert node.num_keys == 2
        assert node.keys[:2] == [1, 3]
    
    def test_remove_key_invalid_index(self):
        """Test removing a key at an invalid index."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        with pytest.raises(IndexError, match="Invalid index for key removal"):
            node.remove_key(3)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid index for key removal"):
            node.remove_key(-1)  # Negative index
    
    def test_insert_child(self):
        """Test inserting a child at a specific index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]  # Exactly num_keys+1
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        # Add extra capacity for insertion
        node.children.append(None)
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        node.insert_child(child_node, 1)
        assert node.children[1] == child_node
    
    def test_insert_child_leaf_node_raises_error(self):
        """Test that leaf nodes cannot insert children."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        
        with pytest.raises(ValueError, match="Leaf nodes cannot have children"):
            node.insert_child(child_node, 0)
    
    def test_insert_child_invalid_index(self):
        """Test inserting a child at an invalid index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        
        with pytest.raises(IndexError, match="Invalid index for child insertion"):
            node.insert_child(child_node, 5)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid index for child insertion"):
            node.insert_child(child_node, -1)  # Negative index
    
    def test_remove_child(self):
        """Test removing a child at a specific index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        node.children[1] = child_node
        
        removed_child = node.remove_child(1)
        
        assert removed_child == child_node
        assert node.children[1] is None
    
    def test_remove_child_leaf_node_raises_error(self):
        """Test that leaf nodes cannot remove children."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        with pytest.raises(ValueError, match="Leaf nodes cannot have children"):
            node.remove_child(0)
    
    def test_remove_child_invalid_index(self):
        """Test removing a child at an invalid index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        with pytest.raises(IndexError, match="Invalid index for child removal"):
            node.remove_child(4)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid index for child removal"):
            node.remove_child(-1)  # Negative index
    
    def test_get_key(self):
        """Test getting a key at a specific index."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        assert node.get_key(0) == 1
        assert node.get_key(1) == 2
        assert node.get_key(2) == 3
    
    def test_get_key_invalid_index(self):
        """Test getting a key at an invalid index."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        with pytest.raises(IndexError, match="Invalid key index"):
            node.get_key(3)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid key index"):
            node.get_key(-1)  # Negative index
    
    def test_set_key(self):
        """Test setting a key at a specific index."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        node.set_key(1, 5)
        
        assert node.get_key(1) == 5
        assert node.keys[1] == 5
    
    def test_set_key_invalid_index(self):
        """Test setting a key at an invalid index."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        with pytest.raises(IndexError, match="Invalid key index"):
            node.set_key(3, 5)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid key index"):
            node.set_key(-1, 5)  # Negative index
    
    def test_get_child(self):
        """Test getting a child at a specific index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        node.children[1] = child_node
        
        assert node.get_child(1) == child_node
        assert node.get_child(0) is None
    
    def test_get_child_leaf_node_raises_error(self):
        """Test that leaf nodes cannot get children."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        with pytest.raises(ValueError, match="Leaf nodes cannot have children"):
            node.get_child(0)
    
    def test_get_child_invalid_index(self):
        """Test getting a child at an invalid index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        with pytest.raises(IndexError, match="Invalid child index"):
            node.get_child(4)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid child index"):
            node.get_child(-1)  # Negative index
    
    def test_set_child(self):
        """Test setting a child at a specific index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        node.set_child(1, child_node)
        
        assert node.get_child(1) == child_node
        assert node.children[1] == child_node
    
    def test_set_child_leaf_node_raises_error(self):
        """Test that leaf nodes cannot set children."""
        keys = [1, 2, 3]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=3)
        
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        
        with pytest.raises(ValueError, match="Leaf nodes cannot have children"):
            node.set_child(0, child_node)
    
    def test_set_child_invalid_index(self):
        """Test setting a child at an invalid index."""
        keys = [1, 2, 3]
        children = [None, None, None, None]
        node = BTreeNode(keys=keys, children=children, is_leaf=False, num_keys=3)
        
        child_node = BTreeNode(keys=[4, 5], children=None, is_leaf=True, num_keys=2)
        
        with pytest.raises(IndexError, match="Invalid child index"):
            node.set_child(4, child_node)  # Index out of bounds
        
        with pytest.raises(IndexError, match="Invalid child index"):
            node.set_child(-1, child_node)  # Negative index
    
    def test_find_key_index(self):
        """Test finding the index where a key should be inserted."""
        keys = [1, 3, 5, 7, 9]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=5)
        
        # Define a simple comparison function
        def compare(x, y):
            return -1 if x < y else (1 if x > y else 0)
        
        assert node.find_key_index(0, compare) == 0  # Before first key
        assert node.find_key_index(2, compare) == 1  # Between keys
        assert node.find_key_index(4, compare) == 2  # Between keys
        assert node.find_key_index(6, compare) == 3  # Between keys
        assert node.find_key_index(8, compare) == 4  # Between keys
        assert node.find_key_index(10, compare) == 5  # After last key
    
    def test_has_key(self):
        """Test checking if a node contains a specific key."""
        keys = [1, 3, 5, 7, 9]
        node = BTreeNode(keys=keys, children=None, is_leaf=True, num_keys=5)
        
        # Define a simple comparison function
        def compare(x, y):
            return -1 if x < y else (1 if x > y else 0)
        
        assert node.has_key(1, compare) is True
        assert node.has_key(3, compare) is True
        assert node.has_key(5, compare) is True
        assert node.has_key(7, compare) is True
        assert node.has_key(9, compare) is True
        
        assert node.has_key(0, compare) is False
        assert node.has_key(2, compare) is False
        assert node.has_key(4, compare) is False
        assert node.has_key(6, compare) is False
        assert node.has_key(8, compare) is False
        assert node.has_key(10, compare) is False


if __name__ == "__main__":
    pytest.main([__file__]) 