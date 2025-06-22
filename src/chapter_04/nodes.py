"""
Node classes for linked list implementations.

This module provides the fundamental node structures used in singly and
doubly linked lists. These nodes contain the data and references to
other nodes in the linked structure.
"""

from typing import TypeVar, Generic, Optional, List
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class SinglyNode(Generic[T]):
    """
    Node for singly linked list.
    
    Contains data and a reference to the next node.
    
    Attributes:
        data: The data stored in this node
        next: Reference to the next node in the list, or None if this is the last node
    """
    data: T
    next: Optional['SinglyNode[T]'] = None

@dataclass
class DoublyNode(Generic[T]):
    """
    Node for doubly linked list.
    
    Contains data and references to both previous and next nodes.
    
    Attributes:
        data: The data stored in this node
        prev: Reference to the previous node in the list, or None if this is the first node
        next: Reference to the next node in the list, or None if this is the last node
    """
    data: T
    prev: Optional['DoublyNode[T]'] = None
    next: Optional['DoublyNode[T]'] = None

# Optimized node classes for high-performance applications
class OptimizedSinglyNode(Generic[T]):
    """Memory-optimized singly linked list node using __slots__."""
    __slots__ = ('data', 'next')
    
    def __init__(self, data: T):
        self.data = data
        self.next = None

class OptimizedDoublyNode(Generic[T]):
    """Memory-optimized doubly linked list node using __slots__."""
    __slots__ = ('data', 'prev', 'next')
    
    def __init__(self, data: T):
        self.data = data
        self.prev = None
        self.next = None

class NodePool(Generic[T]):
    """
    Reusable node pool to reduce allocation overhead.
    
    This class maintains a pool of reusable nodes to avoid frequent
    memory allocations and deallocations, which can improve performance
    in scenarios with high node turnover.
    """
    
    def __init__(self, initial_size: int = 100):
        """
        Initialize the node pool.
        
        Args:
            initial_size: Initial number of nodes to pre-allocate
        """
        self._pool: List[DoublyNode[T]] = []
        self._max_size = initial_size * 10  # Prevent unbounded growth
        
        # Pre-allocate some nodes
        for _ in range(initial_size):
            self._pool.append(DoublyNode(None))  # type: ignore
        
    def get_node(self, data: T) -> DoublyNode[T]:
        """
        Get a node from the pool or create new one.
        
        Args:
            data: Data to store in the node
            
        Returns:
            A node instance ready for use
        """
        if self._pool:
            node = self._pool.pop()
            node.data = data
            node.prev = node.next = None
            return node
        return DoublyNode(data)
    
    def return_node(self, node: DoublyNode[T]) -> None:
        """
        Return a node to the pool for reuse.
        
        Args:
            node: The node to return to the pool
        """
        if len(self._pool) < self._max_size:
            node.data = None  # Help GC
            node.prev = node.next = None
            self._pool.append(node)
    
    def pool_size(self) -> int:
        """Get the current number of nodes in the pool."""
        return len(self._pool)
    
    def clear_pool(self) -> None:
        """Clear all nodes from the pool."""
        self._pool.clear() 