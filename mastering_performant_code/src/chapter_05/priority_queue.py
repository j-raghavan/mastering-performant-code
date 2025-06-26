"""
Priority queue implementation using skip lists.

This module provides a priority queue implementation that leverages
the efficiency of skip lists for O(log n) average-case performance
on all operations.
"""

from typing import TypeVar, Generic, Optional, Tuple, Iterator, Dict
from dataclasses import dataclass
from .skip_list import SkipList

K = TypeVar('K')  # Key type (priority)
V = TypeVar('V')  # Value type

@dataclass
class PriorityItem(Generic[K, V]):
    """An item in a priority queue with key and value."""
    key: K
    value: V
    
    def __lt__(self, other: 'PriorityItem[K, V]') -> bool:
        """Compare by key for priority ordering."""
        return self.key < other.key
    
    def __eq__(self, other: object) -> bool:
        """Check equality by key only."""
        if not isinstance(other, PriorityItem):
            return False
        return self.key == other.key
    
    def __hash__(self) -> int:
        """Hash based on key and value."""
        return hash((self.key, self.value))

class SkipListPriorityQueue(Generic[K, V]):
    """
    A priority queue implementation using skip lists.
    
    This implementation provides O(log n) average-case performance for
    all operations while maintaining items in priority order.
    
    Advantages over heap-based priority queues:
    - O(log n) deletion of arbitrary items
    - O(log n) priority updates
    - Better performance for large datasets
    - More predictable performance characteristics
    """
    
    def __init__(self, max_height: int = 16, probability: float = 0.5):
        """Initialize the priority queue."""
        self.skip_list = SkipList[PriorityItem[K, V]](max_height, probability)
        self._item_map: Dict[V, PriorityItem[K, V]] = {}
    
    def put(self, key: K, value: V) -> None:
        """
        Add an item to the priority queue.
        
        Args:
            key: Priority key (lower values = higher priority)
            value: The value to store
        """
        item = PriorityItem(key, value)
        
        # If value already exists, remove old item
        if value in self._item_map:
            old_item = self._item_map[value]
            self.skip_list.delete(old_item)
        
        # Add new item
        self.skip_list.insert(item)
        self._item_map[value] = item
    
    def get(self) -> Tuple[K, V]:
        """
        Remove and return the highest priority item.
        
        Returns:
            Tuple of (key, value) for the highest priority item
            
        Raises:
            IndexError: If the queue is empty
        """
        if len(self.skip_list) == 0:
            raise IndexError("Priority queue is empty")
        
        # Get the first item (lowest key = highest priority)
        first_item = next(iter(self.skip_list))
        
        # Remove from skip list and item map
        self.skip_list.delete(first_item)
        del self._item_map[first_item.value]
        
        return first_item.key, first_item.value
    
    def peek(self) -> Tuple[K, V]:
        """
        Return the highest priority item without removing it.
        
        Returns:
            Tuple of (key, value) for the highest priority item
            
        Raises:
            IndexError: If the queue is empty
        """
        if len(self.skip_list) == 0:
            raise IndexError("Priority queue is empty")
        
        first_item = next(iter(self.skip_list))
        return first_item.key, first_item.value
    
    def remove(self, value: V) -> bool:
        """
        Remove a specific value from the priority queue.
        
        Args:
            value: The value to remove
            
        Returns:
            True if the value was found and removed, False otherwise
        """
        if value not in self._item_map:
            return False
        
        item = self._item_map[value]
        self.skip_list.delete(item)
        del self._item_map[value]
        return True
    
    def update_priority(self, value: V, new_key: K) -> bool:
        """
        Update the priority of an existing value.
        
        Args:
            value: The value whose priority to update
            new_key: The new priority key
            
        Returns:
            True if the value was found and updated, False otherwise
        """
        if value not in self._item_map:
            return False
        
        self.put(new_key, value)
        return True
    
    def __len__(self) -> int:
        return len(self.skip_list)
    
    def __contains__(self, value: V) -> bool:
        return value in self._item_map
    
    def __iter__(self) -> Iterator[Tuple[K, V]]:
        """Iterate over all items in priority order."""
        for item in self.skip_list:
            yield item.key, item.value
    
    def get_priority(self, value: V) -> Optional[K]:
        """Get the priority of a specific value."""
        if value in self._item_map:
            return self._item_map[value].key
        return None
    
    def __repr__(self) -> str:
        items = [f"({k}, {repr(v)})" for k, v in self]
        return f"SkipListPriorityQueue([{', '.join(items)}])" 




def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running priority_queue demonstration...")
    print("=" * 50)

    # Create instance of PriorityItem
    try:
        instance = PriorityItem()
        print(f"✓ Created PriorityItem instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating PriorityItem instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
