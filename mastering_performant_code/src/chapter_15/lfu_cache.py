from typing import Any, Optional, Dict, Set
class LFUNode:
    """
    Node for LFU cache doubly-linked list.
    
    Attributes:
        key (Any): The cache key
        value (Any): The cache value
        freq (int): Access frequency count
        prev (Optional[LFUNode]): Previous node in the list
        next (Optional[LFUNode]): Next node in the list
    """
    def __init__(self, key: Any, value: Any, freq: int = 1):
        self.key = key
        self.value = value
        self.freq = freq
        self.prev: Optional['LFUNode'] = None
        self.next: Optional['LFUNode'] = None

class DoublyLinkedList:
    """
    Doubly-linked list for managing nodes with the same frequency.
    
    Attributes:
        head (LFUNode): Dummy head node
        tail (LFUNode): Dummy tail node
        size (int): Number of nodes in the list
    """
    def __init__(self):
        self.head = LFUNode(None, None)
        self.tail = LFUNode(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def append(self, node: LFUNode) -> None:
        """Add a node to the end of the list."""
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node
        self.size += 1

    def pop(self, node: Optional[LFUNode] = None) -> Optional[LFUNode]:
        """
        Remove a node from the list.
        
        Args:
            node (Optional[LFUNode]): Node to remove, or None to remove the first node
            
        Returns:
            Optional[LFUNode]: The removed node, or None if list is empty
        """
        if self.size == 0:
            return None
        if not node:
            node = self.head.next
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
        return node

class LFUCache:
    """
    Production-quality LFU Cache implementation.
    
    This implementation provides O(1) average time complexity for all operations
    and includes comprehensive statistics and error handling.
    
    Attributes:
        capacity (int): Maximum number of items the cache can hold
        size (int): Current number of items in the cache
        min_freq (int): Minimum frequency among all items
        node_map (Dict): Hash map for O(1) key lookup
        freq_map (Dict): Frequency buckets containing doubly-linked lists
        stats (Dict): Statistics tracking hits, misses, evictions, and total requests
    """
    
    def __init__(self, capacity: int):
        """
        Initialize the LFU cache with specified capacity.
        
        Args:
            capacity (int): Maximum number of items the cache can hold
            
        Raises:
            ValueError: If capacity is not positive
        """
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
            
        self.capacity = capacity
        self.size = 0
        self.min_freq = 0
        self.node_map: Dict[Any, LFUNode] = {}
        self.freq_map: Dict[int, DoublyLinkedList] = {}
        
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_requests': 0
        }

    def get(self, key: Any) -> Optional[Any]:
        """
        Get value from cache and update frequency.
        
        Args:
            key (Any): The key to look up
            
        Returns:
            Optional[Any]: The value associated with the key, or None if not found
        """
        self.stats['total_requests'] += 1
        
        if key not in self.node_map:
            self.stats['misses'] += 1
            return None
            
        self.stats['hits'] += 1
        node = self.node_map[key]
        self._update(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """
        Put value into cache with LFU eviction if necessary.
        
        Args:
            key (Any): The key to store
            value (Any): The value to associate with the key
        """
        if self.capacity == 0:
            return
            
        if key in self.node_map:
            node = self.node_map[key]
            node.value = value
            self._update(node)
        else:
            if self.size >= self.capacity:
                lfu_list = self.freq_map[self.min_freq]
                to_remove = lfu_list.pop()
                if to_remove:
                    self.stats['evictions'] += 1
                    del self.node_map[to_remove.key]
                    self.size -= 1
            new_node = LFUNode(key, value)
            self.node_map[key] = new_node
            self.freq_map.setdefault(1, DoublyLinkedList()).append(new_node)
            self.min_freq = 1
            self.size += 1

    def _update(self, node: LFUNode) -> None:
        """
        Update node frequency and move to appropriate frequency bucket.
        
        Args:
            node (LFUNode): The node to update
        """
        freq = node.freq
        self.freq_map[freq].pop(node)
        if self.freq_map[freq].size == 0:
            del self.freq_map[freq]
            if self.min_freq == freq:
                self.min_freq += 1
        node.freq += 1
        self.freq_map.setdefault(node.freq, DoublyLinkedList()).append(node)
    
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
        base_size = sys.getsizeof(self.node_map) + sys.getsizeof(self.freq_map)
        node_sizes = sum(
            sys.getsizeof(node.key) + sys.getsizeof(node.value) + sys.getsizeof(node)
            for node in self.node_map.values()
        )
        freq_sizes = sum(
            sys.getsizeof(freq_list) + sys.getsizeof(freq_list.head) + sys.getsizeof(freq_list.tail)
            for freq_list in self.freq_map.values()
        )
        return base_size + node_sizes + freq_sizes
    
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
            'size': self.size,
            'capacity': self.capacity,
            'memory_usage': self.get_memory_usage(),
            'min_frequency': self.min_freq,
            'frequency_buckets': len(self.freq_map)
        }
    
    def __len__(self) -> int:
        return self.size
    
    def __contains__(self, key: Any) -> bool:
        return key in self.node_map
    
    def __repr__(self) -> str:
        return f"LFUCache(capacity={self.capacity}, size={self.size}, hit_ratio={self.get_hit_ratio():.2f})" 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running lfu_cache demonstration...")
    print("=" * 50)

    # Create instance of DoublyLinkedList
    try:
        instance = DoublyLinkedList()
        print(f"✓ Created DoublyLinkedList instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.append(1)
        instance.append(2)
        instance.append(3)
        print(f"  After adding elements: {instance}")
        print(f"  Length: {len(instance)}")
    except Exception as e:
        print(f"✗ Error creating DoublyLinkedList instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
