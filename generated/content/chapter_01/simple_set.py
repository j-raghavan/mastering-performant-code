"""
Simple Set Implementation

This module provides a simplified implementation of Python's set using hash tables.
It demonstrates the core concepts behind Python's set implementation including
hash table with open addressing, set operations, and memory efficiency.
"""

from typing import TypeVar, Generic, Iterator, Set as PySet, Optional
from .hash_table import HashTable

T = TypeVar('T')

class SimpleSet(Generic[T]):
    """
    A simplified implementation of Python's set using hash tables.
    
    This demonstrates the core concepts behind Python's set implementation:
    - Hash table with open addressing (similar to dict)
    - Only keys, no values
    - Set operations (union, intersection, difference)
    """
    
    def __init__(self, iterable: Optional[PySet[T]] = None) -> None:
        self._hash_table = HashTable[T, bool]()
        if iterable:
            for item in iterable:
                self.add(item)
    
    def __len__(self) -> int:
        return len(self._hash_table)
    
    def __contains__(self, item: T) -> bool:
        return item in self._hash_table
    
    def add(self, item: T) -> None:
        """Add an item to the set."""
        self._hash_table[item] = True
    
    def remove(self, item: T) -> None:
        """Remove an item from the set."""
        del self._hash_table[item]
    
    def discard(self, item: T) -> None:
        """Remove an item from the set if present."""
        try:
            del self._hash_table[item]
        except KeyError:
            pass
    
    def __iter__(self) -> Iterator[T]:
        return iter(self._hash_table)
    
    def __repr__(self) -> str:
        items = [repr(item) for item in self]
        return f"SimpleSet({{{', '.join(items)}}})"
    
    def union(self, other: 'SimpleSet[T]') -> 'SimpleSet[T]':
        """Return the union of two sets."""
        result = SimpleSet(self)
        for item in other:
            result.add(item)
        return result
    
    def intersection(self, other: 'SimpleSet[T]') -> 'SimpleSet[T]':
        """Return the intersection of two sets."""
        result = SimpleSet()
        for item in self:
            if item in other:
                result.add(item)
        return result
    
    def difference(self, other: 'SimpleSet[T]') -> 'SimpleSet[T]':
        """Return the difference of two sets."""
        result = SimpleSet()
        for item in self:
            if item not in other:
                result.add(item)
        return result 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running simple_set demonstration...")
    print("=" * 50)

    # Create instance of SimpleSet
    try:
        instance = SimpleSet()
        print(f"✓ Created SimpleSet instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating SimpleSet instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
