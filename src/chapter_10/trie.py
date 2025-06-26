"""
Standard Trie Implementation

This module provides a production-quality trie implementation for string storage
and retrieval with comprehensive functionality and error handling.
"""

import sys
from typing import TypeVar, Generic, Optional, Iterator, List, Dict, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

T = TypeVar('T')

@dataclass
class TrieNode:
    """
    A node in the trie data structure.
    
    Attributes:
        char: The character stored at this node (None for root)
        is_end: Whether this node marks the end of a word
        value: Optional value associated with this node
        children: Dictionary mapping characters to child nodes
    """
    char: Optional[str] = None
    is_end: bool = False
    value: Optional[T] = None
    children: Dict[str, 'TrieNode'] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize the node after creation."""
        if self.children is None:
            self.children = {}

class Trie(Generic[T]):
    """
    A production-quality trie implementation for string storage and retrieval.
    
    This trie supports:
    - Unicode string storage and retrieval
    - Prefix-based searches and autocomplete
    - Key-value storage
    - Memory-efficient operations
    - Comprehensive error handling
    
    Time Complexity:
    - Insert: O(m) where m is string length
    - Search: O(m) where m is string length
    - Prefix search: O(m + k) where k is number of matches
    - Delete: O(m) where m is string length
    
    Space Complexity:
    - O(n × m × σ) where n is number of strings, m is average length, σ is alphabet size
    """
    
    def __init__(self) -> None:
        """Initialize an empty trie."""
        self._root = TrieNode()
        self._size = 0
    
    def __len__(self) -> int:
        """Return the number of strings stored in the trie."""
        return self._size
    
    def __contains__(self, key: str) -> bool:
        """Check if a string is stored in the trie."""
        node = self._find_node(key)
        return node is not None and node.is_end
    
    def __getitem__(self, key: str) -> T:
        """Get the value associated with a key."""
        node = self._find_node(key)
        if node is None or not node.is_end:
            raise KeyError(f"Key '{key}' not found in trie")
        return node.value
    
    def __setitem__(self, key: str, value: T) -> None:
        """Set the value associated with a key."""
        self.insert(key, value)
    
    def __delitem__(self, key: str) -> None:
        """Remove a key from the trie."""
        self.delete(key)
    
    def insert(self, key: str, value: Optional[T] = None) -> None:
        """
        Insert a string into the trie.
        
        Args:
            key: The string to insert
            value: Optional value to associate with the key
            
        Raises:
            ValueError: If key is empty or None
        """
        if not key:
            raise ValueError("Cannot insert empty string")
        
        node = self._root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode(char=char)
            node = node.children[char]
        
        if not node.is_end:
            self._size += 1
        
        node.is_end = True
        node.value = value
    
    def search(self, key: str) -> Optional[T]:
        """
        Search for a string in the trie.
        
        Args:
            key: The string to search for
            
        Returns:
            The value associated with the key, or None if not found
        """
        node = self._find_node(key)
        return node.value if node and node.is_end else None
    
    def starts_with(self, prefix: str) -> bool:
        """
        Check if any string in the trie starts with the given prefix.
        
        Args:
            prefix: The prefix to search for
            
        Returns:
            True if any string starts with the prefix, False otherwise
        """
        return self._find_node(prefix) is not None
    
    def get_all_with_prefix(self, prefix: str) -> List[Tuple[str, T]]:
        """
        Get all strings that start with the given prefix.
        
        Args:
            prefix: The prefix to search for
            
        Returns:
            List of (string, value) tuples for all matching strings
        """
        results = []
        node = self._find_node(prefix)
        
        if node is not None:
            self._collect_words(node, prefix, results)
        
        return results
    
    def autocomplete(self, prefix: str, max_results: int = 10) -> List[str]:
        """
        Get autocomplete suggestions for a prefix.
        
        Args:
            prefix: The prefix to autocomplete
            max_results: Maximum number of suggestions to return
            
        Returns:
            List of autocomplete suggestions
        """
        suggestions = []
        node = self._find_node(prefix)
        
        if node is not None:
            self._collect_words(node, prefix, suggestions, max_results)
        
        # Return just the strings, not the tuples
        return [s for s, _ in suggestions[:max_results]]
    
    def delete(self, key: str) -> bool:
        """
        Delete a string from the trie.
        
        Args:
            key: The string to delete
            
        Returns:
            True if the string was deleted, False if it wasn't found
        """
        if not key:
            return False
        
        # Find the path to the key
        path = []
        node = self._root
        
        for char in key:
            if char not in node.children:
                return False
            path.append((node, char))
            node = node.children[char]
        
        if not node.is_end:
            return False
        
        # Mark as not end of word
        node.is_end = False
        node.value = None
        self._size -= 1
        
        # Remove unnecessary nodes
        self._cleanup_path(path, key)
        
        return True
    
    def longest_common_prefix(self) -> str:
        """
        Find the longest common prefix of all strings in the trie.
        
        Returns:
            The longest common prefix
        """
        if self._size == 0:
            return ""
        
        prefix = []
        node = self._root
        
        while len(node.children) == 1 and not node.is_end:
            char = next(iter(node.children))
            prefix.append(char)
            node = node.children[char]
        
        return "".join(prefix)
    
    def get_all_strings(self) -> List[Tuple[str, T]]:
        """
        Get all strings stored in the trie.
        
        Returns:
            List of (string, value) tuples for all stored strings
        """
        return self.get_all_with_prefix("")
    
    def _find_node(self, key: str) -> Optional[TrieNode]:
        """Find the node corresponding to a key."""
        if not key:
            return self._root
        
        node = self._root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node
    
    def _collect_words(self, node: TrieNode, prefix: str, 
                      results: List, max_results: Optional[int] = None) -> None:
        """Collect all words starting from a given node."""
        if node.is_end:
            results.append((prefix, node.value))
            if max_results and len(results) >= max_results:
                return
        
        for char, child in node.children.items():
            if max_results and len(results) >= max_results:
                break
            self._collect_words(child, prefix + char, results, max_results)
    
    def _cleanup_path(self, path: List[Tuple[TrieNode, str]], key: str) -> None:
        """Remove unnecessary nodes after deletion."""
        for node, char in reversed(path):
            child = node.children[char]
            if not child.is_end and len(child.children) == 0:
                del node.children[char]
            else:
                break
    
    def __repr__(self) -> str:
        """String representation of the trie."""
        strings = [f"'{s}'" for s, _ in self.get_all_strings()]
        return f"Trie({', '.join(strings)})" 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running trie demonstration...")
    print("=" * 50)

    # Create instance of Trie
    try:
        instance = Trie()
        print(f"✓ Created Trie instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating Trie instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
