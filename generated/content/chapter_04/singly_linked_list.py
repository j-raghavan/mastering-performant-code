"""
Singly linked list implementation with sentinel nodes.

This module provides a production-quality implementation of a singly linked list
with sentinel nodes to simplify edge cases and improve code clarity.
"""

from typing import TypeVar, Generic, Optional, Iterator, List
from .nodes import SinglyNode
import sys

T = TypeVar('T')

class SinglyLinkedList(Generic[T]):
    """
    A singly linked list implementation with sentinel nodes.
    
    This implementation uses sentinel nodes to simplify edge cases:
    - head_sentinel: Dummy node before the first actual element
    - tail_sentinel: Dummy node after the last actual element
    
    This eliminates special cases for empty lists and boundary operations.
    
    Attributes:
        _head_sentinel: Sentinel node at the beginning of the list
        _tail_sentinel: Sentinel node at the end of the list
        _size: Number of elements in the list
    """
    
    def __init__(self) -> None:
        """Initialize an empty singly linked list with sentinel nodes."""
        self._head_sentinel = SinglyNode(None)  # type: ignore
        self._tail_sentinel = SinglyNode(None)  # type: ignore
        self._head_sentinel.next = self._tail_sentinel
        self._size = 0
    
    def __len__(self) -> int:
        """Return the number of elements in the list."""
        return self._size
    
    def is_empty(self) -> bool:
        """Check if the list is empty."""
        return self._size == 0
    
    def append(self, data: T) -> None:
        """
        Add an element to the end of the list.
        
        Args:
            data: The data to append to the list
        """
        new_node = SinglyNode(data)
        
        # Find the last node (before tail sentinel)
        current = self._head_sentinel
        while current.next != self._tail_sentinel:
            current = current.next
        
        # Insert new node before tail sentinel
        new_node.next = self._tail_sentinel
        current.next = new_node
        self._size += 1
    
    def prepend(self, data: T) -> None:
        """
        Add an element to the beginning of the list.
        
        Args:
            data: The data to prepend to the list
        """
        new_node = SinglyNode(data)
        new_node.next = self._head_sentinel.next
        self._head_sentinel.next = new_node
        self._size += 1
    
    def insert_after(self, target_data: T, new_data: T) -> bool:
        """
        Insert new_data after the first occurrence of target_data.
        
        Args:
            target_data: The data to search for
            new_data: The data to insert
            
        Returns:
            True if insertion was successful, False if target_data was not found
        """
        current = self._head_sentinel.next
        
        while current != self._tail_sentinel:
            if current.data == target_data:
                new_node = SinglyNode(new_data)
                new_node.next = current.next
                current.next = new_node
                self._size += 1
                return True
            current = current.next
        
        return False
    
    def delete_first(self, data: T) -> bool:
        """
        Delete the first occurrence of data from the list.
        
        Args:
            data: The data to delete
            
        Returns:
            True if deletion was successful, False if data was not found
        """
        current = self._head_sentinel
        
        while current.next != self._tail_sentinel:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def get_at_index(self, index: int) -> T:
        """
        Get the element at the specified index.
        
        Args:
            index: The index of the element to retrieve
            
        Returns:
            The element at the specified index
            
        Raises:
            IndexError: If index is out of range
        """
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        
        current = self._head_sentinel.next
        for _ in range(index):
            current = current.next
        
        return current.data
    
    def set_at_index(self, index: int, data: T) -> None:
        """
        Set the element at the specified index.
        
        Args:
            index: The index of the element to set
            data: The new data to store at the index
            
        Raises:
            IndexError: If index is out of range
        """
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        
        current = self._head_sentinel.next
        for _ in range(index):
            current = current.next
        
        current.data = data
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over the list elements."""
        current = self._head_sentinel.next
        while current != self._tail_sentinel:
            yield current.data
            current = current.next
    
    def __repr__(self) -> str:
        """Return a string representation of the list."""
        elements = list(self)
        return f"SinglyLinkedList({elements})"
    
    def to_list(self) -> List[T]:
        """Convert the linked list to a Python list."""
        return list(self)
    
    def reverse(self) -> None:
        """Reverse the linked list in-place."""
        if self._size <= 1:
            return
        
        prev = self._head_sentinel
        current = self._head_sentinel.next
        next_node = current.next
        
        # Reverse the links
        while current != self._tail_sentinel:
            current.next = prev
            prev = current
            current = next_node
            next_node = current.next if current != self._tail_sentinel else None
        
        # Update sentinel connections
        self._head_sentinel.next.next = self._tail_sentinel
        self._head_sentinel.next = prev
    
    def contains(self, data: T) -> bool:
        """
        Check if the list contains the specified data.
        
        Args:
            data: The data to search for
            
        Returns:
            True if the data is found, False otherwise
        """
        current = self._head_sentinel.next
        while current != self._tail_sentinel:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def count(self, data: T) -> int:
        """
        Count the number of occurrences of the specified data.
        
        Args:
            data: The data to count
            
        Returns:
            The number of occurrences of the data
        """
        count = 0
        current = self._head_sentinel.next
        while current != self._tail_sentinel:
            if current.data == data:
                count += 1
            current = current.next
        return count
    
    def clear(self) -> None:
        """Remove all elements from the list."""
        self._head_sentinel.next = self._tail_sentinel
        self._size = 0
    
    def get_memory_usage(self) -> int:
        """
        Calculate the total memory usage of the list including all nodes.
        
        Returns:
            Total memory usage in bytes
        """
                # Base object size
        total_size = sys.getsizeof(self)
        
        # Add size of sentinel nodes
        total_size += sys.getsizeof(self._head_sentinel)
        total_size += sys.getsizeof(self._tail_sentinel)
        
        # Add size of all data nodes
        current = self._head_sentinel.next
        while current != self._tail_sentinel:
            total_size += sys.getsizeof(current)
            current = current.next
        
        return total_size 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running singly_linked_list demonstration...")
    print("=" * 50)

    # Create instance of SinglyLinkedList
    try:
        instance = SinglyLinkedList()
        print(f"✓ Created SinglyLinkedList instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.append(1)
        instance.append(2)
        instance.append(3)
        print(f"  After adding elements: {instance}")
        print(f"  Length: {len(instance)}")
    except Exception as e:
        print(f"✗ Error creating SinglyLinkedList instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
