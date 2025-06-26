"""
Database Index Implementation using B-Trees

This module demonstrates how B-Trees are used in real database systems
to provide efficient key-based lookups and range queries.
"""

from typing import TypeVar, Generic, Optional, List, Dict, Any, Tuple
from dataclasses import dataclass
import time
from .btree import BTree

K = TypeVar('K')
V = TypeVar('V')

@dataclass
class IndexEntry(Generic[K, V]):
    """An entry in a database index."""
    key: K
    value: V
    timestamp: float
    
    def __lt__(self, other: 'IndexEntry[K, V]') -> bool:
        """Compare entries by key."""
        return self.key < other.key

class DatabaseIndex(Generic[K, V]):
    """
    A simple database index implementation using B-Trees.
    
    This demonstrates how B-Trees are used in real database systems
    to provide efficient key-based lookups and range queries.
    
    Args:
        min_degree: Minimum degree of the underlying B-Tree
    """
    
    def __init__(self, min_degree: int = 3) -> None:
        self.btree = BTree[IndexEntry[K, V]](min_degree=min_degree)
        self.size = 0
    
    def __len__(self) -> int:
        """Return the number of entries in the index."""
        return self.size
    
    def is_empty(self) -> bool:
        """Check if the index is empty."""
        return self.size == 0
    
    def insert(self, key: K, value: V) -> None:
        """
        Insert a key-value pair into the index.
        
        Args:
            key: The key to insert
            value: The value associated with the key
        """
        entry = IndexEntry(key=key, value=value, timestamp=time.time())
        self.btree.insert(entry)
        self.size += 1
    
    def get(self, key: K) -> Optional[V]:
        """
        Get the value associated with a key.
        
        Args:
            key: The key to look up
            
        Returns:
            The value associated with the key, or None if not found
        """
        # Find the entry with the same key
        for entry in self.btree.inorder_traversal():
            if entry.key == key:
                return entry.value
        return None
    
    def delete(self, key: K) -> bool:
        """
        Delete a key-value pair from the index.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False if it wasn't found
        """
        # Find and delete the entry with the given key
        for entry in self.btree.inorder_traversal():
            if entry.key == key:
                self.btree.delete(entry)
                self.size -= 1
                return True
        return False
    
    def range_query(self, start_key: K, end_key: K) -> List[Tuple[K, V]]:
        """
        Find all key-value pairs in the range [start_key, end_key].
        
        Args:
            start_key: Start of the range (inclusive)
            end_key: End of the range (inclusive)
            
        Returns:
            List of (key, value) tuples in the range
        """
        start_entry = IndexEntry(key=start_key, value=None, timestamp=0)
        end_entry = IndexEntry(key=end_key, value=None, timestamp=0)
        
        entries = self.btree.range_query(start_entry, end_entry)
        return [(entry.key, entry.value) for entry in entries]
    
    def get_all(self) -> List[Tuple[K, V]]:
        """Get all key-value pairs in the index."""
        return [(entry.key, entry.value) for entry in self.btree.inorder_traversal()]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the index."""
        from .analyzer import BTreeAnalyzer
        
        btree_stats = BTreeAnalyzer.analyze_btree(self.btree)
        
        return {
            'size': self.size,
            'height': btree_stats.height,
            'min_degree': btree_stats.min_degree,
            'memory_usage': btree_stats.memory_usage,
            'average_keys_per_node': btree_stats.average_keys_per_node,
            'storage_efficiency': btree_stats.storage_efficiency,
            'theoretical_height': btree_stats.theoretical_height
        }
    
    def clear(self) -> None:
        """Remove all entries from the index."""
        self.btree.clear()
        self.size = 0
    
    def __contains__(self, key: K) -> bool:
        """Check if a key exists in the index."""
        return self.get(key) is not None
    
    def __repr__(self) -> str:
        if self.is_empty():
            return "DatabaseIndex()"
        
        items = self.get_all()
        if len(items) <= 5:
            return f"DatabaseIndex({dict(items)})"
        else:
            return f"DatabaseIndex({dict(items[:3])}...{dict(items[-2:])})"
    
    def __iter__(self):
        """Iterate over all key-value pairs in the index."""
        return iter(self.get_all())

class MultiValueIndex(Generic[K, V]):
    """
    A database index that supports multiple values per key.
    
    This is useful for cases where a key can have multiple associated values,
    such as in a many-to-many relationship.
    """
    
    def __init__(self, min_degree: int = 3) -> None:
        self.index = DatabaseIndex[K, List[V]](min_degree=min_degree)
    
    def __len__(self) -> int:
        """Return the total number of values across all keys."""
        total = 0
        for key, values in self.index.get_all():
            total += len(values)
        return total
    
    def insert(self, key: K, value: V) -> None:
        """
        Insert a value for a key.
        
        Args:
            key: The key
            value: The value to associate with the key
        """
        existing_values = self.index.get(key)
        if existing_values is None:
            existing_values = []
        
        existing_values.append(value)
        self.index.insert(key, existing_values)
    
    def get(self, key: K) -> List[V]:
        """
        Get all values associated with a key.
        
        Args:
            key: The key to look up
            
        Returns:
            List of values associated with the key, or empty list if not found
        """
        values = self.index.get(key)
        return values if values is not None else []
    
    def delete(self, key: K, value: Optional[V] = None) -> bool:
        """
        Delete a key-value pair or entire key.
        
        Args:
            key: The key to delete
            value: The specific value to delete (if None, delete entire key)
            
        Returns:
            True if something was deleted, False otherwise
        """
        if value is None:
            # Delete entire key
            return self.index.delete(key)
        else:
            # Delete specific value
            existing_values = self.index.get(key)
            if existing_values is None:
                return False
            
            try:
                existing_values.remove(value)
                if not existing_values:
                    # If no values left, delete the key entirely
                    self.index.delete(key)
                else:
                    # Update with remaining values
                    self.index.insert(key, existing_values)
                return True
            except ValueError:
                return False
    
    def range_query(self, start_key: K, end_key: K) -> List[Tuple[K, List[V]]]:
        """
        Find all key-value pairs in the range [start_key, end_key].
        
        Args:
            start_key: Start of the range (inclusive)
            end_key: End of the range (inclusive)
            
        Returns:
            List of (key, values) tuples in the range
        """
        return self.index.range_query(start_key, end_key)
    
    def get_all(self) -> List[Tuple[K, List[V]]]:
        """Get all key-value pairs in the index."""
        return self.index.get_all()
    
    def __contains__(self, key: K) -> bool:
        """Check if a key exists in the index."""
        return key in self.index
    
    def __repr__(self) -> str:
        if self.index.is_empty():
            return "MultiValueIndex()"
        
        items = self.get_all()
        if len(items) <= 3:
            return f"MultiValueIndex({dict(items)})"
        else:
            return f"MultiValueIndex({dict(items[:2])}...{dict(items[-1:])})"

class TimestampedIndex(Generic[K, V]):
    """
    A database index that maintains timestamps for all entries.
    
    This is useful for tracking when data was inserted or modified,
    and for implementing features like data expiration or versioning.
    """
    
    def __init__(self, min_degree: int = 3) -> None:
        self.index = DatabaseIndex[K, Tuple[V, float]](min_degree=min_degree)
    
    def __len__(self) -> int:
        """Return the number of entries in the index."""
        return len(self.index)
    
    def insert(self, key: K, value: V, timestamp: Optional[float] = None) -> None:
        """
        Insert a key-value pair with a timestamp.
        
        Args:
            key: The key to insert
            value: The value associated with the key
            timestamp: The timestamp (defaults to current time)
        """
        if timestamp is None:
            timestamp = time.time()
        
        self.index.insert(key, (value, timestamp))
    
    def get(self, key: K) -> Optional[Tuple[V, float]]:
        """
        Get the value and timestamp associated with a key.
        
        Args:
            key: The key to look up
            
        Returns:
            Tuple of (value, timestamp) or None if not found
        """
        return self.index.get(key)
    
    def get_value(self, key: K) -> Optional[V]:
        """
        Get only the value associated with a key.
        
        Args:
            key: The key to look up
            
        Returns:
            The value or None if not found
        """
        result = self.index.get(key)
        return result[0] if result is not None else None
    
    def get_timestamp(self, key: K) -> Optional[float]:
        """
        Get only the timestamp associated with a key.
        
        Args:
            key: The key to look up
            
        Returns:
            The timestamp or None if not found
        """
        result = self.index.get(key)
        return result[1] if result is not None else None
    
    def delete(self, key: K) -> bool:
        """
        Delete a key-value pair from the index.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was deleted, False if it wasn't found
        """
        return self.index.delete(key)
    
    def range_query(self, start_key: K, end_key: K) -> List[Tuple[K, Tuple[V, float]]]:
        """
        Find all key-value pairs in the range [start_key, end_key].
        
        Args:
            start_key: Start of the range (inclusive)
            end_key: End of the range (inclusive)
            
        Returns:
            List of (key, (value, timestamp)) tuples in the range
        """
        return self.index.range_query(start_key, end_key)
    
    def get_all(self) -> List[Tuple[K, Tuple[V, float]]]:
        """Get all key-value pairs in the index."""
        return self.index.get_all()
    
    def get_entries_after(self, timestamp: float) -> List[Tuple[K, Tuple[V, float]]]:
        """
        Get all entries with timestamps after the given time.
        
        Args:
            timestamp: The minimum timestamp
            
        Returns:
            List of entries with timestamps after the given time
        """
        # This is a simplified implementation - in practice, you might want
        # a separate index on timestamps for efficient range queries
        result = []
        for key, (value, ts) in self.index.get_all():
            if ts > timestamp:
                result.append((key, (value, ts)))
        return result
    
    def get_entries_before(self, timestamp: float) -> List[Tuple[K, Tuple[V, float]]]:
        """
        Get all entries with timestamps before the given time.
        
        Args:
            timestamp: The maximum timestamp
            
        Returns:
            List of entries with timestamps before the given time
        """
        result = []
        for key, (value, ts) in self.index.get_all():
            if ts < timestamp:
                result.append((key, (value, ts)))
        return result
    
    def __contains__(self, key: K) -> bool:
        """Check if a key exists in the index."""
        return key in self.index
    
    def __repr__(self) -> str:
        if self.index.is_empty():
            return "TimestampedIndex()"
        
        items = self.get_all()
        if len(items) <= 3:
            return f"TimestampedIndex({dict(items)})"
        else:
            return f"TimestampedIndex({dict(items[:2])}...{dict(items[-1:])})" 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running database_index demonstration...")
    print("=" * 50)

    # Create instance of IndexEntry
    try:
        instance = IndexEntry()
        print(f"✓ Created IndexEntry instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating IndexEntry instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
