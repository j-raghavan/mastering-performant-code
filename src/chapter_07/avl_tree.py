"""
AVL Tree Implementation

This module provides a complete AVL tree implementation with automatic balancing,
including all standard BST operations with guaranteed O(log n) performance.
"""

from typing import TypeVar, Generic, Optional, Iterator, List
from .avl_node import AVLNode

T = TypeVar('T')

class AVLTree(Generic[T]):
    """
    An AVL Tree implementation with automatic balancing.
    
    This implementation provides:
    - Guaranteed O(log n) operations through automatic balancing
    - Four types of rotations to maintain AVL property
    - Efficient height and balance factor calculations
    - All standard BST operations with improved worst-case performance
    """
    
    def __init__(self):
        self._root: Optional[AVLNode[T]] = None
        self._size: int = 0
    
    def __len__(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._root is None
    
    def height(self) -> int:
        """Get the height of the tree."""
        return self._root.height if self._root else 0
    
    def insert(self, value: T) -> None:
        """Insert a value into the AVL tree and rebalance if necessary."""
        if self._root is None:
            self._root = AVLNode(value)
            self._size = 1
        else:
            self._root = self._insert_recursive(self._root, value)
            self._size += 1
    
    def _insert_recursive(self, node: AVLNode[T], value: T) -> AVLNode[T]:
        """Recursively insert a value and rebalance the tree."""
        if value < node.value:
            if node.left is None:
                node.left = AVLNode(value, parent=node)
            else:
                node.left = self._insert_recursive(node.left, value)
        else:  # value >= node.value
            if node.right is None:
                node.right = AVLNode(value, parent=node)
            else:
                node.right = self._insert_recursive(node.right, value)
        
        # Update height and rebalance
        node.update_height()
        return self._rebalance(node)
    
    def delete(self, value: T) -> bool:
        """Delete a value from the AVL tree and rebalance if necessary."""
        if self._root is None:
            return False
        
        # Check if the value exists before deleting
        if self.search(value) is None:
            return False
        
        self._root = self._delete_recursive(self._root, value)
        return True
    
    def _delete_recursive(self, node: Optional[AVLNode[T]], value: T) -> Optional[AVLNode[T]]:
        """Recursively delete a value and rebalance the tree."""
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node to delete found
            self._size -= 1
            
            # Case 1: Node is a leaf
            if node.is_leaf():
                return None
            
            # Case 2: Node has one child
            elif node.has_one_child():
                child = node.get_only_child()
                if child:
                    child.parent = node.parent
                return child
            
            # Case 3: Node has two children
            else:
                # Find successor (smallest value in right subtree)
                successor = self._find_min(node.right)
                if successor:
                    # Copy successor's value to current node
                    node.value = successor.value
                    # Delete successor (don't decrement size again)
                    node.right = self._delete_recursive(node.right, successor.value)
                    # Increment size back since we're not actually deleting a node
                    self._size += 1
        
        # Update height and rebalance
        if node:
            node.update_height()
            return self._rebalance(node)
        return None
    
    def search(self, value: T) -> Optional[AVLNode[T]]:
        """Search for a value in the AVL tree."""
        return self._search_recursive(self._root, value)
    
    def _search_recursive(self, node: Optional[AVLNode[T]], value: T) -> Optional[AVLNode[T]]:
        """Recursively search for a value in the tree."""
        if node is None or node.value == value:
            return node
        
        if value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def _find_min(self, node: Optional[AVLNode[T]]) -> Optional[AVLNode[T]]:
        """Find the minimum value in the subtree rooted at node."""
        if node is None:
            return None
        
        while node.left is not None:
            node = node.left
        return node
    
    def _find_max(self, node: Optional[AVLNode[T]]) -> Optional[AVLNode[T]]:
        """Find the maximum value in the subtree rooted at node."""
        if node is None:
            return None
        
        while node.right is not None:
            node = node.right
        return node
    
    def _rebalance(self, node: AVLNode[T]) -> AVLNode[T]:
        """Rebalance the tree starting from the given node."""
        balance_factor = node.get_balance_factor()
        
        # Left heavy
        if balance_factor < -1:
            # Left-Right case
            if node.left and node.left.get_balance_factor() > 0:
                node.left = self._left_rotate(node.left)
            # Left-Left case
            return self._right_rotate(node)
        
        # Right heavy
        elif balance_factor > 1:
            # Right-Left case
            if node.right and node.right.get_balance_factor() < 0:
                node.right = self._right_rotate(node.right)
            # Right-Right case
            return self._left_rotate(node)
        
        return node
    
    def _left_rotate(self, node: AVLNode[T]) -> AVLNode[T]:
        """Perform a left rotation on the given node."""
        right_child = node.right
        if right_child is None:
            return node
        
        # Perform rotation
        node.right = right_child.left
        if right_child.left:
            right_child.left.parent = node
        
        right_child.left = node
        right_child.parent = node.parent
        node.parent = right_child
        
        # Update heights
        node.update_height()
        right_child.update_height()
        
        return right_child
    
    def _right_rotate(self, node: AVLNode[T]) -> AVLNode[T]:
        """Perform a right rotation on the given node."""
        left_child = node.left
        if left_child is None:
            return node
        
        # Perform rotation
        node.left = left_child.right
        if left_child.right:
            left_child.right.parent = node
        
        left_child.right = node
        left_child.parent = node.parent
        node.parent = left_child
        
        # Update heights
        node.update_height()
        left_child.update_height()
        
        return left_child
    
    def inorder_traversal(self) -> Iterator[T]:
        """Perform inorder traversal of the tree."""
        def _inorder(node: Optional[AVLNode[T]]) -> Iterator[T]:
            if node:
                yield from _inorder(node.left)
                yield node.value
                yield from _inorder(node.right)
        
        yield from _inorder(self._root)
    
    def preorder_traversal(self) -> Iterator[T]:
        """Perform preorder traversal of the tree."""
        def _preorder(node: Optional[AVLNode[T]]) -> Iterator[T]:
            if node:
                yield node.value
                yield from _preorder(node.left)
                yield from _preorder(node.right)
        
        yield from _preorder(self._root)
    
    def postorder_traversal(self) -> Iterator[T]:
        """Perform postorder traversal of the tree."""
        def _postorder(node: Optional[AVLNode[T]]) -> Iterator[T]:
            if node:
                yield from _postorder(node.left)
                yield from _postorder(node.right)
                yield node.value
        
        yield from _postorder(self._root)
    
    def level_order_traversal(self) -> Iterator[List[T]]:
        """Perform level-order traversal of the tree."""
        if self._root is None:
            return
        
        queue = [self._root]
        while queue:
            level_size = len(queue)
            level_values = []
            
            for _ in range(level_size):
                node = queue.pop(0)
                level_values.append(node.value)
                
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            
            yield level_values
    
    def get_sorted_values(self) -> List[T]:
        """Get all values in sorted order."""
        return list(self.inorder_traversal())
    
    def successor(self, value: T) -> Optional[T]:
        """Find the successor of the given value."""
        node = self.search(value)
        if node is None:
            return None
        
        # If node has right child, successor is minimum of right subtree
        if node.right:
            successor_node = self._find_min(node.right)
            return successor_node.value if successor_node else None
        
        # Otherwise, successor is the first ancestor where we turn right
        current = node
        while current.parent and current == current.parent.right:
            current = current.parent
        
        return current.parent.value if current.parent else None
    
    def predecessor(self, value: T) -> Optional[T]:
        """Find the predecessor of the given value."""
        node = self.search(value)
        if node is None:
            return None
        
        # If node has left child, predecessor is maximum of left subtree
        if node.left:
            predecessor_node = self._find_max(node.left)
            return predecessor_node.value if predecessor_node else None
        
        # Otherwise, predecessor is the first ancestor where we turn left
        current = node
        while current.parent and current == current.parent.left:
            current = current.parent
        
        return current.parent.value if current.parent else None
    
    def is_balanced(self) -> bool:
        """Check if the tree satisfies the AVL property."""
        def _check_balance(node: Optional[AVLNode[T]]) -> bool:
            if node is None:
                return True
            
            balance_factor = node.get_balance_factor()
            if abs(balance_factor) > 1:
                return False
            
            return _check_balance(node.left) and _check_balance(node.right)
        
        return _check_balance(self._root)
    
    def __repr__(self) -> str:
        return f"AVLTree({self.get_sorted_values()})" 