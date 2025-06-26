"""
Dynamic Array Implementation

This module contains implementations of dynamic arrays with different growth strategies,
from basic to production-quality versions.
"""

import sys
import timeit
from typing import TypeVar, Generic, Optional, Iterator, List, Any
from enum import Enum
import math

T = TypeVar('T')

class GrowthStrategy(Enum):
    """Different growth strategies for dynamic arrays."""
    DOUBLING = "doubling"
    FIXED = "fixed"
    GOLDEN_RATIO = "golden_ratio"
    ADAPTIVE = "adaptive"


class DynamicArray(Generic[T]):
    """
    A basic dynamic array implementation with configurable growth strategies.
    
    This demonstrates the core concepts behind dynamic arrays:
    - Dynamic resizing with different growth strategies
    - Amortized O(1) append operations
    - Memory layout and object references
    - Trade-offs between memory usage and performance
    """
    
    def __init__(self, initial_capacity: int = 8, growth_factor: float = 2.0) -> None:
        """
        Initialize a dynamic array.
        
        Args:
            initial_capacity: Starting capacity of the array
            growth_factor: Factor by which to grow when resizing
        """
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        if growth_factor <= 1.0:
            raise ValueError("Growth factor must be greater than 1.0")
        
        self._capacity = initial_capacity
        self._size = 0
        self._growth_factor = growth_factor
        self._array: List[Optional[T]] = [None] * initial_capacity
    
    def __len__(self) -> int:
        """Return the number of elements in the array."""
        return self._size
    
    def __getitem__(self, index: int) -> T:
        """Get element at index."""
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        return self._array[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """Set element at index."""
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        self._array[index] = value
    
    def append(self, value: T) -> None:
        """Add an element to the end of the array."""
        if self._size == self._capacity:
            self._resize(int(self._capacity * self._growth_factor))
        self._array[self._size] = value
        self._size += 1
    
    def insert(self, index: int, value: T) -> None:
        """Insert an element at the specified index."""
        if not 0 <= index <= self._size:
            raise IndexError("Index out of range")
        
        if self._size == self._capacity:
            self._resize(int(self._capacity * self._growth_factor))
        
        # Shift elements to make room
        for i in range(self._size, index, -1):
            self._array[i] = self._array[i - 1]
        
        self._array[index] = value
        self._size += 1
    
    def pop(self, index: Optional[int] = None) -> T:
        """Remove and return element at index (default: last element)."""
        if self._size == 0:
            raise IndexError("Cannot pop from empty array")
        
        if index is None:
            index = self._size - 1
        
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        
        value = self._array[index]
        
        # Shift elements to fill gap
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]
        
        self._size -= 1
        return value
    
    def remove(self, value: T) -> None:
        """Remove first occurrence of value."""
        for i in range(self._size):
            if self._array[i] == value:
                self.pop(i)
                return
        raise ValueError("Value not found")
    
    def _resize(self, new_capacity: int) -> None:
        """Resize the internal array to new capacity."""
        new_array: List[Optional[T]] = [None] * new_capacity
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over elements in the array."""
        for i in range(self._size):
            yield self._array[i]
    
    def __contains__(self, value: T) -> bool:
        """Check if value is in the array."""
        for item in self:
            if item == value:
                return True
        return False
    
    def __repr__(self) -> str:
        """String representation of the array."""
        return f"DynamicArray({list(self)})"
    
    @property
    def capacity(self) -> int:
        """Get the current capacity of the array."""
        return self._capacity
    
    @property
    def load_factor(self) -> float:
        """Get the current load factor (size/capacity)."""
        return self._size / self._capacity if self._capacity > 0 else 0.0


class AdvancedDynamicArray(Generic[T]):
    """
    Advanced dynamic array with multiple growth strategies and optimizations.
    
    Features:
    - Multiple growth strategies
    - Memory usage tracking
    - Performance monitoring
    - Shrink on demand
    """
    
    def __init__(self, 
                 initial_capacity: int = 8, 
                 strategy: GrowthStrategy = GrowthStrategy.DOUBLING,
                 shrink_threshold: float = 0.25) -> None:
        """
        Initialize an advanced dynamic array.
        
        Args:
            initial_capacity: Starting capacity
            strategy: Growth strategy to use
            shrink_threshold: Load factor below which to shrink
        """
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        if not 0.0 < shrink_threshold < 1.0:
            raise ValueError("Shrink threshold must be between 0 and 1")
        
        self._capacity = initial_capacity
        self._size = 0
        self._strategy = strategy
        self._shrink_threshold = shrink_threshold
        self._array: List[Optional[T]] = [None] * initial_capacity
        self._resize_count = 0
        self._total_elements_added = 0
    
    def _get_new_capacity(self, current_capacity: int) -> int:
        """Calculate new capacity based on growth strategy."""
        if self._strategy == GrowthStrategy.DOUBLING:
            return current_capacity * 2
        elif self._strategy == GrowthStrategy.FIXED:
            return current_capacity + 10
        elif self._strategy == GrowthStrategy.GOLDEN_RATIO:
            return int(current_capacity * 1.618)
        elif self._strategy == GrowthStrategy.ADAPTIVE:
            # Adaptive: use doubling for small arrays, golden ratio for large
            if current_capacity < 1000:
                return current_capacity * 2
            else:
                return int(current_capacity * 1.618)
        else:
            raise ValueError(f"Unknown growth strategy: {self._strategy}")
    
    def append(self, value: T) -> None:
        """Add an element to the end of the array."""
        if self._size == self._capacity:
            self._resize(self._get_new_capacity(self._capacity))
        
        self._array[self._size] = value
        self._size += 1
        self._total_elements_added += 1
    
    def _resize(self, new_capacity: int) -> None:
        """Resize the internal array to new capacity."""
        new_array: List[Optional[T]] = [None] * new_capacity
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity
        self._resize_count += 1
    
    def shrink_to_fit(self) -> None:
        """Shrink the array to fit the current size."""
        if self._size < self._capacity * self._shrink_threshold:
            new_capacity = max(self._size, 8)  # Minimum capacity of 8
            self._resize(new_capacity)
    
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
    
    def __iter__(self) -> Iterator[T]:
        for i in range(self._size):
            yield self._array[i]
    
    def __repr__(self) -> str:
        return f"AdvancedDynamicArray({list(self)})"
    
    @property
    def capacity(self) -> int:
        return self._capacity
    
    @property
    def load_factor(self) -> float:
        return self._size / self._capacity if self._capacity > 0 else 0.0
    
    @property
    def resize_count(self) -> int:
        return self._resize_count
    
    @property
    def memory_efficiency(self) -> float:
        """Calculate memory efficiency (size/capacity)."""
        return self._size / self._capacity if self._capacity > 0 else 0.0

    def pop(self, index: Optional[int] = None) -> T:
        """Remove and return element at index (default: last element)."""
        if self._size == 0:
            raise IndexError("Cannot pop from empty array")
        
        if index is None:
            index = self._size - 1
        
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        
        value = self._array[index]
        
        # Shift elements to fill gap
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]
        
        self._size -= 1
        return value


class ProductionDynamicArray(Generic[T]):
    """
    Production-quality dynamic array implementation.
    
    Features:
    - Multiple growth strategies
    - Memory usage optimization
    - Performance monitoring
    - Comprehensive error handling
    - Type safety with generics
    """
    
    def __init__(self, 
                 initial_capacity: int = 8, 
                 strategy: GrowthStrategy = GrowthStrategy.DOUBLING,
                 shrink_threshold: float = 0.25,
                 min_capacity: int = 8) -> None:
        """
        Initialize a production dynamic array.
        
        Args:
            initial_capacity: Starting capacity (must be positive)
            strategy: Growth strategy to use
            shrink_threshold: Load factor below which to shrink
            min_capacity: Minimum capacity after shrinking
        """
        if initial_capacity <= 0:
            raise ValueError("Initial capacity must be positive")
        if not 0.0 < shrink_threshold < 1.0:
            raise ValueError("Shrink threshold must be between 0 and 1")
        if min_capacity <= 0:
            raise ValueError("Minimum capacity must be positive")
        
        self._capacity = initial_capacity
        self._size = 0
        self._strategy = strategy
        self._shrink_threshold = shrink_threshold
        self._min_capacity = min_capacity
        self._array: List[Optional[T]] = [None] * initial_capacity
        
        # Performance tracking
        self._resize_count = 0
        self._total_elements_added = 0
        self._total_elements_removed = 0
    
    def __len__(self) -> int:
        """Return the number of elements in the array."""
        return self._size
    
    def __getitem__(self, index: int) -> T:
        """Get element at index with bounds checking."""
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range for array of size {self._size}")
        return self._array[index]
    
    def __setitem__(self, index: int, value: T) -> None:
        """Set element at index with bounds checking."""
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range for array of size {self._size}")
        self._array[index] = value
    
    def append(self, value: T) -> None:
        """Add an element to the end of the array."""
        if self._size == self._capacity:
            self._resize(self._get_new_capacity(self._capacity))
        
        self._array[self._size] = value
        self._size += 1
        self._total_elements_added += 1
    
    def insert(self, index: int, value: T) -> None:
        """Insert an element at the specified index."""
        if not 0 <= index <= self._size:
            raise IndexError(f"Index {index} out of range for insertion")
        
        if self._size == self._capacity:
            self._resize(self._get_new_capacity(self._capacity))
        
        # Shift elements to make room
        for i in range(self._size, index, -1):
            self._array[i] = self._array[i - 1]
        
        self._array[index] = value
        self._size += 1
        self._total_elements_added += 1
    
    def pop(self, index: Optional[int] = None) -> T:
        """Remove and return element at index (default: last element)."""
        if self._size == 0:
            raise IndexError("Cannot pop from empty array")
        
        if index is None:
            index = self._size - 1
        
        if not 0 <= index < self._size:
            raise IndexError(f"Index {index} out of range for array of size {self._size}")
        
        value = self._array[index]
        
        # Shift elements to fill gap
        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]
        
        self._size -= 1
        self._total_elements_removed += 1
        
        # Consider shrinking if load factor is too low
        if self._size < self._capacity * self._shrink_threshold:
            self._shrink_to_fit()
        
        return value
    
    def remove(self, value: T) -> None:
        """Remove first occurrence of value."""
        for i in range(self._size):
            if self._array[i] == value:
                self.pop(i)
                return
        raise ValueError(f"Value {value} not found in array")
    
    def clear(self) -> None:
        """Remove all elements from the array."""
        self._array = [None] * self._min_capacity
        self._capacity = self._min_capacity
        self._size = 0
    
    def extend(self, iterable: Iterator[T]) -> None:
        """Extend array with elements from iterable."""
        for item in iterable:
            self.append(item)
    
    def index(self, value: T, start: int = 0, end: Optional[int] = None) -> int:
        """Return index of first occurrence of value."""
        if end is None:
            end = self._size
        
        if not 0 <= start <= end <= self._size:
            raise ValueError("Invalid start/end indices")
        
        for i in range(start, end):
            if self._array[i] == value:
                return i
        
        raise ValueError(f"Value {value} not found in array")
    
    def count(self, value: T) -> int:
        """Return number of occurrences of value."""
        count = 0
        for item in self:
            if item == value:
                count += 1
        return count
    
    def reverse(self) -> None:
        """Reverse the array in place."""
        for i in range(self._size // 2):
            self._array[i], self._array[self._size - 1 - i] = \
                self._array[self._size - 1 - i], self._array[i]
    
    def _get_new_capacity(self, current_capacity: int) -> int:
        """Calculate new capacity based on growth strategy."""
        if self._strategy == GrowthStrategy.DOUBLING:
            return current_capacity * 2
        elif self._strategy == GrowthStrategy.FIXED:
            return current_capacity + 10
        elif self._strategy == GrowthStrategy.GOLDEN_RATIO:
            return int(current_capacity * 1.618)
        elif self._strategy == GrowthStrategy.ADAPTIVE:
            # Adaptive: use doubling for small arrays, golden ratio for large
            if current_capacity < 1000:
                return current_capacity * 2
            else:
                return int(current_capacity * 1.618)
        else:
            raise ValueError(f"Unknown growth strategy: {self._strategy}")
    
    def _resize(self, new_capacity: int) -> None:
        """Resize the internal array to new capacity."""
        new_array: List[Optional[T]] = [None] * new_capacity
        for i in range(self._size):
            new_array[i] = self._array[i]
        self._array = new_array
        self._capacity = new_capacity
        self._resize_count += 1
    
    def _shrink_to_fit(self) -> None:
        """Shrink the array to fit the current size."""
        new_capacity = max(self._size, self._min_capacity)
        if new_capacity < self._capacity:
            self._resize(new_capacity)
    
    def __iter__(self) -> Iterator[T]:
        """Iterate over elements in the array."""
        for i in range(self._size):
            yield self._array[i]
    
    def __contains__(self, value: T) -> bool:
        """Check if value is in the array."""
        for item in self:
            if item == value:
                return True
        return False
    
    def __repr__(self) -> str:
        """String representation of the array."""
        return f"ProductionDynamicArray({list(self)})"
    
    # Properties for monitoring
    @property
    def capacity(self) -> int:
        """Get the current capacity of the array."""
        return self._capacity
    
    @property
    def load_factor(self) -> float:
        """Get the current load factor (size/capacity)."""
        return self._size / self._capacity if self._capacity > 0 else 0.0
    
    @property
    def resize_count(self) -> int:
        """Get the number of times the array has been resized."""
        return self._resize_count
    
    @property
    def memory_efficiency(self) -> float:
        """Calculate memory efficiency (size/capacity)."""
        return self._size / self._capacity if self._capacity > 0 else 0.0
    
    @property
    def stats(self) -> dict:
        """Get performance statistics."""
        return {
            'size': self._size,
            'capacity': self._capacity,
            'load_factor': self.load_factor,
            'resize_count': self._resize_count,
            'total_added': self._total_elements_added,
            'total_removed': self._total_elements_removed,
            'strategy': self._strategy.value
        } 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running dynamic_array demonstration...")
    print("=" * 50)

    # Create instance of GrowthStrategy
    try:
        instance = GrowthStrategy()
        print(f"✓ Created GrowthStrategy instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating GrowthStrategy instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
