"""
B-Tree Implementation

This module provides a complete B-Tree implementation with all standard operations
including search, insert, delete, and range queries. B-Trees are designed for
efficient external storage with guaranteed O(log n) performance.
"""

import sys
from typing import TypeVar, Generic, Optional, List, Iterator, Callable
from .btree_node import BTreeNode

T = TypeVar('T')

class BTree(Generic[T]):
    """
    A B-Tree implementation for efficient external storage.
    
    This B-Tree maintains the following properties:
    - Every node has at most 2t children
    - Every non-leaf node (except root) has at least t children
    - The root has at least 2 children if it's not a leaf
    - All leaves are at the same level
    - A non-leaf node with k children contains k-1 keys
    
    Args:
        min_degree: Minimum degree of the B-Tree (t ≥ 2)
        key_comparator: Optional custom comparator for keys
    """
    
    def __init__(self, min_degree: int = 3, key_comparator: Optional[Callable[[T, T], int]] = None) -> None:
        if min_degree < 2:
            raise ValueError("Minimum degree must be at least 2")
        
        self.min_degree = min_degree
        self.max_keys = 2 * min_degree - 1
        self.min_keys = min_degree - 1
        self.root: Optional[BTreeNode[T]] = None
        self.size = 0
        self.height = 0
        
        # Use custom comparator or default to < operator
        if key_comparator:
            self._compare = key_comparator
        else:
            self._compare = lambda x, y: -1 if x < y else (1 if x > y else 0)
    
    def __len__(self) -> int:
        """Return the number of keys in the B-Tree."""
        return self.size
    
    def __contains__(self, key: T) -> bool:
        """Check if a key exists in the B-Tree."""
        return self.search(key) is not None
    
    def is_empty(self) -> bool:
        """Check if the B-Tree is empty."""
        return self.root is None
    
    def clear(self) -> None:
        """Remove all keys from the B-Tree."""
        self.root = None
        self.size = 0
        self.height = 0
    
    def _create_node(self, is_leaf: bool) -> BTreeNode[T]:
        """Create a new B-Tree node."""
        return BTreeNode(
            keys=[None] * self.max_keys,
            children=[None] * (self.max_keys + 1) if not is_leaf else None,
            is_leaf=is_leaf,
            num_keys=0
        )
    
    def search(self, key: T) -> Optional[T]:
        """
        Search for a key in the B-Tree.
        
        Args:
            key: The key to search for
            
        Returns:
            The key if found, None otherwise
        """
        if self.root is None:
            return None
        
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node: BTreeNode[T], key: T) -> Optional[T]:
        """Recursively search for a key in a subtree."""
        i = 0
        
        # Find the first key greater than or equal to the search key
        while i < node.num_keys and self._compare(key, node.keys[i]) > 0:
            i += 1
        
        # If we found the key, return it
        if i < node.num_keys and self._compare(key, node.keys[i]) == 0:
            return node.keys[i]
        
        # If this is a leaf, the key is not in the tree
        if node.is_leaf:
            return None
        
        # Otherwise, search in the appropriate child
        return self._search_recursive(node.children[i], key)
    
    def insert(self, key: T) -> None:
        """
        Insert a key into the B-Tree.
        
        Args:
            key: The key to insert
        """
        if self.root is None:
            # Create the first node
            self.root = self._create_node(is_leaf=True)
            self.root.keys[0] = key
            self.root.num_keys = 1
            self.size = 1
            self.height = 1
        else:
            # If the root is full, split it
            if self.root.num_keys == self.max_keys:
                old_root = self.root
                self.root = self._create_node(is_leaf=False)
                self.root.children[0] = old_root
                self._split_child(self.root, 0, old_root)
                self.height += 1
            
            # Insert the key
            self._insert_non_full(self.root, key)
            self.size += 1
    
    def _insert_non_full(self, node: BTreeNode[T], key: T) -> None:
        """Insert a key into a non-full node."""
        i = node.num_keys - 1
        
        if node.is_leaf:
            # Find the position to insert the key
            while i >= 0 and self._compare(key, node.keys[i]) < 0:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            
            # Insert the key
            node.keys[i + 1] = key
            node.num_keys += 1
        else:
            # Find the child to insert into
            while i >= 0 and self._compare(key, node.keys[i]) < 0:
                i -= 1
            i += 1
            
            # If the child is full, split it
            if node.children[i].num_keys == self.max_keys:
                self._split_child(node, i, node.children[i])
                
                # Determine which child to insert into
                if self._compare(key, node.keys[i]) > 0:
                    i += 1
            
            # Insert into the child
            self._insert_non_full(node.children[i], key)
    
    def _split_child(self, parent: BTreeNode[T], child_index: int, child: BTreeNode[T]) -> None:
        """Split a full child node."""
        # Create a new node for the right half
        new_child = self._create_node(is_leaf=child.is_leaf)
        new_child.num_keys = self.min_keys
        
        # Copy the right half of keys
        for j in range(self.min_keys):
            new_child.keys[j] = child.keys[j + self.min_keys + 1]
        
        # Copy the right half of children (if not a leaf)
        if not child.is_leaf:
            for j in range(self.min_keys + 1):
                new_child.children[j] = child.children[j + self.min_keys + 1]
        
        # Update the original child
        child.num_keys = self.min_keys
        
        # Make room for the new child in the parent
        for j in range(parent.num_keys, child_index, -1):
            parent.children[j + 1] = parent.children[j]
        
        # Insert the new child
        parent.children[child_index + 1] = new_child
        
        # Make room for the promoted key
        for j in range(parent.num_keys - 1, child_index - 1, -1):
            parent.keys[j + 1] = parent.keys[j]
        
        # Promote the middle key
        parent.keys[child_index] = child.keys[self.min_keys]
        parent.num_keys += 1
    
    def delete(self, key: T) -> bool:
        """
        Delete a key from the B-Tree.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False if it wasn't found
        """
        if self.root is None:
            return False
        
        # Delete the key
        deleted = self._delete_recursive(self.root, key)
        
        if deleted:
            self.size -= 1
            
            # If the root becomes empty, update the tree
            if self.root.num_keys == 0:
                if self.root.is_leaf:
                    self.root = None
                    self.height = 0
                else:
                    self.root = self.root.children[0]
                    self.height -= 1
        
        return deleted
    
    def _delete_recursive(self, node: BTreeNode[T], key: T) -> bool:
        """Recursively delete a key from a subtree."""
        i = 0
        
        # Find the key or the child to search in
        while i < node.num_keys and self._compare(key, node.keys[i]) > 0:
            i += 1
        
        if node.is_leaf:
            # Key is in this leaf node
            if i < node.num_keys and self._compare(key, node.keys[i]) == 0:
                # Remove the key
                for j in range(i, node.num_keys - 1):
                    node.keys[j] = node.keys[j + 1]
                node.num_keys -= 1
                return True
            return False
        else:
            # Key is in a child node
            if i < node.num_keys and self._compare(key, node.keys[i]) == 0:
                # Key is in this node, replace it with predecessor or successor
                return self._delete_internal_node(node, key, i)
            else:
                # Key is in a child
                return self._delete_from_child(node, key, i)
    
    def _delete_internal_node(self, node: BTreeNode[T], key: T, key_index: int) -> bool:
        """Delete a key from an internal node."""
        child = node.children[key_index]
        right_child = node.children[key_index + 1]
        
        if child.num_keys > self.min_keys:
            # Replace with predecessor
            predecessor = self._get_predecessor(child)
            node.keys[key_index] = predecessor
            return self._delete_recursive(child, predecessor)
        elif right_child.num_keys > self.min_keys:
            # Replace with successor
            successor = self._get_successor(right_child)
            node.keys[key_index] = successor
            return self._delete_recursive(right_child, successor)
        else:
            # Both children have minimum keys, merge them
            self._merge_children(node, key_index)
            return self._delete_recursive(child, key)
    
    def _delete_from_child(self, node: BTreeNode[T], key: T, child_index: int) -> bool:
        """Delete a key from a child node."""
        child = node.children[child_index]
        
        if child.num_keys == self.min_keys:
            # Ensure the child has enough keys
            self._ensure_child_has_keys(node, child_index)
            
            # Update child index if it changed
            if child_index > 0 and child_index < node.num_keys:
                if self._compare(key, node.keys[child_index - 1]) <= 0:
                    child = node.children[child_index - 1]
                elif self._compare(key, node.keys[child_index]) > 0:
                    child = node.children[child_index + 1]
            elif child_index == 0:
                if self._compare(key, node.keys[0]) > 0:
                    child = node.children[1]
            else:
                if self._compare(key, node.keys[child_index - 1]) <= 0:
                    child = node.children[child_index - 1]
        
        return self._delete_recursive(child, key)
    
    def _get_predecessor(self, node: BTreeNode[T]) -> T:
        """Get the predecessor of a key (rightmost key in left subtree)."""
        while not node.is_leaf:
            node = node.children[node.num_keys]
        return node.keys[node.num_keys - 1]
    
    def _get_successor(self, node: BTreeNode[T]) -> T:
        """Get the successor of a key (leftmost key in right subtree)."""
        while not node.is_leaf:
            node = node.children[0]
        return node.keys[0]
    
    def _ensure_child_has_keys(self, parent: BTreeNode[T], child_index: int) -> None:
        """Ensure a child has enough keys by borrowing from siblings or merging."""
        child = parent.children[child_index]
        left_sibling = parent.children[child_index - 1] if child_index > 0 else None
        right_sibling = parent.children[child_index + 1] if child_index < parent.num_keys else None
        
        # Try to borrow from left sibling
        if left_sibling and left_sibling.num_keys > self.min_keys:
            self._borrow_from_left_sibling(parent, child_index, left_sibling, child)
        # Try to borrow from right sibling
        elif right_sibling and right_sibling.num_keys > self.min_keys:
            self._borrow_from_right_sibling(parent, child_index, right_sibling, child)
        # Merge with left sibling
        elif left_sibling:
            self._merge_children(parent, child_index - 1)
        # Merge with right sibling
        elif right_sibling:
            self._merge_children(parent, child_index)
    
    def _borrow_from_left_sibling(self, parent: BTreeNode[T], child_index: int, 
                                 left_sibling: BTreeNode[T], child: BTreeNode[T]) -> None:
        """Borrow a key from the left sibling."""
        # Make room for the borrowed key
        for i in range(child.num_keys, 0, -1):
            child.keys[i] = child.keys[i - 1]
        if not child.is_leaf:
            for i in range(child.num_keys + 1, 0, -1):
                child.children[i] = child.children[i - 1]
        
        # Borrow the key from parent
        child.keys[0] = parent.keys[child_index - 1]
        child.num_keys += 1
        
        # Move the rightmost key from left sibling to parent
        parent.keys[child_index - 1] = left_sibling.keys[left_sibling.num_keys - 1]
        
        # Move the rightmost child from left sibling
        if not left_sibling.is_leaf:
            child.children[0] = left_sibling.children[left_sibling.num_keys]
        
        left_sibling.num_keys -= 1
    
    def _borrow_from_right_sibling(self, parent: BTreeNode[T], child_index: int,
                                  right_sibling: BTreeNode[T], child: BTreeNode[T]) -> None:
        """Borrow a key from the right sibling."""
        # Borrow the key from parent
        child.keys[child.num_keys] = parent.keys[child_index]
        child.num_keys += 1
        
        # Move the leftmost key from right sibling to parent
        parent.keys[child_index] = right_sibling.keys[0]
        
        # Move the leftmost child from right sibling
        if not right_sibling.is_leaf:
            child.children[child.num_keys] = right_sibling.children[0]
        
        # Remove the borrowed key from right sibling
        for i in range(right_sibling.num_keys - 1):
            right_sibling.keys[i] = right_sibling.keys[i + 1]
        if not right_sibling.is_leaf:
            for i in range(right_sibling.num_keys):
                right_sibling.children[i] = right_sibling.children[i + 1]
        
        right_sibling.num_keys -= 1
    
    def _merge_children(self, parent: BTreeNode[T], key_index: int) -> None:
        """Merge two children of a parent node."""
        left_child = parent.children[key_index]
        right_child = parent.children[key_index + 1]
        
        # Move the key from parent to left child
        left_child.keys[left_child.num_keys] = parent.keys[key_index]
        left_child.num_keys += 1
        
        # Move all keys and children from right child to left child
        for i in range(right_child.num_keys):
            left_child.keys[left_child.num_keys] = right_child.keys[i]
            left_child.children[left_child.num_keys + 1] = right_child.children[i]
            left_child.num_keys += 1
        
        # Move the keys from parent to left child
        for i in range(key_index, parent.num_keys - 1):
            parent.keys[i] = parent.keys[i + 1]
        
        # Move the children from parent to left child
        for i in range(key_index + 1, parent.num_keys):
            parent.children[i] = parent.children[i + 1]
        
        parent.num_keys -= 1
        
        # Remove the right child
        parent.children[key_index + 1] = None
    
    def range_query(self, start_key: T, end_key: T) -> List[T]:
        """
        Find all keys in the range [start_key, end_key].
        
        Args:
            start_key: Start of the range (inclusive)
            end_key: End of the range (inclusive)
            
        Returns:
            List of keys in the range
        """
        result = []
        if self.root is not None:
            self._range_query_recursive(self.root, start_key, end_key, result)
        return result
    
    def _range_query_recursive(self, node: BTreeNode[T], start_key: T, end_key: T, result: List[T]) -> bool:
        """
        Recursively find keys in the range [start_key, end_key].
        Returns True if should continue searching (haven't exceeded end_key).
        """
        i = 0
        
        # Find the first key >= start_key
        while i < node.num_keys and self._compare(start_key, node.keys[i]) > 0:
            i += 1
        
        if node.is_leaf:
            while i < node.num_keys and self._compare(node.keys[i], end_key) <= 0:
                result.append(node.keys[i])
                i += 1
            return i < node.num_keys  # Continue if more keys to check
        else:
            # Search in children with early termination
            while i < node.num_keys:
                if not self._range_query_recursive(node.children[i], start_key, end_key, result):
                    return False
                
                if self._compare(node.keys[i], end_key) > 0:
                    return False  # Stop searching
                
                if self._compare(node.keys[i], start_key) >= 0:
                    result.append(node.keys[i])
                
                i += 1
            
            return self._range_query_recursive(node.children[i], start_key, end_key, result)
    
    def inorder_traversal(self) -> Iterator[T]:
        """Perform an inorder traversal of the B-Tree."""
        if self.root is not None:
            yield from self._inorder_recursive(self.root)
    
    def _inorder_recursive(self, node: BTreeNode[T]) -> Iterator[T]:
        """Recursively perform inorder traversal."""
        if node.is_leaf:
            for i in range(node.num_keys):
                yield node.keys[i]
        else:
            for i in range(node.num_keys):
                yield from self._inorder_recursive(node.children[i])
                yield node.keys[i]
            yield from self._inorder_recursive(node.children[node.num_keys])
    
    def get_height(self) -> int:
        """Get the height of the B-Tree."""
        return self.height
    
    def get_memory_usage(self) -> int:
        """Calculate total memory usage of the B-Tree."""
        if self.root is None:
            return sys.getsizeof(self)
        
        total_size = sys.getsizeof(self)
        total_size += self._get_node_memory_usage(self.root)
        return total_size
    
    def _get_node_memory_usage(self, node: BTreeNode[T]) -> int:
        """Calculate memory usage of a node and its children."""
        total_size = node.get_memory_size()
        
        if not node.is_leaf and node.children:
            for i in range(node.num_keys + 1):
                if node.children[i]:
                    total_size += self._get_node_memory_usage(node.children[i])
        
        return total_size
    
    def __repr__(self) -> str:
        if self.root is None:
            return "BTree()"
        
        keys = list(self.inorder_traversal())
        return f"BTree({keys})"
    
    def __iter__(self) -> Iterator[T]:
        return self.inorder_traversal() 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running btree demonstration...")
    print("=" * 50)

    # Create instance of BTree
    try:
        instance = BTree()
        print(f"✓ Created BTree instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.insert(5)
        instance.insert(3)
        instance.insert(7)
        print(f"  After inserting elements: {instance}")
    except Exception as e:
        print(f"✗ Error creating BTree instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
