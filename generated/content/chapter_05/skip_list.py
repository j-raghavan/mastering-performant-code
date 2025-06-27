"""
Core skip list implementation.

This module provides the fundamental skip list data structure with
probabilistic height determination and efficient search, insertion,
and deletion operations.
"""

import random
import time
from typing import TypeVar, Generic, Optional, List, Iterator
from dataclasses import dataclass
from collections import defaultdict

T = TypeVar('T')

@dataclass
class SkipListNode(Generic[T]):
    """
    A node in a skip list.
    
    Each node contains:
    - data: The actual value stored in the node
    - forward: List of forward pointers for each level
    - height: The number of levels this node participates in
    """
    data: T
    forward: List[Optional['SkipListNode[T]']]
    height: int
    
    def __post_init__(self):
        """Ensure forward list has correct length."""
        if len(self.forward) != self.height:
            self.forward = [None] * self.height
    
    def __repr__(self) -> str:
        return f"SkipListNode({self.data}, height={self.height})"

class SkipList(Generic[T]):
    """
    A probabilistic skip list implementation.
    
    Skip lists provide O(log n) average-case performance for search,
    insertion, and deletion operations while being much simpler to
    implement than balanced binary search trees.
    
    Key features:
    - Probabilistic height determination using coin flips
    - Multiple levels for fast traversal
    - Simple insertion and deletion algorithms
    - Range query support
    """
    
    def __init__(self, max_height: int = 16, probability: float = 0.5):
        """
        Initialize a skip list.
        
        Args:
            max_height: Maximum height for any node
            probability: Probability of increasing height (default 0.5)
        """
        self.max_height = max_height
        self.probability = probability
        self.head = SkipListNode[T](None, [None] * max_height, max_height)
        self.size = 0
        self.current_max_height = 1
    
    def _random_height(self) -> int:
        """
        Generate a random height using coin flips.
        
        Returns:
            A random height between 1 and max_height
        """
        height = 1
        while (random.random() < self.probability and 
               height < self.max_height):
            height += 1
        return height
    
    def _find_path(self, target: T) -> List[Optional[SkipListNode[T]]]:
        """
        Find the search path to a target value.
        
        This method returns a list of nodes that are the last nodes
        visited at each level during the search. This path is used
        for both search and insertion operations.
        
        Args:
            target: The value to search for
            
        Returns:
            List of nodes representing the search path
        """
        path = [None] * self.max_height
        current = self.head
        
        # Start from the highest level and work down
        for level in range(self.current_max_height - 1, -1, -1):
            while (current.forward[level] is not None and 
                   current.forward[level].data < target):
                current = current.forward[level]
            path[level] = current
        
        # Fill any remaining levels with the head node
        for level in range(self.current_max_height, self.max_height):
            path[level] = self.head
        
        return path
    
    def search(self, target: T) -> Optional[T]:
        """
        Search for a value in the skip list.
        
        Args:
            target: The value to search for
            
        Returns:
            The value if found, None otherwise
        """
        path = self._find_path(target)
        
        # Check if the next node at level 0 contains the target
        if (path[0].forward[0] is not None and 
            path[0].forward[0].data == target):
            return path[0].forward[0].data
        
        return None
    
    def insert(self, value: T) -> None:
        """
        Insert a value into the skip list.
        
        Args:
            value: The value to insert
        """
        # Check if value already exists
        if self.search(value) is not None:
            return  # Don't insert duplicates
        
        # Find the search path
        path = self._find_path(value)
        
        # Generate random height for the new node
        height = self._random_height()
        
        # Update current max height if necessary
        if height > self.current_max_height:
            self.current_max_height = height
        
        # Create new node
        new_node = SkipListNode[T](value, [None] * height, height)
        
        # Insert the node at all levels up to its height
        for level in range(height):
            new_node.forward[level] = path[level].forward[level]
            path[level].forward[level] = new_node
        
        self.size += 1
    
    def delete(self, target: T) -> bool:
        """
        Delete a value from the skip list.
        
        Args:
            target: The value to delete
            
        Returns:
            True if the value was found and deleted, False otherwise
        """
        path = self._find_path(target)
        
        # Check if the target exists
        if (path[0].forward[0] is None or 
            path[0].forward[0].data != target):
            return False
        
        # Remove the node from all levels
        node_to_delete = path[0].forward[0]
        for level in range(node_to_delete.height):
            if path[level].forward[level] == node_to_delete:
                path[level].forward[level] = node_to_delete.forward[level]
        
        # Update current max height if necessary
        while (self.current_max_height > 1 and 
               self.head.forward[self.current_max_height - 1] is None):
            self.current_max_height -= 1
        
        self.size -= 1
        return True
    
    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, item: T) -> bool:
        return self.search(item) is not None
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over all values in sorted order."""
        current = self.head.forward[0]
        while current is not None:
            yield current.data
            current = current.forward[0]
    
    def range_query(self, start: T, end: T) -> Iterator[T]:
        """
        Find all values in the range [start, end).
        
        Args:
            start: Start of range (inclusive)
            end: End of range (exclusive)
            
        Yields:
            All values in the specified range
        """
        path = self._find_path(start)
        current = path[0].forward[0]
        
        while current is not None and current.data < end:
            if current.data >= start:
                yield current.data
            current = current.forward[0]
    
    def get_level_distribution(self) -> List[int]:
        """
        Get the distribution of nodes across levels.
        
        Returns:
            List where index i contains the number of nodes at level i
        """
        distribution = [0] * self.max_height
        
        current = self.head.forward[0]
        while current is not None:
            distribution[current.height - 1] += 1
            current = current.forward[0]
        
        return distribution
    
    def __repr__(self) -> str:
        items = list(self)
        return f"SkipList({items})"

class SkipListWithStats(Generic[T]):
    """
    Enhanced skip list with performance statistics and monitoring.
    
    This version tracks various metrics to help understand the
    performance characteristics and behavior of skip lists.
    """
    
    def __init__(self, max_height: int = 16, probability: float = 0.5):
        """Initialize skip list with statistics tracking."""
        self.skip_list = SkipList[T](max_height, probability)
        self.stats = {
            'searches': 0,
            'inserts': 0,
            'deletes': 0,
            'search_time': 0.0,
            'insert_time': 0.0,
            'delete_time': 0.0,
            'height_distribution': defaultdict(int)
        }
    
    def search(self, target: T) -> Optional[T]:
        """Search with timing statistics."""
        start_time = time.perf_counter()
        result = self.skip_list.search(target)
        end_time = time.perf_counter()
        
        self.stats['searches'] += 1
        self.stats['search_time'] += (end_time - start_time)
        
        return result
    
    def insert(self, value: T) -> None:
        """Insert with timing statistics."""
        start_time = time.perf_counter()
        self.skip_list.insert(value)
        end_time = time.perf_counter()
        
        self.stats['inserts'] += 1
        self.stats['insert_time'] += (end_time - start_time)
        
        # Update height distribution
        path = self.skip_list._find_path(value)
        height = self.skip_list._random_height()
        self.stats['height_distribution'][height] += 1
    
    def delete(self, target: T) -> bool:
        """Delete with timing statistics."""
        start_time = time.perf_counter()
        result = self.skip_list.delete(target)
        end_time = time.perf_counter()
        
        self.stats['deletes'] += 1
        self.stats['delete_time'] += (end_time - start_time)
        
        return result
    
    def get_stats(self) -> dict:
        """Get performance statistics."""
        stats = self.stats.copy()
        
        # Calculate averages
        if stats['searches'] > 0:
            stats['avg_search_time'] = stats['search_time'] / stats['searches']
        if stats['inserts'] > 0:
            stats['avg_insert_time'] = stats['insert_time'] / stats['inserts']
        if stats['deletes'] > 0:
            stats['avg_delete_time'] = stats['delete_time'] / stats['deletes']
        
        # Add level distribution
        level_dist = self.skip_list.get_level_distribution()
        stats['level_distribution'] = {i: count for i, count in enumerate(level_dist) if count > 0}
        
        return stats
    
    def reset_stats(self) -> None:
        """Reset all statistics."""
        self.stats = {
            'searches': 0,
            'inserts': 0,
            'deletes': 0,
            'search_time': 0.0,
            'insert_time': 0.0,
            'delete_time': 0.0,
            'height_distribution': defaultdict(int)
        }
    
    # Delegate other methods to the underlying skip list
    def __len__(self) -> int:
        return len(self.skip_list)
    
    def __contains__(self, item: T) -> bool:
        return item in self.skip_list
    
    def __iter__(self) -> Iterator[T]:
        return iter(self.skip_list)
    
    def range_query(self, start: T, end: T) -> Iterator[T]:
        return self.skip_list.range_query(start, end)
    
    def __repr__(self) -> str:
        return repr(self.skip_list) 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running skip_list demonstration...")
    print("=" * 50)

    # Create instance of SkipList
    try:
        instance = SkipList()
        print(f"✓ Created SkipList instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.append(1)
        instance.append(2)
        instance.append(3)
        print(f"  After adding elements: {instance}")
        print(f"  Length: {len(instance)}")
    except Exception as e:
        print(f"✗ Error creating SkipList instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
