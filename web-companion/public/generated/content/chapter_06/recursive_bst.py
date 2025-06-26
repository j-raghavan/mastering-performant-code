"""
Recursive Binary Search Tree implementation for Chapter 6.

This module provides a BST implementation using recursive algorithms.
"""

from typing import TypeVar, Generic, Optional, Iterator, List
from .bst_node import BSTNode

T = TypeVar('T')

class RecursiveBST(Generic[T]):
    """
    A Binary Search Tree implementation using recursive algorithms.
    
    This implementation provides:
    - Efficient search, insert, and delete operations
    - Multiple traversal methods
    - Successor and predecessor operations
    - Memory-efficient node management
    """
    
    def __init__(self):
        self._root: Optional[BSTNode[T]] = None
        self._size: int = 0
    
    def __len__(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._root is None
    
    def insert(self, value: T) -> None:
        """Insert a value into the BST."""
        if self._root is None:
            self._root = BSTNode(value)
            self._size = 1
        else:
            self._insert_recursive(self._root, value)
    
    def _insert_recursive(self, node: BSTNode[T], value: T) -> None:
        """Recursively insert a value into the subtree rooted at node."""
        if value < node.value:
            if node.left is None:
                node.left = BSTNode(value, parent=node)
                self._size += 1
            else:
                self._insert_recursive(node.left, value)
        else:  # value >= node.value
            if node.right is None:
                node.right = BSTNode(value, parent=node)
                self._size += 1
            else:
                self._insert_recursive(node.right, value)
    
    def search(self, value: T) -> Optional[BSTNode[T]]:
        """Search for a value in the BST."""
        return self._search_recursive(self._root, value)
    
    def _search_recursive(self, node: Optional[BSTNode[T]], value: T) -> Optional[BSTNode[T]]:
        """Recursively search for a value in the subtree rooted at node."""
        if node is None or node.value == value:
            return node
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def contains(self, value: T) -> bool:
        """Check if a value exists in the BST."""
        return self.search(value) is not None
    
    def delete(self, value: T) -> bool:
        """Delete a value from the BST."""
        node = self.search(value)
        if node is None:
            return False
        
        self._delete_node(node)
        self._size -= 1
        return True
    
    def _delete_node(self, node: BSTNode[T]) -> None:
        """Delete a node from the BST."""
        if node.is_leaf():
            self._delete_leaf(node)
        elif node.has_one_child():
            self._delete_node_with_one_child(node)
        else:
            self._delete_node_with_two_children(node)
    
    def _delete_leaf(self, node: BSTNode[T]) -> None:
        """Delete a leaf node."""
        if node.parent is None:
            self._root = None
        elif node.parent.left == node:
            node.parent.left = None
        else:
            node.parent.right = None
    
    def _delete_node_with_one_child(self, node: BSTNode[T]) -> None:
        """Delete a node with exactly one child."""
        child = node.get_only_child()
        if node.parent is None:
            self._root = child
            if child:
                child.parent = None
        elif node.parent.left == node:
            node.parent.left = child
            if child:
                child.parent = node.parent
        else:
            node.parent.right = child
            if child:
                child.parent = node.parent
    
    def _delete_node_with_two_children(self, node: BSTNode[T]) -> None:
        """Delete a node with two children using successor."""
        successor = self._find_successor(node)
        if successor:
            node.value = successor.value
            self._delete_node(successor)
    
    def _find_successor(self, node: BSTNode[T]) -> Optional[BSTNode[T]]:
        """Find the successor of a node."""
        if node.right:
            return self._find_minimum(node.right)
        
        # Find the lowest ancestor whose left child is also an ancestor
        current = node
        while current.parent and current.parent.right == current:
            current = current.parent
        return current.parent
    
    def _find_predecessor(self, node: BSTNode[T]) -> Optional[BSTNode[T]]:
        """Find the predecessor of a node."""
        if node.left:
            return self._find_maximum(node.left)
        
        # Find the lowest ancestor whose right child is also an ancestor
        current = node
        while current.parent and current.parent.left == current:
            current = current.parent
        return current.parent
    
    def _find_minimum(self, node: BSTNode[T]) -> BSTNode[T]:
        """Find the minimum value in the subtree rooted at node."""
        while node.left:
            node = node.left
        return node
    
    def _find_maximum(self, node: BSTNode[T]) -> BSTNode[T]:
        """Find the maximum value in the subtree rooted at node."""
        while node.right:
            node = node.right
        return node
    
    def find_minimum(self) -> Optional[T]:
        """Find the minimum value in the BST."""
        if self._root is None:
            return None
        return self._find_minimum(self._root).value
    
    def find_maximum(self) -> Optional[T]:
        """Find the maximum value in the BST."""
        if self._root is None:
            return None
        return self._find_maximum(self._root).value
    
    def get_successor(self, value: T) -> Optional[T]:
        """Get the successor of a value in the BST."""
        node = self.search(value)
        if node is None:
            return None
        
        successor = self._find_successor(node)
        return successor.value if successor else None
    
    def get_predecessor(self, value: T) -> Optional[T]:
        """Get the predecessor of a value in the BST."""
        node = self.search(value)
        if node is None:
            return None
        
        predecessor = self._find_predecessor(node)
        return predecessor.value if predecessor else None
    
    def inorder_traversal(self) -> Iterator[T]:
        """Perform inorder traversal (Left → Root → Right)."""
        def inorder_recursive(node: Optional[BSTNode[T]]) -> Iterator[T]:
            if node:
                yield from inorder_recursive(node.left)
                yield node.value
                yield from inorder_recursive(node.right)
        
        yield from inorder_recursive(self._root)
    
    def preorder_traversal(self) -> Iterator[T]:
        """Perform preorder traversal (Root → Left → Right)."""
        def preorder_recursive(node: Optional[BSTNode[T]]) -> Iterator[T]:
            if node:
                yield node.value
                yield from preorder_recursive(node.left)
                yield from preorder_recursive(node.right)
        
        yield from preorder_recursive(self._root)
    
    def postorder_traversal(self) -> Iterator[T]:
        """Perform postorder traversal (Left → Right → Root)."""
        def postorder_recursive(node: Optional[BSTNode[T]]) -> Iterator[T]:
            if node:
                yield from postorder_recursive(node.left)
                yield from postorder_recursive(node.right)
                yield node.value
        
        yield from postorder_recursive(self._root)
    
    def level_order_traversal(self) -> Iterator[T]:
        """Perform level-order traversal (breadth-first)."""
        if self._root is None:
            return
        
        from collections import deque
        queue = deque([self._root])
        
        while queue:
            node = queue.popleft()
            yield node.value
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    def get_sorted_list(self) -> List[T]:
        """Get all values in sorted order."""
        return list(self.inorder_traversal())
    
    def range_search(self, min_val: T, max_val: T) -> List[T]:
        """Get all values in the range [min_val, max_val]."""
        result = []
        self._range_search_recursive(self._root, min_val, max_val, result)
        return result
    
    def _range_search_recursive(self, node: Optional[BSTNode[T]], min_val: T, max_val: T, result: List[T]) -> None:
        """Recursively search for values in the given range."""
        if node is None:
            return
        
        # If current node is greater than min_val, search left subtree
        if min_val < node.value:
            self._range_search_recursive(node.left, min_val, max_val, result)
        
        # If current node is in range, add it to result
        if min_val <= node.value <= max_val:
            result.append(node.value)
        
        # If current node is less than max_val, search right subtree
        if node.value < max_val:
            self._range_search_recursive(node.right, min_val, max_val, result)
    
    def get_height(self) -> int:
        """Get the height of the tree."""
        return self._get_height_recursive(self._root)
    
    def _get_height_recursive(self, node: Optional[BSTNode[T]]) -> int:
        """Recursively calculate the height of a subtree."""
        if node is None:
            return -1
        return 1 + max(
            self._get_height_recursive(node.left),
            self._get_height_recursive(node.right)
        )
    
    def is_balanced(self) -> bool:
        """Check if the tree is balanced."""
        return self._is_balanced_recursive(self._root) != -1
    
    def _is_balanced_recursive(self, node: Optional[BSTNode[T]]) -> int:
        """Recursively check if a subtree is balanced. Returns -1 if unbalanced."""
        if node is None:
            return 0
        
        left_height = self._is_balanced_recursive(node.left)
        if left_height == -1:
            return -1
        
        right_height = self._is_balanced_recursive(node.right)
        if right_height == -1:
            return -1
        
        if abs(left_height - right_height) > 1:
            return -1
        
        return 1 + max(left_height, right_height)
    
    def clear(self) -> None:
        """Clear all elements from the tree."""
        self._root = None
        self._size = 0
    
    def __repr__(self) -> str:
        if self._root is None:
            return "RecursiveBST()"
        
        values = list(self.inorder_traversal())
        return f"RecursiveBST({values})" 