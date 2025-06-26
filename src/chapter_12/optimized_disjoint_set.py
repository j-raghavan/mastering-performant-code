"""
Optimized Union-Find (Disjoint-Set) implementation with path compression.

This module provides an optimized implementation of the Union-Find data structure
with path compression and union by rank optimizations.
"""

from typing import Dict, List, Optional, Tuple
import sys


class OptimizedDisjointSet:
    """
    An optimized implementation of Union-Find with path compression and union by rank.
    
    This demonstrates the advanced optimizations:
    - Path compression during find operations
    - Union by rank for balanced trees
    - Amortized O(α(n)) complexity for all operations
    
    Time Complexity (amortized):
    - Make Set: O(1)
    - Find: O(α(n))
    - Union: O(α(n))
    - Connected: O(α(n))
    
    Where α(n) is the inverse Ackermann function, which grows extremely slowly.
    """
    
    def __init__(self) -> None:
        self.parents: Dict[int, int] = {}
        self.ranks: Dict[int, int] = {}
        self.sizes: Dict[int, int] = {}  # Track set sizes
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
            self.sizes[x] = 1
            self.size += 1
    
    def find(self, x: int) -> int:
        """
        Find the representative (root) of the set containing x with path compression.
        
        Args:
            x: The element to find the root for
            
        Returns:
            The root element of the set containing x
            
        Raises:
            ValueError: If x is not found in any set
            
        Time Complexity: O(α(n)) amortized
        """
        if x not in self.parents:
            raise ValueError(f"Element {x} not found in any set")
        
        # Path compression: make every node point directly to the root
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])
        
        return self.parents[x]
    
    def union(self, x: int, y: int) -> None:
        """
        Merge the sets containing x and y using union by rank.
        
        Args:
            x: First element
            y: Second element
            
        Time Complexity: O(α(n)) amortized
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return  # Already in the same set
        
        # Union by rank: attach smaller tree to larger tree
        if self.ranks[root_x] < self.ranks[root_y]:
            self.parents[root_x] = root_y
            self.sizes[root_y] += self.sizes[root_x]
        elif self.ranks[root_x] > self.ranks[root_y]:
            self.parents[root_y] = root_x
            self.sizes[root_x] += self.sizes[root_y]
        else:
            # Ranks are equal, attach one to the other and increment rank
            self.parents[root_y] = root_x
            self.ranks[root_x] += 1
            self.sizes[root_x] += self.sizes[root_y]
    
    def connected(self, x: int, y: int) -> bool:
        """
        Check if x and y are in the same set.
        
        Args:
            x: First element
            y: Second element
            
        Returns:
            True if x and y are in the same set, False otherwise
            
        Time Complexity: O(α(n)) amortized
        """
        return self.find(x) == self.find(y)
    
    def get_set_size(self, x: int) -> int:
        """
        Get the size of the set containing x.
        
        Args:
            x: The element to find the set size for
            
        Returns:
            The number of elements in the set containing x
            
        Time Complexity: O(α(n)) amortized
        """
        root = self.find(x)
        return self.sizes[root]
    
    def get_sets(self) -> Dict[int, List[int]]:
        """
        Get all sets as a dictionary mapping root to elements.
        
        Returns:
            Dictionary where keys are root elements and values are lists of elements in that set
            
        Time Complexity: O(n * α(n)) amortized
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
            
        Time Complexity: O(n * α(n)) amortized
        """
        return list(self.get_sets().values())
    
    def get_roots(self) -> List[int]:
        """
        Get all root elements (representatives of sets).
        
        Returns:
            List of root elements
            
        Time Complexity: O(n * α(n)) amortized
        """
        roots = set()
        for element in self.parents:
            roots.add(self.find(element))
        return list(roots)
    
    def get_set_elements(self, root: int) -> List[int]:
        """
        Get all elements in the set with the given root.
        
        Args:
            root: The root element of the set
            
        Returns:
            List of elements in the set
            
        Time Complexity: O(n * α(n)) amortized
        """
        elements = []
        for element in self.parents:
            if self.find(element) == root:
                elements.append(element)
        return elements
    
    def count_sets(self) -> int:
        """
        Count the number of disjoint sets.
        
        Returns:
            Number of disjoint sets
            
        Time Complexity: O(n * α(n)) amortized
        """
        return len(self.get_roots())
    
    def is_root(self, x: int) -> bool:
        """
        Check if element x is a root (representative of its set).
        
        Args:
            x: The element to check
            
        Returns:
            True if x is a root, False otherwise
            
        Time Complexity: O(α(n)) amortized
        """
        return x in self.parents and self.find(x) == x
    
    def get_rank(self, x: int) -> int:
        """
        Get the rank of element x.
        
        Args:
            x: The element to get the rank for
            
        Returns:
            The rank of element x
            
        Time Complexity: O(α(n)) amortized
        """
        root = self.find(x)
        return self.ranks[root]
    
    def __len__(self) -> int:
        """Return the total number of elements in all sets."""
        return self.size
    
    def __repr__(self) -> str:
        """String representation of the OptimizedDisjointSet."""
        sets = self.get_sets()
        sets_str = ", ".join(f"{{{', '.join(map(str, elements))}}}" for elements in sets.values())
        return f"OptimizedDisjointSet({sets_str})"
    
    def __contains__(self, x: int) -> bool:
        """Check if element x is in any set."""
        return x in self.parents 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running optimized_disjoint_set demonstration...")
    print("=" * 50)

    # Create instance of OptimizedDisjointSet
    try:
        instance = OptimizedDisjointSet()
        print(f"✓ Created OptimizedDisjointSet instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating OptimizedDisjointSet instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
