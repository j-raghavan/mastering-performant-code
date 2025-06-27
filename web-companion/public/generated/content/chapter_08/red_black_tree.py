"""
Red-Black Tree Implementation

This module provides a complete implementation of Red-Black trees,
including the core data structure, performance analysis, and validation functions.

Classes:
    - Color: Enumeration for node colors
    - RedBlackNode: Node implementation for Red-Black trees
    - RedBlackTree: Complete Red-Black tree implementation

Functions:
    - red_black_height_analysis: Analyze height bounds
    - benchmark_red_black_tree_operations: Performance benchmarking
    - analyze_red_black_properties: Property validation
"""

from typing import TypeVar, Generic, Optional, Iterator, Dict
from enum import Enum
import timeit
import sys
T = TypeVar('T')

class Color(Enum):
    """Enumeration for node colors in Red-Black tree."""
    RED = "RED"
    BLACK = "BLACK"

class RedBlackNode(Generic[T]):
    """
    A node in a Red-Black tree.
    
    Each node contains:
    - key: The value stored in the node
    - color: RED or BLACK
    - left, right: References to child nodes
    - parent: Reference to parent node
    """
    
    def __init__(self, key: T, color: Color = Color.RED) -> None:
        self.key = key
        self.color = color
        self.left: Optional['RedBlackNode[T]'] = None
        self.right: Optional['RedBlackNode[T]'] = None
        self.parent: Optional['RedBlackNode[T]'] = None
    
    def __repr__(self) -> str:
        return f"RedBlackNode({self.key}, {self.color.value})"
    
    def is_red(self) -> bool:
        """Check if the node is red."""
        return self.color == Color.RED
    
    def is_black(self) -> bool:
        """Check if the node is black."""
        return self.color == Color.BLACK
    
    def set_red(self) -> None:
        """Set the node color to red."""
        self.color = Color.RED
    
    def set_black(self) -> None:
        """Set the node color to black."""
        self.color = Color.BLACK
    
    def get_sibling(self) -> Optional['RedBlackNode[T]']:
        """Get the sibling of this node."""
        if self.parent is None:
            return None
        
        if self.parent.left == self:
            return self.parent.right
        else:
            return self.parent.left
    
    def get_uncle(self) -> Optional['RedBlackNode[T]']:
        """Get the uncle of this node (parent's sibling)."""
        if self.parent is None or self.parent.parent is None:
            return None
        
        return self.parent.get_sibling()

class RedBlackTree(Generic[T]):
    """
    A Red-Black tree implementation.
    
    This tree maintains the five Red-Black properties:
    1. Every node is either red or black
    2. The root is always black
    3. All leaves (NIL) are black
    4. Red nodes cannot have red children
    5. Every path from root to leaves has the same number of black nodes
    
    This guarantees O(log n) performance for all operations.
    
    Thread Safety:
    This implementation is not thread-safe. For concurrent access,
    external synchronization (e.g., locks) must be used. Consider
    using threading.Lock or threading.RLock for multi-threaded applications.
    """
    
    def __init__(self) -> None:
        self.root: Optional[RedBlackNode[T]] = None
        self._size = 0
    
    def __len__(self) -> int:
        return self._size
    
    def is_empty(self) -> bool:
        """Check if the tree is empty."""
        return self.root is None
    
    def insert(self, key: T) -> None:
        """
        Insert a key into the Red-Black tree.
        
        Args:
            key: The key to insert
            
        Time Complexity: O(log n)
        """
        if key is None:
            raise ValueError("Cannot insert None key")
        
        node = RedBlackNode(key)
        
        # Perform standard BST insertion
        self._bst_insert(node)
        
        # Fix Red-Black properties
        self._fix_insert(node)
        
        self._size += 1
    
    def _bst_insert(self, node: RedBlackNode[T]) -> None:
        """Perform standard BST insertion."""
        if self.root is None:
            self.root = node
            return
        
        current = self.root
        parent = None
        
        while current is not None:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                current = current.right
        
        node.parent = parent
        if node.key < parent.key:
            parent.left = node
        else:
            parent.right = node
    
    def _fix_insert(self, node: RedBlackNode[T]) -> None:
        """Fix Red-Black properties after insertion."""
        # Case 1: node is root
        if node.parent is None:
            node.set_black()
            return
        
        # Case 2: parent is black
        if node.parent.is_black():
            return
        
        # Case 3: parent is red
        uncle = node.get_uncle()
        
        if uncle is not None and uncle.is_red():
            # Case 3a: uncle is red
            self._fix_red_uncle(node)
        else:
            # Case 3b: uncle is black or None
            self._fix_black_uncle(node)
    
    def _fix_red_uncle(self, node: RedBlackNode[T]) -> None:
        """Fix case where uncle is red."""
        parent = node.parent
        grandparent = parent.parent
        uncle = node.get_uncle()
        
        # Recolor
        parent.set_black()
        uncle.set_black()
        grandparent.set_red()
        
        # Recursively fix grandparent
        self._fix_insert(grandparent)
    
    def _fix_black_uncle(self, node: RedBlackNode[T]) -> None:
        """Fix case where uncle is black or None."""
        parent = node.parent
        grandparent = parent.parent
        
        # Determine if we need to rotate
        if parent == grandparent.left:
            if node == parent.right:
                # Left-Right case
                self._left_rotate(parent)
                node = parent
                parent = node.parent
            
            # Left-Left case
            self._right_rotate(grandparent)
        else:
            if node == parent.left:
                # Right-Left case
                self._right_rotate(parent)
                node = parent
                parent = node.parent
            
            # Right-Right case
            self._left_rotate(grandparent)
        
        # Recolor
        parent.set_black()
        grandparent.set_red()
    
    def _left_rotate(self, node: RedBlackNode[T]) -> None:
        """Perform left rotation around node."""
        right_child = node.right
        if right_child is None:
            return
        
        # Update parent pointers
        node.right = right_child.left
        if right_child.left is not None:
            right_child.left.parent = node
        
        right_child.parent = node.parent
        
        # Update root if necessary
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        
        # Complete rotation
        right_child.left = node
        node.parent = right_child
    
    def _right_rotate(self, node: RedBlackNode[T]) -> None:
        """Perform right rotation around node."""
        left_child = node.left
        if left_child is None:
            return
        
        # Update parent pointers
        node.left = left_child.right
        if left_child.right is not None:
            left_child.right.parent = node
        
        left_child.parent = node.parent
        
        # Update root if necessary
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        
        # Complete rotation
        left_child.right = node
        node.parent = left_child
    
    def search(self, key: T) -> Optional[RedBlackNode[T]]:
        """
        Search for a key in the Red-Black tree.
        
        Args:
            key: The key to search for
            
        Returns:
            The node containing the key, or None if not found
            
        Time Complexity: O(log n)
        """
        if key is None:
            return None
        
        return self._search_recursive(self.root, key)
    
    def _search_recursive(self, node: Optional[RedBlackNode[T]], key: T) -> Optional[RedBlackNode[T]]:
        """Recursively search for a key."""
        if node is None or node.key == key:
            return node
        
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)
    
    def delete(self, key: T) -> bool:
        """
        Delete a key from the Red-Black tree.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was found and deleted, False otherwise
            
        Time Complexity: O(log n)
        """
        if key is None:
            return False
        
        node = self.search(key)
        if node is None:
            return False
        
        self._delete_node(node)
        self._size -= 1
        return True
    
    def _delete_node(self, node: RedBlackNode[T]) -> None:
        """Delete a node from the tree."""
        # Find the node to actually delete
        if node.left is not None and node.right is not None:
            # Node has two children - find successor
            successor = self._find_successor(node)
            node.key = successor.key
            node = successor
        
        # Node has at most one child
        child = node.left if node.left is not None else node.right
        
        if node.is_black():
            if child is None:
                # Node is black with no children
                self._fix_delete_double_black(node)
            else:
                # Node is black with one red child
                child.set_black()
        
        # Replace node with child
        if node.parent is None:
            self.root = child
        elif node == node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child
        
        if child is not None:
            child.parent = node.parent
    
    def _find_successor(self, node: RedBlackNode[T]) -> RedBlackNode[T]:
        """Find the successor of a node."""
        if node.right is not None:
            # Successor is the leftmost node in right subtree
            current = node.right
            while current.left is not None:
                current = current.left
            return current
        
        # Successor is the first ancestor whose left child is also an ancestor
        current = node
        while current.parent is not None and current == current.parent.right:
            current = current.parent
        return current.parent
    
    def _fix_delete_double_black(self, node: RedBlackNode[T]) -> None:
        """Fix double-black violation after deletion."""
        if node.parent is None:
            return
        
        sibling = node.get_sibling()
        if sibling is None:
            return
        
        if sibling.is_red():
            # Case 1: Sibling is red
            self._fix_red_sibling(node, sibling)
        else:
            # Case 2: Sibling is black
            self._fix_black_sibling(node, sibling)
    
    def _fix_red_sibling(self, node: RedBlackNode[T], sibling: RedBlackNode[T]) -> None:
        """Fix case where sibling is red."""
        parent = node.parent
        sibling.set_black()
        parent.set_red()
        
        if node == parent.left:
            self._left_rotate(parent)
        else:
            self._right_rotate(parent)
        
        # Continue fixing with new sibling
        new_sibling = node.get_sibling()
        if new_sibling is not None:
            self._fix_black_sibling(node, new_sibling)
    
    def _fix_black_sibling(self, node: RedBlackNode[T], sibling: RedBlackNode[T]) -> None:
        """Fix case where sibling is black."""
        parent = node.parent
        
        # Check if sibling's children are black
        left_nephew_black = sibling.left is None or sibling.left.is_black()
        right_nephew_black = sibling.right is None or sibling.right.is_black()
        
        if left_nephew_black and right_nephew_black:
            # Case 2a: Both nephews are black
            sibling.set_red()
            if parent.is_red():
                parent.set_black()
            else:
                self._fix_delete_double_black(parent)
        else:
            # Case 2b: At least one nephew is red
            self._fix_red_nephew(node, sibling, left_nephew_black, right_nephew_black)
    
    def _fix_red_nephew(self, node: RedBlackNode[T], sibling: RedBlackNode[T], 
                       left_nephew_black: bool, right_nephew_black: bool) -> None:
        """Fix case where at least one nephew is red."""
        parent = node.parent
        
        if node == parent.left:
            if right_nephew_black:
                # Case 2b(i): Right nephew is black, left nephew is red
                if sibling.left is not None:
                    sibling.left.set_black()
                sibling.set_red()
                self._right_rotate(sibling)
                sibling = parent.right
            
            # Case 2b(ii): Right nephew is red
            if sibling.right is not None:
                sibling.right.set_black()
            sibling.color = parent.color
            parent.set_black()
            self._left_rotate(parent)
        else:
            if left_nephew_black:
                # Case 2b(i): Left nephew is black, right nephew is red
                if sibling.right is not None:
                    sibling.right.set_black()
                sibling.set_red()
                self._left_rotate(sibling)
                sibling = parent.left
            
            # Case 2b(ii): Left nephew is red
            if sibling.left is not None:
                sibling.left.set_black()
            sibling.color = parent.color
            parent.set_black()
            self._right_rotate(parent)
    
    def find_min(self) -> Optional[T]:
        """Find the minimum key in the tree."""
        if self.root is None:
            return None
        
        current = self.root
        while current.left is not None:
            current = current.left
        return current.key
    
    def find_max(self) -> Optional[T]:
        """Find the maximum key in the tree."""
        if self.root is None:
            return None
        
        current = self.root
        while current.right is not None:
            current = current.right
        return current.key
    
    def inorder_traversal(self) -> Iterator[T]:
        """Perform inorder traversal of the tree."""
        def _inorder(node: Optional[RedBlackNode[T]]) -> Iterator[T]:
            if node is not None:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)
        
        yield from _inorder(self.root)
    
    def preorder_traversal(self) -> Iterator[T]:
        """Perform preorder traversal of the tree."""
        def _preorder(node: Optional[RedBlackNode[T]]) -> Iterator[T]:
            if node is not None:
                yield node.key
                yield from _preorder(node.left)
                yield from _preorder(node.right)
        
        yield from _preorder(self.root)
    
    def postorder_traversal(self) -> Iterator[T]:
        """Perform postorder traversal of the tree."""
        def _postorder(node: Optional[RedBlackNode[T]]) -> Iterator[T]:
            if node is not None:
                yield from _postorder(node.left)
                yield from _postorder(node.right)
                yield node.key
        
        yield from _postorder(self.root)
    
    def level_order_traversal(self) -> Iterator[list[T]]:
        """Perform level-order traversal of the tree."""
        if self.root is None:
            return
        
        queue = [self.root]
        while queue:
            level_size = len(queue)
            level = []
            
            for _ in range(level_size):
                node = queue.pop(0)
                level.append(node.key)
                
                if node.left is not None:
                    queue.append(node.left)
                if node.right is not None:
                    queue.append(node.right)
            
            yield level
    
    def height(self) -> int:
        """Calculate the height of the tree."""
        def _height(node: Optional[RedBlackNode[T]]) -> int:
            if node is None:
                return -1  # Standard definition: empty tree has height -1
            return 1 + max(_height(node.left), _height(node.right))
        
        return _height(self.root)
    
    def black_height(self) -> int:
        """Calculate the black height of the tree."""
        if self.root is None:
            return 0
        
        def _black_height(node: Optional[RedBlackNode[T]]) -> int:
            if node is None:
                return 0  # Don't count NIL nodes
            left_bh = _black_height(node.left)
            right_bh = _black_height(node.right)
            if left_bh != right_bh:
                raise ValueError("Invalid Red-Black tree: unequal black heights")
            return left_bh + (1 if node.is_black() else 0)
        
        return _black_height(self.root)
    
    def is_valid(self) -> bool:
        """Check if the tree satisfies all Red-Black properties."""
        if self.root is None:
            return True
        
        # Property 2: Root is black
        if self.root.is_red():
            return False
        
        try:
            # Check all paths have same black height
            black_height = self._get_black_height(self.root)
            return self._check_properties(self.root, black_height, 0)
        except ValueError:
            # Black heights are unequal
            return False
    
    def _get_black_height(self, node: Optional[RedBlackNode[T]]) -> int:
        """Get the black height from a node to any leaf."""
        if node is None:
            return 0  # Don't count NIL nodes
        left_bh = self._get_black_height(node.left)
        right_bh = self._get_black_height(node.right)
        if left_bh != right_bh:
            raise ValueError("Invalid Red-Black tree: unequal black heights")
        return left_bh + (1 if node.is_black() else 0)
    
    def _check_properties(self, node: Optional[RedBlackNode[T]], 
                         expected_black_height: int, current_black_height: int) -> bool:
        """Check Red-Black properties recursively."""
        if node is None:
            return current_black_height == expected_black_height
        
        # Property 4: No two consecutive red nodes
        if node.is_red():
            if (node.left is not None and node.left.is_red()) or \
               (node.right is not None and node.right.is_red()):
                return False
        
        # Update black height
        new_black_height = current_black_height + (1 if node.is_black() else 0)
        
        # Check left and right subtrees
        return (self._check_properties(node.left, expected_black_height, new_black_height) and
                self._check_properties(node.right, expected_black_height, new_black_height))
    
    def __repr__(self) -> str:
        return f"RedBlackTree(size={self._size}, height={self.height()})"

def red_black_height_analysis(n: int) -> Dict[str, float]:
    """
    Analyze Red-Black tree height bounds.
    
    Args:
        n: Number of nodes in the Red-Black tree
        
    Returns:
        Dictionary containing height analysis
    """
    # Calculate theoretical bounds
    min_black_height = (n + 1).bit_length() - 1
    max_black_height = n  # Worst case: all nodes black in a chain
    
    # Red-Black height bound
    rb_height_bound = 2 * (n + 1).bit_length() - 2
    
    # AVL height bound for comparison
    avl_height_bound = int(1.44 * (n + 2).bit_length() - 0.328)
    
    # Perfect binary tree height
    perfect_height = (n + 1).bit_length() - 1
    
    return {
        'nodes': n,
        'min_black_height': min_black_height,
        'max_black_height': max_black_height,
        'rb_height_bound': rb_height_bound,
        'avl_height_bound': avl_height_bound,
        'perfect_height': perfect_height,
        'rb_vs_avl_ratio': rb_height_bound / avl_height_bound if avl_height_bound > 0 else 0,
        'rb_vs_perfect_ratio': rb_height_bound / perfect_height if perfect_height > 0 else 0
    }

def benchmark_red_black_tree_operations():
    """
    Benchmark Red-Black tree operations against built-in data structures.
    
    This demonstrates the performance characteristics of Red-Black trees
    and compares them with Python's built-in sorted data structures.
    """
    
    def benchmark_insertion():
        """Benchmark insertion operations."""
        print("=== Insertion Benchmark ===")
        
        # Test data
        test_sizes = [100, 1000, 10000]
        
        for size in test_sizes:
            print(f"\nSize: {size}")
            
            # Red-Black tree insertion
            rb_tree = RedBlackTree[int]()
            rb_time = timeit.timeit(
                lambda: [rb_tree.insert(i) for i in range(size)],
                number=1
            )
            print(f"Red-Black Tree: {rb_time:.6f}s")
            
            # List insertion (for comparison)
            list_time = timeit.timeit(
                lambda: [i for i in range(size)],
                number=1
            )
            print(f"List: {list_time:.6f}s")
            
            # Sorted list insertion
            sorted_list = []
            sorted_time = timeit.timeit(
                lambda: sorted_list.extend(range(size)),
                number=1
            )
            print(f"Sorted List: {sorted_time:.6f}s")
    
    def benchmark_search():
        """Benchmark search operations."""
        print("\n=== Search Benchmark ===")
        
        # Prepare test data
        size = 10000
        rb_tree = RedBlackTree[int]()
        for i in range(size):
            rb_tree.insert(i)
        
        # Red-Black tree search
        rb_time = timeit.timeit(
            lambda: [rb_tree.search(i) for i in range(0, size, 100)],
            number=100
        )
        print(f"Red-Black Tree Search: {rb_time:.6f}s")
        
        # List search (for comparison)
        test_list = list(range(size))
        list_time = timeit.timeit(
            lambda: [i in test_list for i in range(0, size, 100)],
            number=100
        )
        print(f"List Search: {list_time:.6f}s")
    
    def benchmark_deletion():
        """Benchmark deletion operations."""
        print("\n=== Deletion Benchmark ===")
        
        # Prepare test data
        size = 1000
        rb_tree = RedBlackTree[int]()
        for i in range(size):
            rb_tree.insert(i)
        
        # Red-Black tree deletion
        rb_time = timeit.timeit(
            lambda: [rb_tree.delete(i) for i in range(0, size, 2)],
            number=1
        )
        print(f"Red-Black Tree Deletion: {rb_time:.6f}s")
    
    def benchmark_memory_usage():
        """Benchmark memory usage."""
        print("\n=== Memory Usage Benchmark ===")
        
                # Test different data structures
        test_size = 10000
        
        # Red-Black tree
        rb_tree = RedBlackTree[int]()
        for i in range(test_size):
            rb_tree.insert(i)
        rb_memory = sys.getsizeof(rb_tree) + sum(sys.getsizeof(node) for node in rb_tree.inorder_traversal())
        
        # List
        test_list = list(range(test_size))
        list_memory = sys.getsizeof(test_list) + sum(sys.getsizeof(i) for i in test_list)
        
        # Dictionary
        test_dict = {i: i for i in range(test_size)}
        dict_memory = sys.getsizeof(test_dict)
        
        print(f"Red-Black Tree Memory: {rb_memory:,} bytes")
        print(f"List Memory: {list_memory:,} bytes")
        print(f"Dictionary Memory: {dict_memory:,} bytes")
        print(f"RB Tree vs List ratio: {rb_memory/list_memory:.2f}")
        print(f"RB Tree vs Dict ratio: {rb_memory/dict_memory:.2f}")
    
    def compare_with_builtin_dict():
        """Compare Red-Black tree performance with dict."""
        print("\n=== Comparison with Built-in Dict ===")
        
        test_size = 10000
        
        # Red-Black tree operations
        rb_tree = RedBlackTree[int]()
        rb_insert_time = timeit.timeit(
            lambda: [rb_tree.insert(i) for i in range(test_size)],
            number=1
        )
        rb_search_time = timeit.timeit(
            lambda: [rb_tree.search(i) for i in range(0, test_size, 10)],
            number=100
        )
        
        # Dict operations
        test_dict = {}
        dict_insert_time = timeit.timeit(
            lambda: [test_dict.__setitem__(i, i) for i in range(test_size)],
            number=1
        )
        dict_search_time = timeit.timeit(
            lambda: [test_dict.get(i) for i in range(0, test_size, 10)],
            number=100
        )
        
        print(f"Insertion - RB Tree: {rb_insert_time:.6f}s, Dict: {dict_insert_time:.6f}s")
        print(f"Search - RB Tree: {rb_search_time:.6f}s, Dict: {dict_search_time:.6f}s")
        print(f"Insertion ratio (RB/Dict): {rb_insert_time/dict_insert_time:.2f}")
        print(f"Search ratio (RB/Dict): {rb_search_time/dict_search_time:.2f}")
    
    # Run all benchmarks
    benchmark_insertion()
    benchmark_search()
    benchmark_deletion()
    benchmark_memory_usage()
    compare_with_builtin_dict()

def analyze_red_black_properties():
    """
    Analyze Red-Black tree properties and validate the implementation.
    """
    print("=== Red-Black Tree Property Analysis ===")
    
    # Test tree construction
    rb_tree = RedBlackTree[int]()
    test_data = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    
    print(f"Inserting test data: {test_data}")
    for key in test_data:
        rb_tree.insert(key)
    
    print(f"Tree size: {len(rb_tree)}")
    print(f"Tree height: {rb_tree.height()}")
    print(f"Black height: {rb_tree.black_height()}")
    print(f"Is valid Red-Black tree: {rb_tree.is_valid()}")
    
    # Test traversals
    print(f"\nInorder traversal: {list(rb_tree.inorder_traversal())}")
    print(f"Preorder traversal: {list(rb_tree.preorder_traversal())}")
    print(f"Postorder traversal: {list(rb_tree.postorder_traversal())}")
    
    # Test search operations
    print(f"\nSearch for 50: {rb_tree.search(50) is not None}")
    print(f"Search for 100: {rb_tree.search(100) is not None}")
    print(f"Minimum: {rb_tree.find_min()}")
    print(f"Maximum: {rb_tree.find_max()}")
    
    # Test deletion
    print(f"\nDeleting 30: {rb_tree.delete(30)}")
    print(f"Tree size after deletion: {len(rb_tree)}")
    print(f"Is valid after deletion: {rb_tree.is_valid()}")
    
    # Height analysis
    print(f"\n=== Height Analysis ===")
    for n in [10, 100, 1000, 10000]:
        analysis = red_black_height_analysis(n)
        print(f"Nodes: {n}, Height Bound: {analysis['rb_height_bound']}, "
              f"AVL Bound: {analysis['avl_height_bound']}, "
              f"Ratio: {analysis['rb_vs_avl_ratio']:.2f}")

if __name__ == "__main__":
    # Run benchmarks and analysis
    benchmark_red_black_tree_operations()
    analyze_red_black_properties() 