"""
Basic Union-Find (Disjoint-Set) implementation.

This module provides a basic implementation of the Union-Find data structure
without optimizations, demonstrating the core concepts.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class UnionFindNode:
    """Represents a node in the Union-Find data structure."""
    parent: int
    rank: int = 0


class DisjointSet:
    """
    A basic implementation of the Union-Find data structure.
    
    This demonstrates the core concepts behind Union-Find:
    - Forest representation of disjoint sets
    - Union and Find operations
    - Basic tree structure without optimizations
    
    Time Complexity:
    - Make Set: O(1)
    - Find: O(n) worst case
    - Union: O(n) worst case
    - Connected: O(n) worst case
    """
    
    def __init__(self) -> None:
        self.parents: Dict[int, int] = {}
        self.ranks: Dict[int, int] = {}
        self.size: int = 0
    
    def make_set(self, x: int) -> None:
        """
        Create a new set containing element x.
        
        Args:
            x: The element to create a set for
            
        Time Complexity: O(1)
        """
        if x not in self.parents:
            self.parents[x] = x
            self.ranks[x] = 0
            self.size += 1
    
    def find(self, x: int) -> int:
        """
        Find the representative (root) of the set containing x.
        
        Args:
            x: The element to find the root for
            
        Returns:
            The root element of the set containing x
            
        Raises:
            ValueError: If x is not found in any set
            
        Time Complexity: O(n) worst case
        """
        if x not in self.parents:
            raise ValueError(f"Element {x} not found in any set")
        
        # Follow parent pointers until we reach the root
        # NOTE: This basic implementation does NOT use path compression
        while self.parents[x] != x:
            x = self.parents[x]
        
        return x
    
    def union(self, x: int, y: int) -> None:
        """
        Merge the sets containing x and y.
        
        Args:
            x: First element
            y: Second element
            
        Time Complexity: O(n) worst case
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return  # Already in the same set
        
        # Attach smaller tree to larger tree (union by rank)
        if self.ranks[root_x] < self.ranks[root_y]:
            self.parents[root_x] = root_y
        elif self.ranks[root_x] > self.ranks[root_y]:
            self.parents[root_y] = root_x
        else:
            self.parents[root_y] = root_x
            self.ranks[root_x] += 1
    
    def connected(self, x: int, y: int) -> bool:
        """
        Check if x and y are in the same set.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if x and y are in the same set, False otherwise
            
        Time Complexity: O(n) worst case
        """
        return self.find(x) == self.find(y)
    
    def get_set_size(self, x: int) -> int:
        """
        Get the size of the set containing x.
        
        Args:
            x: The element to find the set size for
            
        Returns:
            The number of elements in the set containing x
            
        Time Complexity: O(n) worst case
        """
        root = self.find(x)
        return sum(1 for parent in self.parents.values() if self.find(parent) == root)
    
    def get_sets(self) -> Dict[int, List[int]]:
        """
        Get all sets as a dictionary mapping root to elements.
        
        Returns:
            Dictionary where keys are root elements and values are lists of elements in that set
            
        Time Complexity: O(n²) worst case
        """
        sets: Dict[int, List[int]] = {}
        for element in self.parents:
            root = self.find(element)
            if root not in sets:
                sets[root] = []
            sets[root].append(element)
        return sets
    
    def get_connected_components(self) -> List[List[int]]:
        """
        Get all connected components as lists of elements.
        
        Returns:
            List of lists, where each inner list represents a connected component
            
        Time Complexity: O(n²) worst case
        """
        return list(self.get_sets().values())
    
    def __len__(self) -> int:
        """Return the total number of elements in all sets."""
        return self.size
    
    def __repr__(self) -> str:
        """String representation of the DisjointSet."""
        sets = self.get_sets()
        sets_str = ", ".join(f"{{{', '.join(map(str, elements))}}}" for elements in sets.values())
        return f"DisjointSet({sets_str})"
    
    def __contains__(self, x: int) -> bool:
        """Check if element x is in any set."""
        return x in self.parents 