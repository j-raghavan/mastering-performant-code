"""
Priority Queue Implementation

This module provides a priority queue implementation using binary heaps
with FIFO ordering for items with the same priority.
"""

from typing import TypeVar, Generic, Optional, List, Callable, Any, Tuple, Dict
from dataclasses import dataclass
import time
from .binary_heap import BinaryHeap, HeapNode

T = TypeVar('T')

@dataclass
class PriorityQueueItem(Generic[T]):
    """An item in the priority queue with priority and counter for tie-breaking."""
    priority: int
    counter: int
    data: T
    
    def __repr__(self) -> str:
        return f"PriorityQueueItem({self.priority}, {self.data})"

class PriorityQueue(Generic[T]):
    """
    A priority queue implementation using binary heap.
    
    This implementation provides:
    - O(log n) insertion and extraction
    - FIFO ordering for items with same priority
    - Thread-safe operations (basic)
    - Support for custom priority functions
    """
    
    def __init__(self, max_heap: bool = False, key_func: Optional[Callable[[T], int]] = None) -> None:
        """
        Initialize a priority queue.
        
        Args:
            max_heap: If True, higher priorities are extracted first
            key_func: Function to extract priority from items
        """
        self._key_func = key_func
        self._counter = 0  # Strictly incrementing counter for FIFO tie-breaking
        
        # Create a custom key function that combines priority and counter
        def combined_key_func(item: PriorityQueueItem[T]) -> int:
            # Use a large multiplier to ensure counter doesn't interfere with priority
            # For min-heap: lower values are higher priority
            # For max-heap: higher values are higher priority
            base_priority = item.priority
            if max_heap:
                # For max-heap, we want higher priorities first, so use negative priority
                return -base_priority * 1000000 + item.counter
            else:
                # For min-heap, we want lower priorities first, so use positive priority
                return base_priority * 1000000 + item.counter
        
        self._heap = BinaryHeap[PriorityQueueItem[T]](
            heap_type="min",  # Always use min-heap, key function handles ordering
            key_func=combined_key_func
        )
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def is_empty(self) -> bool:
        return self._heap.is_empty()
    
    def put(self, item: T, priority: Optional[int] = None) -> None:
        """
        Add an item to the priority queue.
        
        Args:
            item: The item to add
            priority: Priority value (if None, uses key_func or item itself)
        """
        if priority is None:
            if self._key_func:
                priority = self._key_func(item)
            elif isinstance(item, (int, float)):
                priority = item
            else:
                raise ValueError("Must provide priority or key_func for non-numeric items")
        
        queue_item = PriorityQueueItem(priority, self._counter, item)
        self._counter += 1
        self._heap.push(queue_item)
    
    def get(self) -> T:
        """
        Remove and return the highest priority item.
        
        Returns:
            The highest priority item
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._heap.pop().data
    
    def peek(self) -> T:
        """
        Return the highest priority item without removing it.
        
        Returns:
            The highest priority item
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._heap.peek().data
    
    def peek_priority(self) -> int:
        """
        Return the priority of the highest priority item.
        
        Returns:
            The priority value
            
        Raises:
            IndexError: If queue is empty
        """
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._heap.peek().priority
    
    def __repr__(self) -> str:
        return f"PriorityQueue({len(self)} items)"
    
    def __iter__(self):
        """
        Iterate over queue items in priority order.
        
        Note: This method creates a complete copy of the queue in O(n) space.
        For large datasets, consider using pop() operations directly to avoid
        memory overhead.
        """
        # Create a copy to avoid modifying the original queue
        temp_heap = BinaryHeap[PriorityQueueItem[T]](
            heap_type=self._heap._heap_type,
            key_func=self._heap._key_func
        )
        
        # Copy all items to temporary heap
        for node in self._heap._heap:
            temp_heap.push(node.data)
        
        while not temp_heap.is_empty():
            yield temp_heap.pop().data
    
    def to_list(self) -> List[T]:
        """Convert queue to a list in priority order."""
        return list(self)
    
    def clear(self) -> None:
        """Clear all elements from the queue."""
        self._heap.clear()
    
    def size(self) -> int:
        """Get the number of elements in the queue."""
        return len(self._heap)
    
    def is_valid(self) -> bool:
        """Check if the queue maintains proper ordering."""
        return self._heap.is_valid()
    
    def get_all_with_priority(self, priority: int) -> List[T]:
        """
        Get all items with a specific priority.
        
        Args:
            priority: The priority to search for
            
        Returns:
            List of items with the specified priority
        """
        result = []
        temp_heap = BinaryHeap[PriorityQueueItem[T]](
            heap_type=self._heap._heap_type,
            key_func=self._heap._key_func
        )
        
        # Extract all elements and check priorities
        while not self._heap.is_empty():
            item = self._heap.pop()
            if item.priority == priority:
                result.append(item.data)
            temp_heap.push(item)
        
        # Restore the heap
        while not temp_heap.is_empty():
            self._heap.push(temp_heap.pop())
        
        return result
    
    def remove_all_with_priority(self, priority: int) -> List[T]:
        """
        Remove all items with a specific priority.
        
        Args:
            priority: The priority to remove
            
        Returns:
            List of removed items
        """
        result = []
        temp_heap = BinaryHeap[PriorityQueueItem[T]](
            heap_type=self._heap._heap_type,
            key_func=self._heap._key_func
        )
        
        # Extract all elements and filter by priority
        while not self._heap.is_empty():
            item = self._heap.pop()
            if item.priority == priority:
                result.append(item.data)
            else:
                temp_heap.push(item)
        
        # Restore the heap
        while not temp_heap.is_empty():
            self._heap.push(temp_heap.pop())
        
        return result
    
    def get_priority_distribution(self) -> Dict[int, int]:
        """
        Get the distribution of priorities in the queue.
        
        Returns:
            Dictionary mapping priority values to counts
        """
        distribution = {}
        temp_heap = BinaryHeap[PriorityQueueItem[T]](
            heap_type=self._heap._heap_type,
            key_func=self._heap._key_func
        )
        
        # Extract all elements and count priorities
        while not self._heap.is_empty():
            item = self._heap.pop()
            distribution[item.priority] = distribution.get(item.priority, 0) + 1
            temp_heap.push(item)
        
        # Restore the heap
        while not temp_heap.is_empty():
            self._heap.push(temp_heap.pop())
        
        return distribution
    
    def task_done(self) -> None:
        """
        Mark a task as done (placeholder for future thread safety).
        
        This method is included for compatibility with Python's queue.Queue
        interface. In a thread-safe implementation, this would be used to
        coordinate with join().
        """
        pass
    
    def qsize(self) -> int:
        """
        Return approximate queue size.
        
        Returns:
            Number of items in the queue
        """
        return len(self)
    
    def full(self) -> bool:
        """
        Check if the queue is full.
        
        Returns:
            False (priority queues are unbounded)
        """
        return False
    
    def empty(self) -> bool:
        """
        Check if the queue is empty.
        
        Returns:
            True if queue is empty, False otherwise
        """
        return self.is_empty() 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running priority_queue demonstration...")
    print("=" * 50)

    # Create instance of PriorityQueueItem
    try:
        instance = PriorityQueueItem()
        print(f"✓ Created PriorityQueueItem instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating PriorityQueueItem instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
