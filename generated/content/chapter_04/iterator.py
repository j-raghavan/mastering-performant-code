"""
Advanced iterator implementation for linked lists.

This module provides an enhanced iterator with additional functionality
including state tracking, filtering, and bidirectional iteration.
"""

from typing import TypeVar, Generic, Optional, Iterator, List, Callable
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class IteratorState(Generic[T]):
    """
    State information for linked list iterators.
    
    This class tracks the current state of iteration including
    the current node, direction, index, and whether iteration is exhausted.
    
    Attributes:
        current_node: The current node being processed
        direction: The direction of iteration ('forward' or 'reverse')
        index: The current index in the iteration
        exhausted: Whether the iteration has been exhausted
    """
    current_node: Optional[T]
    direction: str  # 'forward' or 'reverse'
    index: int
    exhausted: bool = False

class LinkedListIterator(Generic[T]):
    """
    Advanced iterator for linked lists with additional functionality.
    
    This iterator provides:
    - Bidirectional traversal
    - State tracking
    - Filtering capabilities
    - Index tracking
    - Take and skip operations
    
    Attributes:
        _list: The linked list being iterated over
        _direction: The direction of iteration
        _state: Current state of the iterator
    """
    
    def __init__(self, linked_list: 'DoublyLinkedList[T]', 
                 direction: str = 'forward', 
                 start_index: Optional[int] = None) -> None:
        """
        Initialize the iterator.
        
        Args:
            linked_list: The doubly linked list to iterate over
            direction: Direction of iteration ('forward' or 'reverse')
            start_index: Optional starting index for iteration
        """
        if direction not in ('forward', 'reverse'):
            raise ValueError("Direction must be 'forward' or 'reverse'")
        
        self._list = linked_list
        self._direction = direction
        self._state = IteratorState(
            current_node=None,
            direction=direction,
            index=-1,
            exhausted=False
        )
        self._reset(start_index)
    
    def _reset(self, start_index: Optional[int] = None) -> None:
        """
        Reset the iterator to its initial state.
        
        Args:
            start_index: Optional starting index for iteration
        """
        if start_index is not None:
            if not 0 <= start_index < len(self._list):
                raise IndexError("Start index out of range")
            self._state.index = start_index - 1
            self._state.current_node = self._list._head_sentinel.next
            for _ in range(start_index):
                self._state.current_node = self._state.current_node.next
        else:
            if self._direction == 'forward':
                self._state.current_node = self._list._head_sentinel.next
                self._state.index = -1
            else:
                self._state.current_node = self._list._tail_sentinel.prev
                self._state.index = len(self._list)
        
        self._state.exhausted = False
    
    def __iter__(self) -> 'LinkedListIterator[T]':
        """Return the iterator itself."""
        return self
    
    def __next__(self) -> T:
        """
        Get the next element in the iteration.
        
        Returns:
            The next element in the iteration
            
        Raises:
            StopIteration: When there are no more elements
        """
        if self._state.exhausted:
            raise StopIteration
        
        # Check if we've reached the take limit
        if hasattr(self, '_take_count') and hasattr(self, '_taken'):
            if self._taken >= self._take_count:
                self._state.exhausted = True
                raise StopIteration
        
        if self._direction == 'forward':
            if (self._state.current_node == self._list._tail_sentinel or 
                self._state.current_node is None):
                self._state.exhausted = True
                raise StopIteration
            
            result = self._state.current_node.data
            self._state.current_node = self._state.current_node.next
            self._state.index += 1
            
            # Check if we've reached the end after moving
            if self._state.current_node == self._list._tail_sentinel:
                self._state.exhausted = True
        else:
            if (self._state.current_node == self._list._head_sentinel or 
                self._state.current_node is None):
                self._state.exhausted = True
                raise StopIteration
            
            result = self._state.current_node.data
            self._state.current_node = self._state.current_node.prev
            self._state.index -= 1
            
            # Check if we've reached the end after moving
            if self._state.current_node == self._list._head_sentinel:
                self._state.exhausted = True
        
        # Increment taken count if we're using take
        if hasattr(self, '_taken'):
            self._taken += 1
        
        return result
    
    def current_index(self) -> int:
        """
        Get the current index in the iteration.
        
        Returns:
            The current index (0-based for forward, len-1-based for reverse)
        """
        return self._state.index
    
    def has_next(self) -> bool:
        """
        Check if there are more elements to iterate over.
        
        Returns:
            True if there are more elements, False otherwise
        """
        if self._state.exhausted:
            return False
        
        if self._direction == 'forward':
            return (self._state.current_node is not None and 
                   self._state.current_node != self._list._tail_sentinel)
        else:
            return (self._state.current_node is not None and 
                   self._state.current_node != self._list._head_sentinel)
    
    def filter(self, predicate: Callable[[T], bool]) -> Iterator[T]:
        """
        Create a filtered iterator based on a predicate.
        
        Args:
            predicate: A function that takes an element and returns True/False
            
        Returns:
            An iterator that yields only elements for which predicate returns True
        """
        for item in self:
            if predicate(item):
                yield item
    
    def take(self, count: int) -> 'LinkedListIterator[T]':
        """
        Take only the first 'count' elements from the iterator.
        
        Args:
            count: Number of elements to take
            
        Returns:
            A new iterator that yields at most 'count' elements
        """
        if count < 0:
            raise ValueError("Count must be non-negative")
        
        # Create a new iterator with the same state
        new_iterator = LinkedListIterator(self._list, self._direction)
        new_iterator._state = IteratorState(
            current_node=self._state.current_node,
            direction=self._direction,
            index=self._state.index,
            exhausted=self._state.exhausted
        )
        
        # Add a counter to limit the number of elements
        new_iterator._take_count = count
        new_iterator._taken = 0
        
        return new_iterator
    
    def skip(self, count: int) -> 'LinkedListIterator[T]':
        """
        Skip the first 'count' elements from the iterator.
        
        Args:
            count: Number of elements to skip
            
        Returns:
            A new iterator that skips the first 'count' elements
        """
        if count < 0:
            raise ValueError("Count must be non-negative")
        
        # Create a new iterator with the same state
        new_iterator = LinkedListIterator(self._list, self._direction)
        new_iterator._state = IteratorState(
            current_node=self._state.current_node,
            direction=self._direction,
            index=self._state.index,
            exhausted=self._state.exhausted
        )
        
        # Skip the specified number of elements
        for _ in range(count):
            try:
                next(new_iterator)
            except StopIteration:
                break
        
        return new_iterator
    
    def map(self, transform: Callable[[T], T]) -> Iterator[T]:
        """
        Apply a transformation function to each element.
        
        Args:
            transform: A function that transforms each element
            
        Returns:
            An iterator that yields transformed elements
        """
        for item in self:
            yield transform(item)
    
    def enumerate(self) -> Iterator[tuple[int, T]]:
        """
        Enumerate the elements with their indices.
        
        Returns:
            An iterator that yields (index, element) pairs
        """
        for i, item in enumerate(self):
            yield (i, item)
    
    def collect(self) -> List[T]:
        """
        Collect all remaining elements into a list.
        
        Returns:
            A list containing all remaining elements
        """
        return list(self)
    
    def find_first(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Find the first element that satisfies the predicate.
        
        Args:
            predicate: A function that takes an element and returns True/False
            
        Returns:
            The first element that satisfies the predicate, or None if not found
        """
        for item in self:
            if predicate(item):
                return item
        return None
    
    def all(self, predicate: Callable[[T], bool]) -> bool:
        """
        Check if all elements satisfy the predicate.
        
        Args:
            predicate: A function that takes an element and returns True/False
            
        Returns:
            True if all elements satisfy the predicate, False otherwise
        """
        for item in self:
            if not predicate(item):
                return False
        return True
    
    def any(self, predicate: Callable[[T], bool]) -> bool:
        """
        Check if any element satisfies the predicate.
        
        Args:
            predicate: A function that takes an element and returns True/False
            
        Returns:
            True if any element satisfies the predicate, False otherwise
        """
        for item in self:
            if predicate(item):
                return True
        return False
    
    def count_matching(self, predicate: Callable[[T], bool]) -> int:
        """
        Count the number of elements that satisfy the predicate.
        
        Args:
            predicate: A function that takes an element and returns True/False
            
        Returns:
            The number of elements that satisfy the predicate
        """
        count = 0
        for item in self:
            if predicate(item):
                count += 1
        return count
    
    def get_state(self) -> IteratorState[T]:
        """
        Get the current state of the iterator.
        
        Returns:
            A copy of the current iterator state
        """
        return IteratorState(
            current_node=self._state.current_node,
            direction=self._state.direction,
            index=self._state.index,
            exhausted=self._state.exhausted
        )
    
    def set_state(self, state: IteratorState[T]) -> None:
        """
        Set the iterator state.
        
        Args:
            state: The new state to set
        """
        self._state = state
        self._direction = state.direction


class ChainableIterator(LinkedListIterator[T]):
    """
    Iterator with efficient method chaining.
    
    This iterator extends LinkedListIterator with method chaining capabilities
    that return new iterators instead of generators, enabling more efficient
    composition of iteration operations.
    """
    
    def __init__(self, linked_list: 'DoublyLinkedList[T]', 
                 direction: str = 'forward', 
                 start_index: Optional[int] = None,
                 filter_predicate: Optional[Callable[[T], bool]] = None,
                 transform_func: Optional[Callable[[T], T]] = None,
                 take_count: Optional[int] = None,
                 taken: int = 0) -> None:
        super().__init__(linked_list, direction, start_index)
        self._filter_predicate = filter_predicate
        self._transform_func = transform_func
        self._take_count = take_count
        self._taken = taken
    
    def filter(self, predicate: Callable[[T], bool]) -> 'ChainableIterator[T]':
        def combined_filter(x):
            if self._filter_predicate:
                return self._filter_predicate(x) and predicate(x)
            return predicate(x)
        return ChainableIterator(
            self._list, 
            self._direction, 
            filter_predicate=combined_filter,
            transform_func=self._transform_func,
            take_count=self._take_count
        )
    
    def map(self, transform: Callable[[T], T]) -> 'ChainableIterator[T]':
        def combined_transform(x):
            if self._transform_func:
                return transform(self._transform_func(x))
            return transform(x)
        return ChainableIterator(
            self._list, 
            self._direction, 
            filter_predicate=self._filter_predicate,
            transform_func=combined_transform,
            take_count=self._take_count
        )
    
    def take(self, count: int) -> 'ChainableIterator[T]':
        # If already has a take, use the smaller of the two
        new_take = count
        if self._take_count is not None:
            new_take = min(self._take_count, count)
        return ChainableIterator(
            self._list, 
            self._direction, 
            filter_predicate=self._filter_predicate,
            transform_func=self._transform_func,
            take_count=new_take
        )
    
    def __next__(self) -> T:
        # Check take limit first
        if self._take_count is not None and self._taken >= self._take_count:
            raise StopIteration
        
        while True:
            # Get next item from parent iterator (without take logic)
            if self._state.exhausted:
                raise StopIteration
            
            if self._direction == 'forward':
                if (self._state.current_node == self._list._tail_sentinel or 
                    self._state.current_node is None):
                    self._state.exhausted = True
                    raise StopIteration
                
                result = self._state.current_node.data
                self._state.current_node = self._state.current_node.next
                self._state.index += 1
                
                if self._state.current_node == self._list._tail_sentinel:
                    self._state.exhausted = True
            else:
                if (self._state.current_node == self._list._head_sentinel or 
                    self._state.current_node is None):
                    self._state.exhausted = True
                    raise StopIteration
                
                result = self._state.current_node.data
                self._state.current_node = self._state.current_node.prev
                self._state.index -= 1
                
                if self._state.current_node == self._list._head_sentinel:
                    self._state.exhausted = True
            
            # Apply filter if present
            if self._filter_predicate is not None and not self._filter_predicate(result):
                continue
            
            # Apply transform if present
            if self._transform_func is not None:
                result = self._transform_func(result)
            
            # Increment taken count
            if self._take_count is not None:
                self._taken += 1
            
            return result 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running iterator demonstration...")
    print("=" * 50)

    # Create instance of IteratorState
    try:
        instance = IteratorState()
        print(f"✓ Created IteratorState instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating IteratorState instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
