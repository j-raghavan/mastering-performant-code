"""
AVL Node Implementation

This module provides the AVLNode class for AVL trees, which includes
height tracking and balance factor calculations.
"""

from typing import TypeVar, Generic, Optional
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class AVLNode(Generic[T]):
    """
    A node in an AVL Tree.
    
    Each node contains:
    - value: The data stored in the node
    - left: Reference to left child (smaller values)
    - right: Reference to right child (larger values)
    - parent: Reference to parent node (for efficient operations)
    - height: Height of the subtree rooted at this node
    """
    value: T
    left: Optional['AVLNode[T]'] = None
    right: Optional['AVLNode[T]'] = None
    parent: Optional['AVLNode[T]'] = None
    height: int = 1
    
    def __post_init__(self):
        """Update parent references of children."""
        if self.left:
            self.left.parent = self
        if self.right:
            self.right.parent = self
    
    def is_leaf(self) -> bool:
        """Check if this node is a leaf (no children)."""
        return self.left is None and self.right is None
    
    def has_one_child(self) -> bool:
        """Check if this node has exactly one child."""
        return (self.left is None) != (self.right is None)
    
    def get_only_child(self) -> Optional['AVLNode[T]']:
        """Get the only child if this node has exactly one child."""
        if self.left is not None and self.right is None:
            return self.left
        elif self.left is None and self.right is not None:
            return self.right
        return None
    
    def get_balance_factor(self) -> int:
        """Calculate the balance factor of this node."""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return right_height - left_height
    
    def update_height(self) -> None:
        """Update the height of this node based on its children."""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1 