"""
Dynamic Array Implementation

This module provides a simplified implementation of Python's list using dynamic arrays.
It demonstrates the core concepts behind Python's list implementation including
dynamic resizing, memory layout, and performance characteristics.

Theoretical Analysis:
- Dynamic arrays provide O(1) amortized append operations
- Individual resize operations are O(n) but become rare as array grows
- Growth factor of 2 ensures amortized O(1) complexity
- Memory layout is contiguous for cache efficiency

Amortized Analysis of Dynamic Array Resizing:
- Each resize doubles capacity: n → 2n
- Cost of resize: O(n) to copy elements
- Frequency: After n/2, n/4, n/8... operations
- Amortized cost per operation: O(1)

Mathematical proof:
Total cost for n operations = n + n/2 + n/4 + ... ≈ 2n = O(n)
Average cost per operation = O(n)/n = O(1)

Memory Layout:
┌─────────────────────────────────────────┐
│ [obj1][obj2][obj3][None][None][None]... │
│  ↑                    ↑                  │
│  size=3              capacity=8          │
└─────────────────────────────────────────┘
"""

import sys
from typing import TypeVar, Generic, Optional, Iterator
from .analyzer import MemoryInfo

T = TypeVar('T')

class DynamicArray(Generic[T]):
    """
    A simplified implementation of Python's list using dynamic arrays.
    
    This demonstrates the core concepts behind Python's list implementation:
    - Dynamic resizing with amortized O(1) append operations
    - Memory layout and object references
    - Growth factor strategies
    
    CPython Implementation Details:
    - Lists use a dynamic array with over-allocation
    - Growth factor is approximately 1.125 (9/8) for small lists
    - For larger lists, growth factor approaches 1.5
    - Memory layout: [PyObject* array, size, allocated]
    - Resize strategy: new_allocated = (size >> 3) + (size < 9 ? 3 : 6) + size
    """
    
    def __init__(self, initial_capacity: int = 8) -> None:
        self._capacity = initial_capacity
        self._size = 0
        self._array = [None] * initial_capacity
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, index: int) -> T:
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        return self._array[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        self._array[index] = value
    
    def append(self, value: T) -> None:
        """
        Add an element to the end of the array.
        
        Time Complexity: O(1) amortized
        - Most operations are O(1) direct array access
        - Resize operations are O(n) but become exponentially rare
        - Amortized analysis shows O(1) average case
        """
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        self._array[self._size] = value
        self._size += 1
    
    def insert(self, index: int, value: T) -> None:
        """
        Insert an element at a specific index.
        
        Time Complexity: O(n)
        - Requires shifting all elements after the insertion point
        - Worst case when inserting at beginning: O(n)
        - Best case when inserting at end: O(1) (same as append)
        """
        if not 0 <= index <= self._size:
            raise IndexError("Index out of range")
        
        if self._size == self._capacity:
            self._resize(self._capacity * 2)
        
        # Shift elements to make room
        for i in range(self._size, index, -1):
            self._array[i] = self._array[i - 1]
        
        self._array[index] = value
        self._size += 1
    
    def pop(self, index: Optional[int] = None) -> T:
        """
        Remove and return an element.
        
        Time Complexity: O(n) for arbitrary index, O(1) for end
        - Removing from end: O(1) - just decrement size
        - Removing from beginning: O(n) - shift all elements
        - Removing from middle: O(n) - shift elements after index
        """
        if index is None:
            index = self._size - 1
        
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        
        value = self._array[index]
        
        # Shift elements to fill the gap
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]
        
        self._size -= 1
        return value
    
    def _resize(self, new_capacity: int) -> None:
        """
        Resize the internal array to new capacity.
        
        This operation has O(n) complexity but is amortized to O(1) per operation
        due to the doubling strategy. The resize frequency decreases exponentially
        as the array grows.
        
        CPython's actual resize strategy is more sophisticated:
        - For small lists: new_allocated = size + (size >> 3) + 3
        - For large lists: new_allocated = size + (size >> 3) + 6
        - This results in approximately 1.125x growth for small lists
        """
        new_array = [None] * new_capacity
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity
    
    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._array[i]
    
    def __repr__(self) -> str:
        return f"DynamicArray({list(self)})"
    
    def get_capacity(self) -> int:
        """Get the current capacity of the array."""
        return self._capacity
    
    def get_load_factor(self) -> float:
        """Get the current load factor (size/capacity) of the array."""
        return self._size / self._capacity if self._capacity > 0 else 0


class MemoryTrackedDynamicArray(DynamicArray[T]):
    """
    Dynamic array with memory tracking capabilities.
    
    This enhanced version tracks:
    - Number of resizes performed
    - Total memory allocations
    - Memory usage statistics
    - Performance characteristics
    """
    
    def __init__(self, initial_capacity: int = 8) -> None:
        super().__init__(initial_capacity)
        self._resize_count = 0
        self._total_allocations = 0
        self._operation_count = 0
    
    def append(self, value: T) -> None:
        """Add an element to the end of the array with tracking."""
        self._operation_count += 1
        super().append(value)
    
    def _resize(self, new_capacity: int) -> None:
        """Resize with tracking."""
        self._resize_count += 1
        self._total_allocations += new_capacity
        super()._resize(new_capacity)
    
    def get_memory_info(self) -> 'MemoryInfo':
        """Get memory information for this array."""
        object_size = sys.getsizeof(self._array)
        total_size = sum(sys.getsizeof(item) for item in self._array if item is not None)
        overhead = object_size - (self._capacity * 8)
        
        return MemoryInfo(
            object_size=object_size,
            total_size=total_size,
            overhead=overhead,
            capacity=self._capacity,
            load_factor=self._size / self._capacity if self._capacity > 0 else 0
        )
    
    def get_statistics(self) -> dict:
        """Get performance statistics for this array."""
        return {
            'resize_count': self._resize_count,
            'total_allocations': self._total_allocations,
            'operation_count': self._operation_count,
            'average_allocations_per_operation': (self._total_allocations / self._operation_count 
                                                 if self._operation_count > 0 else 0),
            'resize_frequency': (self._resize_count / self._operation_count 
                                if self._operation_count > 0 else 0)
        } 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running dynamic_array demonstration...")
    print("=" * 50)

    # Create instance of DynamicArray
    try:
        instance = DynamicArray()
        print(f"✓ Created DynamicArray instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.append(1)
        instance.append(2)
        instance.append(3)
        print(f"  After adding elements: {instance}")
        print(f"  Length: {len(instance)}")
    except Exception as e:
        print(f"✗ Error creating DynamicArray instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
