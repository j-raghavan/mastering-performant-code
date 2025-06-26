from collections import OrderedDict
from typing import Optional, Any, Dict
import timeit
class LRUCacheOrderedDict:
    """
    Production-quality LRU Cache implementation using collections.OrderedDict.
    
    This implementation provides O(1) average time complexity for all operations
    and includes comprehensive statistics and error handling.
    
    Attributes:
        capacity (int): Maximum number of items the cache can hold
        cache (OrderedDict): The underlying cache storage
        stats (Dict): Statistics tracking hits, misses, evictions, and total requests
    
    Example:
        >>> cache = LRUCacheOrderedDict(3)
        >>> cache.put("a", 1)
        >>> cache.get("a")
        1
        >>> cache.get_hit_ratio()
        1.0
    """
    
    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with specified capacity.
        
        Args:
            capacity (int): Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is not positive
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self.cache = OrderedDict()
        self.capacity = capacity
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }

    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache and update access order.
        
        Args:
            key (Any): The key to look up
            
        Returns:
            Optional[Any]: The value associated with the key, or None if not found
        """
        self.stats['total_requests'] += 1
        
        if key not in self.cache:
            self.stats['misses'] += 1
            return None
            
        self.stats['hits'] += 1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        """
        Put value into cache with LRU eviction if necessary.
        
        Args:
            key (Any): The key to store
            value (Any): The value to associate with the key
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.stats['evictions'] += 1
                self.cache.popitem(last=False)
        
        self.cache[key] = value
    
    def get_hit_ratio(self) -> float:
        """
        Calculate cache hit ratio.
        
        Returns:
            float: Hit ratio between 0.0 and 1.0
        """
        if self.stats['total_requests'] == 0:
            return 0.0
        return self.stats['hits'] / self.stats['total_requests']
    
    def get_memory_usage(self) -> int:
        """
        Estimate memory usage in bytes.
        
        Returns:
            int: Estimated memory usage in bytes
        """
        base_size = sys.getsizeof(self.cache)
        item_sizes = sum(
            sys.getsizeof(k) + sys.getsizeof(v) 
            for k, v in self.cache.items()
        )
        return base_size + item_sizes
    
    def clear_stats(self) -> None:
        """Reset all statistics to zero."""
        self.stats = {key: 0 for key in self.stats}
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive cache statistics.
        
        Returns:
            Dict[str, Any]: Dictionary containing all statistics
        """
        return {
            **self.stats,
            'hit_ratio': self.get_hit_ratio(),
            'size': len(self.cache),
            'capacity': self.capacity,
            'memory_usage': self.get_memory_usage()
        }
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __contains__(self, key: Any) -> bool:
        return key in self.cache
    
    def __repr__(self) -> str:
        return f"LRUCache(capacity={self.capacity}, size={len(self.cache)}, hit_ratio={self.get_hit_ratio():.2f})"

class Node:
    """
    Node for doubly-linked list implementation.
    
    Attributes:
        key (Any): The cache key
        value (Any): The cache value
        prev (Optional[Node]): Previous node in the list
        next (Optional[Node]): Next node in the list
    """
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCacheDLL:
    """
    Production-quality LRU Cache implementation using a custom doubly-linked list.
    
    This implementation provides O(1) average time complexity for all operations
    and includes comprehensive statistics and error handling.
    
    Attributes:
        capacity (int): Maximum number of items the cache can hold
        cache (Dict): Hash map for O(1) key lookup
        head (Node): Dummy head node
        tail (Node): Dummy tail node
        stats (Dict): Statistics tracking hits, misses, evictions, and total requests
    """
    
    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with specified capacity.
        
        Args:
            capacity (int): Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is not positive
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
            
        self.capacity = capacity
        self.cache = dict()
        self.head = Node(0, 0)  # Dummy head
        self.tail = Node(0, 0)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }

    def _remove(self, node: Node) -> None:
        """Remove a node from the doubly-linked list."""
        prev, nxt = node.prev, node.next
        if prev and nxt:
            prev.next = nxt
            nxt.prev = prev

    def _add(self, node: Node) -> None:
        """Add a node to the front of the doubly-linked list."""
        node.prev = self.head
        node.next = self.head.next
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache and update access order.
        
        Args:
            key (Any): The key to look up
            
        Returns:
            Optional[Any]: The value associated with the key, or None if not found
        """
        self.stats['total_requests'] += 1
        
        node = self.cache.get(key, None)
        if not node:
            self.stats['misses'] += 1
            return None
            
        self.stats['hits'] += 1
        self._remove(node)
        self._add(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """
        Put value into cache with LRU eviction if necessary.
        
        Args:
            key (Any): The key to store
            value (Any): The value to associate with the key
        """
        node = self.cache.get(key)
        if node:
            self._remove(node)
            node.value = value
            self._add(node)
        else:
            if len(self.cache) >= self.capacity:
                # Remove LRU
                lru = self.tail.prev
                if lru and lru != self.head:
                    self.stats['evictions'] += 1
                    self._remove(lru)
                    del self.cache[lru.key]
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
    
    def get_hit_ratio(self) -> float:
        """
        Calculate cache hit ratio.
        
        Returns:
            float: Hit ratio between 0.0 and 1.0
        """
        if self.stats['total_requests'] == 0:
            return 0.0
        return self.stats['hits'] / self.stats['total_requests']
    
    def get_memory_usage(self) -> int:
        """
        Estimate memory usage in bytes.
        
        Returns:
            int: Estimated memory usage in bytes
        """
        base_size = sys.getsizeof(self.cache)
        node_sizes = sum(
            sys.getsizeof(node.key) + sys.getsizeof(node.value) + sys.getsizeof(node)
            for node in self.cache.values()
        )
        return base_size + node_sizes
    
    def clear_stats(self) -> None:
        """Reset all statistics to zero."""
        self.stats = {key: 0 for key in self.stats}
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive cache statistics.
        
        Returns:
            Dict[str, Any]: Dictionary containing all statistics
        """
        return {
            **self.stats,
            'hit_ratio': self.get_hit_ratio(),
            'size': len(self.cache),
            'capacity': self.capacity,
            'memory_usage': self.get_memory_usage()
        }
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __contains__(self, key: Any) -> bool:
        return key in self.cache
    
    def __repr__(self) -> str:
        return f"LRUCacheDLL(capacity={self.capacity}, size={len(self.cache)}, hit_ratio={self.get_hit_ratio():.2f})" 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running lru_cache demonstration...")
    print("=" * 50)

    # Create instance of LRUCacheOrderedDict
    try:
        instance = LRUCacheOrderedDict()
        print(f"✓ Created LRUCacheOrderedDict instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating LRUCacheOrderedDict instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
