"""
Iterative Binary Search Tree implementation for Chapter 6.

This module provides a BST implementation using iterative algorithms.
"""

from typing import TypeVar, Generic, Optional, Iterator, List
from collections import deque
from .bst_node import BSTNode

T = TypeVar('T')

class IterativeBST(Generic[T]):
    """
    A Binary Search Tree implementation using iterative algorithms.
    
    This implementation provides the same functionality as RecursiveBST
    but uses iterative approaches for better performance and memory efficiency.
    """
    
    def __init__(self):
        self._root: Optional[BSTNode[T]] = None
        self._size: int = 0
    
    def __len__(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        return self._root is None
    
    def insert(self, value: T) -> None:
        """Insert a value into the BST iteratively."""
        if self._root is None:
            self._root = BSTNode(value)
            self._size = 1
            return
        
        current = self._root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = BSTNode(value, parent=current)
                    self._size += 1
                    break
                current = current.left
            else:  # value >= current.value
                if current.right is None:
                    current.right = BSTNode(value, parent=current)
                    self._size += 1
                    break
                current = current.right
    
    def search(self, value: T) -> Optional[BSTNode[T]]:
        """Search for a value in the BST iteratively."""
        current = self._root
        while current and current.value != value:
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return current
    
    def contains(self, value: T) -> bool:
        """Check if a value exists in the BST."""
        return self.search(value) is not None
    
    def delete(self, value: T) -> bool:
        """Delete a value from the BST iteratively."""
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
        """Find the successor of a node iteratively."""
        if node.right:
            return self._find_minimum(node.right)
        
        # Find the lowest ancestor whose left child is also an ancestor
        current = node
        while current.parent and current.parent.right == current:
            current = current.parent
        return current.parent
    
    def _find_predecessor(self, node: BSTNode[T]) -> Optional[BSTNode[T]]:
        """Find the predecessor of a node iteratively."""
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
        """Perform inorder traversal iteratively using a stack."""
        if self._root is None:
            return
        
        stack = []
        current = self._root
        
        while current or stack:
            # Reach the leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process current node
            current = stack.pop()
            yield current.value
            
            # Move to right subtree
            current = current.right
    
    def preorder_traversal(self) -> Iterator[T]:
        """Perform preorder traversal iteratively using a stack."""
        if self._root is None:
            return
        
        stack = [self._root]
        
        while stack:
            current = stack.pop()
            yield current.value
            
            # Push right child first (so left is processed first)
            if current.right:
                stack.append(current.right)
            if current.left:
                stack.append(current.left)
    
    def postorder_traversal(self) -> Iterator[T]:
        """Perform postorder traversal iteratively using two stacks."""
        if self._root is None:
            return
        
        stack1 = [self._root]
        stack2 = []
        
        while stack1:
            current = stack1.pop()
            stack2.append(current)
            
            if current.left:
                stack1.append(current.left)
            if current.right:
                stack1.append(current.right)
        
        while stack2:
            yield stack2.pop().value
    
    def level_order_traversal(self) -> Iterator[T]:
        """Perform level-order traversal using a queue."""
        if self._root is None:
            return
        
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
        stack = []
        current = self._root
        
        while current or stack:
            # Reach the leftmost node
            while current:
                stack.append(current)
                current = current.left
            
            # Process current node
            current = stack.pop()
            
            # If current node is in range, add it to result
            if min_val <= current.value <= max_val:
                result.append(current.value)
            elif current.value > max_val:
                break  # No need to check further
            
            # Move to right subtree
            current = current.right
        
        return result
    
    def get_height(self) -> int:
        """Get the height of the tree iteratively."""
        if self._root is None:
            return -1
        
        queue = deque([(self._root, 0)])
        max_height = 0
        
        while queue:
            node, height = queue.popleft()
            max_height = max(max_height, height)
            
            if node.left:
                queue.append((node.left, height + 1))
            if node.right:
                queue.append((node.right, height + 1))
        
        return max_height
    
    def is_balanced(self) -> bool:
        """Check if the tree is balanced iteratively."""
        if self._root is None:
            return True
        
        stack = [(self._root, False)]
        heights = {}
        
        while stack:
            node, visited = stack.pop()
            
            if visited:
                left_height = heights.get(id(node.left), -1)
                right_height = heights.get(id(node.right), -1)
                
                if abs(left_height - right_height) > 1:
                    return False
                
                heights[id(node)] = 1 + max(left_height, right_height)
            else:
                stack.append((node, True))
                if node.right:
                    stack.append((node.right, False))
                if node.left:
                    stack.append((node.left, False))
        
        return True
    
    def get_node_count(self) -> int:
        """Get the number of nodes in the tree iteratively."""
        if self._root is None:
            return 0
        
        count = 0
        stack = [self._root]
        
        while stack:
            node = stack.pop()
            count += 1
            
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        
        return count
    
    def get_leaf_count(self) -> int:
        """Get the number of leaf nodes in the tree iteratively."""
        if self._root is None:
            return 0
        
        count = 0
        stack = [self._root]
        
        while stack:
            node = stack.pop()
            
            if node.is_leaf():
                count += 1
            else:
                if node.right:
                    stack.append(node.right)
                if node.left:
                    stack.append(node.left)
        
        return count
    
    def get_internal_node_count(self) -> int:
        """Get the number of internal nodes (non-leaf nodes) in the tree."""
        return self.get_node_count() - self.get_leaf_count()
    
    def clear(self) -> None:
        """Clear all elements from the tree."""
        self._root = None
        self._size = 0
    
    def __repr__(self) -> str:
        if self._root is None:
            return "IterativeBST()"
        
        values = list(self.inorder_traversal())
        return f"IterativeBST({values})" 