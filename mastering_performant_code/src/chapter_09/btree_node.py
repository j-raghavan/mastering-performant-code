"""
B-Tree Node Implementation

This module provides the BTreeNode class, which represents individual nodes
in a B-Tree data structure. Each node contains keys, child pointers, and
metadata about its structure.
"""

from typing import TypeVar, Generic, Optional, List
from dataclasses import dataclass
T = TypeVar('T')

@dataclass
class BTreeNode(Generic[T]):
    """
    A node in a B-Tree.
    
    Each node contains:
    - keys: sorted array of keys
    - children: array of child pointers (None for leaf nodes)
    - is_leaf: boolean indicating if this is a leaf node
    - num_keys: number of keys currently stored
    
    Args:
        keys: Array of keys stored in this node
        children: Array of child pointers (None for leaf nodes)
        is_leaf: Whether this node is a leaf
        num_keys: Number of keys currently stored
    """
    keys: List[T]
    children: Optional[List['BTreeNode[T]']]
    is_leaf: bool
    num_keys: int
    
    def __post_init__(self) -> None:
        """Validate node properties after initialization."""
        if self.is_leaf and self.children is not None:
            raise ValueError("Leaf nodes cannot have children")
        if not self.is_leaf and self.children is None:
            raise ValueError("Non-leaf nodes must have children")
        if self.num_keys > len(self.keys):
            raise ValueError("num_keys cannot exceed keys array size")
        if not self.is_leaf and self.children and self.num_keys + 1 > len(self.children):
            raise ValueError("Insufficient children array size")
    
    def __repr__(self) -> str:
        """String representation of the node."""
        return f"BTreeNode(keys={self.keys[:self.num_keys]}, is_leaf={self.is_leaf})"
    
    def get_memory_size(self) -> int:
        """Calculate accurate memory usage of this node."""
        base_size = sys.getsizeof(self)
        
        # Count only used keys
        keys_size = sum(sys.getsizeof(self.keys[i]) for i in range(self.num_keys))
        keys_size += sys.getsizeof(self.keys)  # Array overhead
        
        children_size = 0
        if self.children:
            children_size = sys.getsizeof(self.children)  # Array overhead
            # Count only used children
            used_children = self.num_keys + 1 if not self.is_leaf else 0
            children_size += sum(sys.getsizeof(self.children[i]) 
                               for i in range(used_children) 
                               if self.children[i] is not None)
        
        return base_size + keys_size + children_size
    
    def is_full(self, max_keys: int) -> bool:
        """Check if the node is full (has max_keys keys)."""
        return self.num_keys >= max_keys
    
    def is_underflow(self, min_keys: int) -> bool:
        """Check if the node is underflow (has fewer than min_keys keys)."""
        return self.num_keys < min_keys
    
    def insert_key(self, key: T, index: int) -> None:
        """Insert a key at the specified index."""
        if index < 0 or index > self.num_keys:
            raise IndexError("Invalid index for key insertion")
        
        # Make room for the new key
        for i in range(self.num_keys, index, -1):
            self.keys[i] = self.keys[i - 1]
        
        # Insert the key
        self.keys[index] = key
        self.num_keys += 1
    
    def remove_key(self, index: int) -> T:
        """Remove and return the key at the specified index."""
        if index < 0 or index >= self.num_keys:
            raise IndexError("Invalid index for key removal")
        
        key = self.keys[index]
        
        # Shift keys to the left
        for i in range(index, self.num_keys - 1):
            self.keys[i] = self.keys[i + 1]
        
        self.num_keys -= 1
        return key
    
    def insert_child(self, child: 'BTreeNode[T]', index: int) -> None:
        """Insert a child at the specified index."""
        if self.is_leaf:
            raise ValueError("Leaf nodes cannot have children")
        
        if index < 0 or index > self.num_keys + 1:
            raise IndexError("Invalid index for child insertion")
        
        # Make room for the new child
        for i in range(self.num_keys + 1, index, -1):
            self.children[i] = self.children[i - 1]
        
        # Insert the child
        self.children[index] = child
    
    def remove_child(self, index: int) -> 'BTreeNode[T]':
        """Remove and return the child at the specified index."""
        if self.is_leaf:
            raise ValueError("Leaf nodes cannot have children")
        
        if index < 0 or index > self.num_keys:
            raise IndexError("Invalid index for child removal")
        
        child = self.children[index]
        
        # Shift children to the left
        for i in range(index, self.num_keys):
            self.children[i] = self.children[i + 1]
        
        return child
    
    def get_key(self, index: int) -> T:
        """Get the key at the specified index."""
        if index < 0 or index >= self.num_keys:
            raise IndexError("Invalid key index")
        return self.keys[index]
    
    def set_key(self, index: int, key: T) -> None:
        """Set the key at the specified index."""
        if index < 0 or index >= self.num_keys:
            raise IndexError("Invalid key index")
        self.keys[index] = key
    
    def get_child(self, index: int) -> Optional['BTreeNode[T]']:
        """Get the child at the specified index."""
        if self.is_leaf:
            raise ValueError("Leaf nodes cannot have children")
        
        if index < 0 or index > self.num_keys:
            raise IndexError("Invalid child index")
        
        return self.children[index]
    
    def set_child(self, index: int, child: Optional['BTreeNode[T]']) -> None:
        """Set the child at the specified index."""
        if self.is_leaf:
            raise ValueError("Leaf nodes cannot have children")
        
        if index < 0 or index > self.num_keys:
            raise IndexError("Invalid child index")
        
        self.children[index] = child
    
    def find_key_index(self, key: T, compare_func) -> int:
        """Find the index where a key should be inserted or found."""
        i = 0
        while i < self.num_keys and compare_func(key, self.keys[i]) > 0:
            i += 1
        return i
    
    def has_key(self, key: T, compare_func) -> bool:
        """Check if the node contains a specific key."""
        index = self.find_key_index(key, compare_func)
        return index < self.num_keys and compare_func(key, self.keys[index]) == 0 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running btree_node demonstration...")
    print("=" * 50)

    # Create instance of BTreeNode
    try:
        instance = BTreeNode()
        print(f"✓ Created BTreeNode instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.insert(5)
        instance.insert(3)
        instance.insert(7)
        print(f"  After inserting elements: {instance}")
    except Exception as e:
        print(f"✗ Error creating BTreeNode instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
