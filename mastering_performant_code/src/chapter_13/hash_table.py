from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, Iterator, Tuple, List, Dict, Any
import sys

K = TypeVar('K')
V = TypeVar('V')

class HashTableInterface(ABC, Generic[K, V]):
    """
    Abstract base class for hash table implementations.
    """
    @abstractmethod
    def __getitem__(self, key: K) -> V:
        pass
    @abstractmethod
    def __setitem__(self, key: K, value: V) -> None:
        pass
    @abstractmethod
    def __delitem__(self, key: K) -> None:
        pass
    @abstractmethod
    def __contains__(self, key: K) -> bool:
        pass
    @abstractmethod
    def __len__(self) -> int:
        pass
    @abstractmethod
    def __iter__(self) -> Iterator[K]:
        pass
    @abstractmethod
    def clear(self) -> None:
        pass
    @abstractmethod
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        pass
    @abstractmethod
    def items(self) -> Iterator[Tuple[K, V]]:
        pass
    @abstractmethod
    def keys(self) -> Iterator[K]:
        pass
    @abstractmethod
    def values(self) -> Iterator[V]:
        pass
    
    @abstractmethod
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics."""
        pass
    
    @abstractmethod
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        pass
    
    @abstractmethod
    def analyze_hash_distribution(self) -> Dict[str, Any]:
        """Analyze hash function distribution quality."""
        pass

class Node(Generic[K, V]):
    def __init__(self, key: K, value: V, next_node: Optional['Node[K, V]'] = None):
        self.key = key
        self.value = value
        self.next = next_node

class SeparateChainingHashTable(HashTableInterface[K, V]):
    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        self._capacity = initial_capacity
        self._size = 0
        self._load_factor = load_factor
        self._table: List[Optional[Node[K, V]]] = [None] * initial_capacity
        # Performance tracking
        self._resize_count = 0
        self._collision_count = 0
        self._probe_count = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, key: K) -> V:
        index = self._hash(key)
        node = self._table[index]
        probes = 0
        
        while node is not None:
            probes += 1
            if node.key == key:
                self._probe_count += probes
                return node.value
            node = node.next
        
        self._probe_count += probes
        raise KeyError(key)
    
    def __setitem__(self, key: K, value: V) -> None:
        if self._size >= self._capacity * self._load_factor:
            self._resize(self._capacity * 2)
        
        index = self._hash(key)
        node = self._table[index]
        
        # Check if key already exists
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next
        
        # Insert new node at beginning of list
        self._table[index] = Node(key, value, self._table[index])
        self._size += 1
        
        # Track collisions
        if self._table[index].next is not None:
            self._collision_count += 1
    
    def __delitem__(self, key: K) -> None:
        index = self._hash(key)
        node = self._table[index]
        prev = None
        
        while node is not None:
            if node.key == key:
                if prev is None:
                    self._table[index] = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return
            prev = node
            node = node.next
        raise KeyError(key)
    
    def __contains__(self, key: K) -> bool:
        try:
            self[key]
            return True
        except KeyError:
            return False
    
    def __iter__(self) -> Iterator[K]:
        for node in self._table:
            while node is not None:
                yield node.key
                node = node.next
    
    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._size = 0
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        try:
            return self[key]
        except KeyError:
            return default
    
    def items(self) -> Iterator[Tuple[K, V]]:
        for node in self._table:
            while node is not None:
                yield (node.key, node.value)
                node = node.next
    
    def keys(self) -> Iterator[K]:
        return iter(self)
    
    def values(self) -> Iterator[V]:
        for node in self._table:
            while node is not None:
                yield node.value
                node = node.next
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            'size': self._size,
            'capacity': self._capacity,
            'load_factor': self._size / self._capacity if self._capacity > 0 else 0,
            'resize_count': self._resize_count,
            'collision_count': self._collision_count,
            'probe_count': self._probe_count,
            'average_probes': self._probe_count / max(self._size, 1),
            'max_chain_length': self._get_max_chain_length(),
            'empty_buckets': self._get_empty_bucket_count()
        }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            'table_memory': sys.getsizeof(self._table),
            'total_memory': sys.getsizeof(self) + sys.getsizeof(self._table),
            'memory_per_element': sys.getsizeof(self._table) / len(self._table),
            'load_factor': self._size / self._capacity
        }
    
    def analyze_hash_distribution(self) -> Dict[str, Any]:
        """Analyze hash function distribution quality."""
        bucket_counts = [0] * self._capacity
        for key in self.keys():
            bucket_counts[self._hash(key)] += 1
        
        return {
            'max_bucket_size': max(bucket_counts),
            'min_bucket_size': min(bucket_counts),
            'empty_buckets': bucket_counts.count(0),
            'distribution_variance': self._calculate_variance(bucket_counts),
            'bucket_distribution': bucket_counts
        }
    
    def _hash(self, key: K) -> int:
        return hash(key) % self._capacity
    
    def _resize(self, new_capacity: int) -> None:
        self._resize_count += 1
        old_table = self._table
        self._capacity = new_capacity
        self._size = 0
        self._table = [None] * new_capacity
        for node in old_table:
            while node is not None:
                self[node.key] = node.value
                node = node.next
    
    def _get_max_chain_length(self) -> int:
        max_length = 0
        for node in self._table:
            length = 0
            current = node
            while current is not None:
                length += 1
                current = current.next
            max_length = max(max_length, length)
        return max_length
    
    def _get_empty_bucket_count(self) -> int:
        return sum(1 for node in self._table if node is None)
    
    def _calculate_variance(self, values: List[int]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

class LinearProbingHashTable(HashTableInterface[K, V]):
    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        self._capacity = initial_capacity
        self._size = 0
        self._load_factor = load_factor
        self._table: List[Optional[Tuple[K, V]]] = [None] * initial_capacity
        self._deleted: List[bool] = [False] * initial_capacity
        # Performance tracking
        self._resize_count = 0
        self._collision_count = 0
        self._probe_count = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, key: K) -> V:
        index = self._find_key(key)
        if index is None:
            raise KeyError(key)
        return self._table[index][1]
    
    def __setitem__(self, key: K, value: V) -> None:
        if self._size >= self._capacity * self._load_factor:
            self._resize(self._capacity * 2)
        
        index = self._find_insertion_point(key)
        if self._table[index] is None or self._deleted[index]:
            self._size += 1
        self._table[index] = (key, value)
        self._deleted[index] = False
    
    def __delitem__(self, key: K) -> None:
        index = self._find_key(key)
        if index is None:
            raise KeyError(key)
        self._table[index] = None
        self._deleted[index] = True
        self._size -= 1
        if self._size < self._capacity * 0.25 and self._capacity > 16:
            self._resize(self._capacity // 2)
    
    def __contains__(self, key: K) -> bool:
        return self._find_key(key) is not None
    
    def __iter__(self) -> Iterator[K]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item[0]
    
    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._deleted = [False] * self._capacity
        self._size = 0
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        try:
            return self[key]
        except KeyError:
            return default
    
    def items(self) -> Iterator[Tuple[K, V]]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item
    
    def keys(self) -> Iterator[K]:
        return iter(self)
    
    def values(self) -> Iterator[V]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item[1]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            'size': self._size,
            'capacity': self._capacity,
            'load_factor': self._size / self._capacity if self._capacity > 0 else 0,
            'resize_count': self._resize_count,
            'collision_count': self._collision_count,
            'probe_count': self._probe_count,
            'average_probes': self._probe_count / max(self._size, 1),
            'tombstone_count': sum(self._deleted),
            'empty_slots': self._get_empty_slot_count()
        }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            'table_memory': sys.getsizeof(self._table),
            'deleted_memory': sys.getsizeof(self._deleted),
            'total_memory': sys.getsizeof(self) + sys.getsizeof(self._table) + sys.getsizeof(self._deleted),
            'memory_per_element': (sys.getsizeof(self._table) + sys.getsizeof(self._deleted)) / len(self._table),
            'load_factor': self._size / self._capacity
        }
    
    def analyze_hash_distribution(self) -> Dict[str, Any]:
        """Analyze hash function distribution quality."""
        bucket_counts = [0] * self._capacity
        for key in self.keys():
            bucket_counts[self._hash(key)] += 1
        
        return {
            'max_bucket_size': max(bucket_counts),
            'min_bucket_size': min(bucket_counts),
            'empty_buckets': bucket_counts.count(0),
            'distribution_variance': self._calculate_variance(bucket_counts),
            'bucket_distribution': bucket_counts
        }
    
    def _hash(self, key: K) -> int:
        return hash(key) % self._capacity
    
    def _find_key(self, key: K) -> Optional[int]:
        index = self._hash(key)
        original_index = index
        probes = 0
        
        while True:
            probes += 1
            if self._table[index] is None and not self._deleted[index]:
                self._probe_count += probes
                return None
            if (self._table[index] is not None and not self._deleted[index] and self._table[index][0] == key):
                self._probe_count += probes
                return index
            index = (index + 1) % self._capacity
            if index == original_index:
                self._probe_count += probes
                return None
    
    def _find_insertion_point(self, key: K) -> int:
        index = self._hash(key)
        original_index = index
        probes = 0
        
        while True:
            probes += 1
            if (self._table[index] is None or self._deleted[index] or 
                (self._table[index] is not None and self._table[index][0] == key)):
                self._probe_count += probes
                return index
            index = (index + 1) % self._capacity
            if index == original_index:
                raise RuntimeError("Hash table is full")
    
    def _resize(self, new_capacity: int) -> None:
        self._resize_count += 1
        old_table = self._table
        old_deleted = self._deleted
        self._capacity = new_capacity
        self._size = 0
        self._table = [None] * new_capacity
        self._deleted = [False] * new_capacity
        for i, item in enumerate(old_table):
            if item is not None and not old_deleted[i]:
                self[item[0]] = item[1]
    
    def _get_empty_slot_count(self) -> int:
        return sum(1 for i, item in enumerate(self._table) 
                  if item is None and not self._deleted[i])
    
    def _calculate_variance(self, values: List[int]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

class QuadraticProbingHashTable(HashTableInterface[K, V]):
    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        self._capacity = initial_capacity
        self._size = 0
        self._load_factor = load_factor
        self._table: List[Optional[Tuple[K, V]]] = [None] * initial_capacity
        self._deleted: List[bool] = [False] * initial_capacity
        # Performance tracking
        self._resize_count = 0
        self._collision_count = 0
        self._probe_count = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, key: K) -> V:
        index = self._find_key(key)
        if index is None:
            raise KeyError(key)
        return self._table[index][1]
    
    def __setitem__(self, key: K, value: V) -> None:
        # Check if we need to resize before attempting insertion
        if self._size >= self._capacity * self._load_factor:
            self._resize(self._capacity * 2)
        
        # Try to find insertion point
        try:
            index = self._find_insertion_point(key)
            if self._table[index] is None or self._deleted[index]:
                self._size += 1
            self._table[index] = (key, value)
            self._deleted[index] = False
        except RuntimeError:
            # If table is full, resize and try again
            self._resize(self._capacity * 2)
            index = self._find_insertion_point(key)
            if self._table[index] is None or self._deleted[index]:
                self._size += 1
            self._table[index] = (key, value)
            self._deleted[index] = False
    
    def __delitem__(self, key: K) -> None:
        index = self._find_key(key)
        if index is None:
            raise KeyError(key)
        self._table[index] = None
        self._deleted[index] = True
        self._size -= 1
        if self._size < self._capacity * 0.25 and self._capacity > 16:
            self._resize(self._capacity // 2)
    
    def __contains__(self, key: K) -> bool:
        return self._find_key(key) is not None
    
    def __iter__(self) -> Iterator[K]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item[0]
    
    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._deleted = [False] * self._capacity
        self._size = 0
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        try:
            return self[key]
        except KeyError:
            return default
    
    def items(self) -> Iterator[Tuple[K, V]]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item
    
    def keys(self) -> Iterator[K]:
        return iter(self)
    
    def values(self) -> Iterator[V]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item[1]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            'size': self._size,
            'capacity': self._capacity,
            'load_factor': self._size / self._capacity if self._capacity > 0 else 0,
            'resize_count': self._resize_count,
            'collision_count': self._collision_count,
            'probe_count': self._probe_count,
            'average_probes': self._probe_count / max(self._size, 1),
            'tombstone_count': sum(self._deleted),
            'empty_slots': self._get_empty_slot_count()
        }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            'table_memory': sys.getsizeof(self._table),
            'deleted_memory': sys.getsizeof(self._deleted),
            'total_memory': sys.getsizeof(self) + sys.getsizeof(self._table) + sys.getsizeof(self._deleted),
            'memory_per_element': (sys.getsizeof(self._table) + sys.getsizeof(self._deleted)) / len(self._table),
            'load_factor': self._size / self._capacity
        }
    
    def analyze_hash_distribution(self) -> Dict[str, Any]:
        """Analyze hash function distribution quality."""
        bucket_counts = [0] * self._capacity
        for key in self.keys():
            bucket_counts[self._hash(key)] += 1
        
        return {
            'max_bucket_size': max(bucket_counts),
            'min_bucket_size': min(bucket_counts),
            'empty_buckets': bucket_counts.count(0),
            'distribution_variance': self._calculate_variance(bucket_counts),
            'bucket_distribution': bucket_counts
        }
    
    def _hash(self, key: K) -> int:
        return hash(key) % self._capacity
    
    def _probe(self, index: int, i: int) -> int:
        return (index + i * i) % self._capacity
    
    def _find_key(self, key: K) -> Optional[int]:
        index = self._hash(key)
        probes = 0
        
        for i in range(self._capacity):
            probes += 1
            probe_index = self._probe(index, i)
            
            if self._table[probe_index] is None and not self._deleted[probe_index]:
                self._probe_count += probes
                return None
            if (self._table[probe_index] is not None and not self._deleted[probe_index] and 
                self._table[probe_index][0] == key):
                self._probe_count += probes
                return probe_index
        
        self._probe_count += probes
        return None
    
    def _find_insertion_point(self, key: K) -> int:
        index = self._hash(key)
        probes = 0
        
        for i in range(self._capacity):
            probes += 1
            probe_index = self._probe(index, i)
            
            if (self._table[probe_index] is None or self._deleted[probe_index] or 
                (self._table[probe_index] is not None and self._table[probe_index][0] == key)):
                self._probe_count += probes
                return probe_index
        
        raise RuntimeError("Hash table is full")
    
    def _resize(self, new_capacity: int) -> None:
        self._resize_count += 1
        old_table = self._table
        old_deleted = self._deleted
        self._capacity = new_capacity
        self._size = 0
        self._table = [None] * new_capacity
        self._deleted = [False] * new_capacity
        for i, item in enumerate(old_table):
            if item is not None and not old_deleted[i]:
                self[item[0]] = item[1]
    
    def _get_empty_slot_count(self) -> int:
        return sum(1 for i, item in enumerate(self._table) 
                  if item is None and not self._deleted[i])
    
    def _calculate_variance(self, values: List[int]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)

class DoubleHashingHashTable(HashTableInterface[K, V]):
    def __init__(self, initial_capacity: int = 16, load_factor: float = 0.75):
        self._capacity = initial_capacity
        self._size = 0
        self._load_factor = load_factor
        self._table: List[Optional[Tuple[K, V]]] = [None] * initial_capacity
        self._deleted: List[bool] = [False] * initial_capacity
        # Performance tracking
        self._resize_count = 0
        self._collision_count = 0
        self._probe_count = 0
    
    def __len__(self) -> int:
        return self._size
    
    def __getitem__(self, key: K) -> V:
        index = self._find_key(key)
        if index is None:
            raise KeyError(key)
        return self._table[index][1]
    
    def __setitem__(self, key: K, value: V) -> None:
        # Check if we need to resize before attempting insertion
        if self._size >= self._capacity * self._load_factor:
            self._resize(self._capacity * 2)
        
        # Try to find insertion point
        try:
            index = self._find_insertion_point(key)
            if self._table[index] is None or self._deleted[index]:
                self._size += 1
            self._table[index] = (key, value)
            self._deleted[index] = False
        except RuntimeError:
            # If table is full, resize and try again
            self._resize(self._capacity * 2)
            index = self._find_insertion_point(key)
            if self._table[index] is None or self._deleted[index]:
                self._size += 1
            self._table[index] = (key, value)
            self._deleted[index] = False
    
    def __delitem__(self, key: K) -> None:
        index = self._find_key(key)
        if index is None:
            raise KeyError(key)
        self._table[index] = None
        self._deleted[index] = True
        self._size -= 1
        if self._size < self._capacity * 0.25 and self._capacity > 16:
            self._resize(self._capacity // 2)
    
    def __contains__(self, key: K) -> bool:
        return self._find_key(key) is not None
    
    def __iter__(self) -> Iterator[K]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item[0]
    
    def clear(self) -> None:
        self._table = [None] * self._capacity
        self._deleted = [False] * self._capacity
        self._size = 0
    
    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        try:
            return self[key]
        except KeyError:
            return default
    
    def items(self) -> Iterator[Tuple[K, V]]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item
    
    def keys(self) -> Iterator[K]:
        return iter(self)
    
    def values(self) -> Iterator[V]:
        for i, item in enumerate(self._table):
            if item is not None and not self._deleted[i]:
                yield item[1]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics."""
        return {
            'size': self._size,
            'capacity': self._capacity,
            'load_factor': self._size / self._capacity if self._capacity > 0 else 0,
            'resize_count': self._resize_count,
            'collision_count': self._collision_count,
            'probe_count': self._probe_count,
            'average_probes': self._probe_count / max(self._size, 1),
            'tombstone_count': sum(self._deleted),
            'empty_slots': self._get_empty_slot_count()
        }
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        return {
            'table_memory': sys.getsizeof(self._table),
            'deleted_memory': sys.getsizeof(self._deleted),
            'total_memory': sys.getsizeof(self) + sys.getsizeof(self._table) + sys.getsizeof(self._deleted),
            'memory_per_element': (sys.getsizeof(self._table) + sys.getsizeof(self._deleted)) / len(self._table),
            'load_factor': self._size / self._capacity
        }
    
    def analyze_hash_distribution(self) -> Dict[str, Any]:
        """Analyze hash function distribution quality."""
        bucket_counts = [0] * self._capacity
        for key in self.keys():
            bucket_counts[self._hash1(key)] += 1
        
        return {
            'max_bucket_size': max(bucket_counts),
            'min_bucket_size': min(bucket_counts),
            'empty_buckets': bucket_counts.count(0),
            'distribution_variance': self._calculate_variance(bucket_counts),
            'bucket_distribution': bucket_counts
        }
    
    def _hash1(self, key: K) -> int:
        return hash(key) % self._capacity
    
    def _hash2(self, key: K) -> int:
        return 1 + (hash(key) % (self._capacity - 1))
    
    def _probe(self, key: K, i: int) -> int:
        return (self._hash1(key) + i * self._hash2(key)) % self._capacity
    
    def _find_key(self, key: K) -> Optional[int]:
        probes = 0
        
        for i in range(self._capacity):
            probes += 1
            probe_index = self._probe(key, i)
            
            if self._table[probe_index] is None and not self._deleted[probe_index]:
                self._probe_count += probes
                return None
            if (self._table[probe_index] is not None and not self._deleted[probe_index] and 
                self._table[probe_index][0] == key):
                self._probe_count += probes
                return probe_index
        
        self._probe_count += probes
        return None
    
    def _find_insertion_point(self, key: K) -> int:
        probes = 0
        
        for i in range(self._capacity):
            probes += 1
            probe_index = self._probe(key, i)
            
            if (self._table[probe_index] is None or self._deleted[probe_index] or 
                (self._table[probe_index] is not None and self._table[probe_index][0] == key)):
                self._probe_count += probes
                return probe_index
        
        raise RuntimeError("Hash table is full")
    
    def _resize(self, new_capacity: int) -> None:
        self._resize_count += 1
        old_table = self._table
        old_deleted = self._deleted
        self._capacity = new_capacity
        self._size = 0
        self._table = [None] * new_capacity
        self._deleted = [False] * new_capacity
        for i, item in enumerate(old_table):
            if item is not None and not old_deleted[i]:
                self[item[0]] = item[1]
    
    def _get_empty_slot_count(self) -> int:
        return sum(1 for i, item in enumerate(self._table) 
                  if item is None and not self._deleted[i])
    
    def _calculate_variance(self, values: List[int]) -> float:
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values) 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running hash_table demonstration...")
    print("=" * 50)

    # Create instance of HashTableInterface
    try:
        instance = HashTableInterface()
        print(f"✓ Created HashTableInterface instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance["key1"] = "value1"
        instance["key2"] = "value2"
        print(f"  After adding elements: {instance}")
        print(f"  Size: {len(instance)}")
    except Exception as e:
        print(f"✗ Error creating HashTableInterface instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
