"""
BST Node implementation for Chapter 6.

This module provides the core node structure for Binary Search Trees.
"""

from typing import TypeVar, Generic, Optional
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class BSTNode(Generic[T]):
    """
    A node in a Binary Search Tree.
    
    Each node contains:
    - value: The data stored in the node
    - left: Reference to left child (smaller values)
    - right: Reference to right child (larger values)
    - parent: Reference to parent node (for efficient operations)
    """
    value: T
    left: Optional['BSTNode[T]'] = None
    right: Optional['BSTNode[T]'] = None
    parent: Optional['BSTNode[T]'] = None
    
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
    
    def get_only_child(self) -> Optional['BSTNode[T]']:
        """Get the only child if this node has exactly one child."""
        if self.left is not None and self.right is None:
            return self.left
        elif self.left is None and self.right is not None:
            return self.right
        return None
    
    def get_children_count(self) -> int:
        """Get the number of children this node has."""
        count = 0
        if self.left:
            count += 1
        if self.right:
            count += 1
        return count
    
    def is_left_child(self) -> bool:
        """Check if this node is a left child of its parent."""
        return self.parent is not None and self.parent.left == self
    
    def is_right_child(self) -> bool:
        """Check if this node is a right child of its parent."""
        return self.parent is not None and self.parent.right == self
    
    def get_sibling(self) -> Optional['BSTNode[T]']:
        """Get the sibling of this node."""
        if self.parent is None:
            return None
        
        if self.is_left_child():
            return self.parent.right
        else:
            return self.parent.left
    
    def __repr__(self) -> str:
        return f"BSTNode(value={self.value})" 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running bst_node demonstration...")
    print("=" * 50)

    # Create instance of BSTNode
    try:
        instance = BSTNode()
        print(f"✓ Created BSTNode instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.insert(5)
        instance.insert(3)
        instance.insert(7)
        print(f"  After inserting elements: {instance}")
    except Exception as e:
        print(f"✗ Error creating BSTNode instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
