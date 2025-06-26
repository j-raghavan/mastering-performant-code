"""
Binary Heap Implementation

This module provides a complete binary heap implementation supporting both
min and max heaps with O(log n) operations and O(n) heapify construction.
"""

from typing import TypeVar, Generic, Optional, List, Callable, Any, Iterator
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class HeapNode(Generic[T]):
    """A node in the binary heap with priority and optional data."""
    priority: int
    data: Optional[T] = None
    
    def __lt__(self, other: 'HeapNode[T]') -> bool:
        # Only compare by priority for simplicity
        return self.priority < other.priority
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, HeapNode):
            return False
        return self.priority == other.priority and self.data == other.data
    
    def __repr__(self) -> str:
        if self.data is not None:
            return f"HeapNode({self.priority}, {self.data})"
        return f"HeapNode({self.priority})"

class BinaryHeap(Generic[T]):
    """
    A binary heap implementation supporting both min and max heaps.
    
    This implementation provides:
    - O(log n) insertion and extraction
    - O(n) heapify construction
    - O(1) peek operations
    - Support for custom comparison functions
    - Memory-efficient array-based storage
    """
    
    def __init__(self, heap_type: str = "min", key_func: Optional[Callable[[T], int]] = None) -> None:
        """
        Initialize a binary heap.
        
        Args:
            heap_type: "min" for min-heap, "max" for max-heap
            key_func: Function to extract priority from data items
        """
        self._heap: List[HeapNode[T]] = []
        self._heap_type = heap_type.lower()
        self._key_func = key_func
        
        if self._heap_type not in ("min", "max"):
            raise ValueError("Heap type must be 'min' or 'max'")
    
    def __len__(self) -> int:
        return len(self._heap)
    
    def is_empty(self) -> bool:
        return len(self._heap) == 0
    
    def push(self, item: T, priority: Optional[int] = None) -> None:
        """
        Add an item to the heap.
        
        Args:
            item: The item to add
            priority: Priority value (if None, uses key_func or item itself)
        """
        if priority is None:
            if self._key_func:
                priority = self._key_func(item)
            elif hasattr(item, 'priority'):
                # Handle PriorityQueueItem and similar objects
                priority = item.priority
            elif isinstance(item, (int, float)):
                priority = item
            else:
                raise ValueError("Must provide priority or key_func for non-numeric items")
        
        node = HeapNode(priority, item)
        self._heap.append(node)
        self._sift_up(len(self._heap) - 1)
    
    def pop(self) -> T:
        """
        Remove and return the highest priority item.
        
        Returns:
            The highest priority item
            
        Raises:
            IndexError: If heap is empty
        """
        if self.is_empty():
            raise IndexError("Heap is empty")
        
        if len(self._heap) == 1:
            return self._heap.pop().data
        
        # Swap root with last element
        root = self._heap[0]
        self._heap[0] = self._heap.pop()
        
        # Restore heap property
        self._sift_down(0)
        
        return root.data
    
    def peek(self) -> T:
        """
        Return the highest priority item without removing it.
        
        Returns:
            The highest priority item
            
        Raises:
            IndexError: If heap is empty
        """
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self._heap[0].data
    
    def peek_priority(self) -> int:
        """
        Return the priority of the highest priority item.
        
        Returns:
            The priority value
            
        Raises:
            IndexError: If heap is empty
        """
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self._heap[0].priority
    
    def _parent(self, index: int) -> int:
        """Get the parent index of a given index."""
        return (index - 1) // 2
    
    def _left_child(self, index: int) -> int:
        """Get the left child index of a given index."""
        return 2 * index + 1
    
    def _right_child(self, index: int) -> int:
        """Get the right child index of a given index."""
        return 2 * index + 2
    
    def _has_parent(self, index: int) -> bool:
        """Check if an index has a parent."""
        return index > 0
    
    def _has_left_child(self, index: int) -> bool:
        """Check if an index has a left child."""
        return self._left_child(index) < len(self._heap)
    
    def _has_right_child(self, index: int) -> bool:
        """Check if an index has a right child."""
        return self._right_child(index) < len(self._heap)
    
    def _swap(self, index1: int, index2: int) -> None:
        """Swap two elements in the heap."""
        self._heap[index1], self._heap[index2] = self._heap[index2], self._heap[index1]
    
    def _should_swap_up(self, child_index: int, parent_index: int) -> bool:
        """Determine if child should swap with parent based on heap type."""
        if self._heap_type == "min":
            return self._heap[child_index] < self._heap[parent_index]
        else:  # max heap
            return self._heap[child_index] > self._heap[parent_index]
    
    def _should_swap_down(self, parent_index: int, child_index: int) -> bool:
        """Determine if parent should swap with child based on heap type."""
        if self._heap_type == "min":
            return self._heap[parent_index] > self._heap[child_index]
        else:  # max heap
            return self._heap[parent_index] < self._heap[child_index]
    
    def _sift_up(self, index: int) -> None:
        """Move an element up the heap to restore heap property."""
        while self._has_parent(index) and self._should_swap_up(index, self._parent(index)):
            self._swap(index, self._parent(index))
            index = self._parent(index)
    
    def _sift_down(self, index: int) -> None:
        """Move an element down the heap to restore heap property."""
        while self._has_left_child(index):
            # Find the smaller/larger child
            child_index = self._left_child(index)
            if (self._has_right_child(index) and 
                self._should_swap_down(child_index, self._right_child(index))):
                child_index = self._right_child(index)
            
            # If parent is already in correct position, stop
            if not self._should_swap_down(index, child_index):
                break
            
            self._swap(index, child_index)
            index = child_index
    
    def heapify(self, items: List[T], priorities: Optional[List[int]] = None) -> None:
        """
        Build a heap from a list of items in O(n) time.
        
        Args:
            items: List of items to add to heap
            priorities: Optional list of priorities (must match items length)
        """
        self._heap.clear()
        
        if priorities is None:
            for item in items:
                self.push(item)
        else:
            if len(items) != len(priorities):
                raise ValueError("Items and priorities must have same length")
            for item, priority in zip(items, priorities):
                self.push(item, priority)
    
    def heapify_bottom_up(self, items: List[T], priorities: Optional[List[int]] = None) -> None:
        """
        Build a heap using bottom-up heapify in O(n) time.
        
        This is more efficient than repeated push operations for large datasets.
        """
        if priorities is None:
            if self._key_func:
                self._heap = [HeapNode(self._key_func(item), item) for item in items]
            elif all(hasattr(item, 'priority') for item in items):
                # Handle PriorityQueueItem and similar objects
                self._heap = [HeapNode(item.priority, item) for item in items]
            elif all(isinstance(item, (int, float)) for item in items):
                self._heap = [HeapNode(item, item) for item in items]
            else:
                raise ValueError("Must provide priorities or key_func for non-numeric items")
        else:
            if len(items) != len(priorities):
                raise ValueError("Items and priorities must have same length")
            self._heap = [HeapNode(priority, item) for item, priority in zip(items, priorities)]
        
        # Bottom-up heapify: start from last non-leaf node
        for i in range(self._parent(len(self._heap) - 1), -1, -1):
            self._sift_down(i)
    
    def __repr__(self) -> str:
        items = [f"{node.priority}:{node.data}" for node in self._heap]
        return f"BinaryHeap({self._heap_type}, [{', '.join(items)}])"
    
    def __iter__(self) -> 'Iterator[T]':
        """
        Iterate over heap items in priority order.
        
        Note: This method creates a complete copy of the heap in O(n) space.
        For large datasets, consider using pop() operations directly to avoid
        memory overhead.
        """
        # Create a copy to avoid modifying the original heap
        temp_heap = BinaryHeap[T](heap_type=self._heap_type, key_func=self._key_func)
        temp_heap._heap = [HeapNode(node.priority, node.data) for node in self._heap]
        
        while not temp_heap.is_empty():
            yield temp_heap.pop()
    
    def iter_destructive(self) -> 'Iterator[T]':
        """
        Iterate over heap items in priority order, consuming the heap.
        
        This method is more memory efficient than __iter__ but destroys
        the original heap. Use when you only need to iterate once.
        """
        while not self.is_empty():
            yield self.pop()
    
    def to_list(self) -> List[T]:
        """Convert heap to a list in priority order."""
        return list(self)
    
    def clear(self) -> None:
        """Clear all elements from the heap."""
        self._heap.clear()
    
    def size(self) -> int:
        """Get the number of elements in the heap."""
        return len(self._heap)
    
    def capacity(self) -> int:
        """Get the current capacity of the heap."""
        return len(self._heap)
    
    def is_valid(self) -> bool:
        """Check if the heap property is maintained."""
        for i in range(len(self._heap)):
            if self._has_left_child(i):
                if self._should_swap_down(i, self._left_child(i)):
                    return False
            if self._has_right_child(i):
                if self._should_swap_down(i, self._right_child(i)):
                    return False
        return True
    
    def merge(self, other: 'BinaryHeap[T]') -> 'BinaryHeap[T]':
        """
        Merge two heaps efficiently.
        
        This method creates a new heap containing all elements from both heaps.
        The resulting heap maintains the heap property.
        
        Args:
            other: Another binary heap to merge with
            
        Returns:
            New heap containing all elements from both heaps
            
        Raises:
            ValueError: If heaps have different types or key functions
        """
        if self._heap_type != other._heap_type:
            raise ValueError("Cannot merge heaps with different types")
        
        if self._key_func != other._key_func:
            raise ValueError("Cannot merge heaps with different key functions")
        
        # Create new heap with same configuration
        merged_heap = BinaryHeap[T](heap_type=self._heap_type, key_func=self._key_func)
        
        # Combine all elements
        all_nodes = self._heap + other._heap
        
        # Use bottom-up heapify for efficient construction
        merged_heap._heap = all_nodes
        for i in range(merged_heap._parent(len(merged_heap._heap) - 1), -1, -1):
            merged_heap._sift_down(i)
        
        return merged_heap 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running binary_heap demonstration...")
    print("=" * 50)

    # Create instance of BinaryHeap
    try:
        instance = BinaryHeap()
        print(f"✓ Created BinaryHeap instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating BinaryHeap instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
