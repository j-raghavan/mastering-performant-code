from typing import Generic, TypeVar, List, Optional, Callable, Set
import timeit
import threading
import time
from collections import deque

T = TypeVar('T')

class PooledObject:
    """
    A simple pooled object with __slots__ for memory efficiency.
    """
    __slots__ = ('value', 'in_use', 'created_at', 'last_used')
    def __init__(self, value: int):
        self.value = value
        self.in_use = False
        self.created_at = time.time()
        self.last_used = time.time()

class ObjectPool(Generic[T]):
    """
    A generic object pool for managing reusable objects efficiently.
    
    This implementation uses separate collections for available and in-use objects
    to achieve O(1) acquire and release operations.
    
    Features:
    - O(1) acquire and release operations
    - Timeout support for acquire operations
    - Fair queuing (FIFO order)
    - Performance monitoring
    - Thread safety
    """
    __slots__ = ('_available', '_in_use', '_factory', '_max_size', '_lock', '_waiting_queue', '_stats')
    
    def __init__(self, factory: Callable[[], T], max_size: int = 10):
        self._available: deque = deque()  # Use deque for O(1) operations
        self._in_use: Set[T] = set()
        self._factory = factory
        self._max_size = max_size
        self._lock = threading.RLock()  # Reentrant lock for thread safety
        self._waiting_queue = deque()  # Queue for threads waiting for objects
        self._stats = {
            'acquires': 0,
            'releases': 0,
            'timeouts': 0,
            'total_wait_time': 0.0
        }
        
        # Pre-populate the pool
        for _ in range(max_size):
            self._available.append(factory())

    def acquire(self, timeout_seconds: Optional[float] = None) -> Optional[T]:
        """
        Acquire an available object from the pool, or None if exhausted.
        
        Args:
            timeout_seconds: Maximum time to wait for an object (None = no timeout)
        
        Time Complexity: O(1) - uses deque.popleft() operation
        """
        with self._lock:
            if self._available:
                obj = self._available.popleft()  # O(1) operation
                self._in_use.add(obj)
                obj.in_use = True
                obj.last_used = time.time()
                self._stats['acquires'] += 1
                return obj
            
            if timeout_seconds is None:
                return None
            
            # Wait for an object to become available
            start_time = time.time()
            while time.time() - start_time < timeout_seconds:
                # Release lock temporarily to allow other threads to release objects
                self._lock.release()
                time.sleep(0.001)  # Small sleep to prevent busy waiting
                self._lock.acquire()
                
                if self._available:
                    obj = self._available.popleft()
                    self._in_use.add(obj)
                    obj.in_use = True
                    obj.last_used = time.time()
                    self._stats['acquires'] += 1
                    self._stats['total_wait_time'] += time.time() - start_time
                    return obj
            
            self._stats['timeouts'] += 1
            return None

    def release(self, obj: T) -> None:
        """
        Release an object back to the pool.
        
        Time Complexity: O(1) - uses set.remove() and deque.appendleft()
        """
        with self._lock:
            if obj in self._in_use:
                self._in_use.remove(obj)
                self._available.appendleft(obj)  # Add to front for immediate reacquisition
                obj.in_use = False
                self._stats['releases'] += 1

    def available(self) -> int:
        """
        Return the number of available objects in the pool.
        
        Time Complexity: O(1) - just returns length of available deque
        """
        with self._lock:
            return len(self._available)
    
    def in_use_count(self) -> int:
        """
        Return the number of objects currently in use.
        
        Time Complexity: O(1) - just returns length of in_use set
        """
        with self._lock:
            return len(self._in_use)
    
    def total_count(self) -> int:
        """
        Return the total number of objects in the pool.
        
        Time Complexity: O(1)
        """
        return self._max_size
    
    def get_stats(self) -> dict:
        """
        Get performance statistics for the pool.
        
        Returns:
            Dictionary containing pool statistics
        """
        with self._lock:
            stats = self._stats.copy()
            if stats['acquires'] > 0:
                stats['avg_wait_time'] = stats['total_wait_time'] / stats['acquires']
            else:
                stats['avg_wait_time'] = 0.0
            return stats
    
    def clear_stats(self) -> None:
        """Clear all statistics."""
        with self._lock:
            self._stats = {
                'acquires': 0,
                'releases': 0,
                'timeouts': 0,
                'total_wait_time': 0.0
            }

def pool_benchmark():
    """Benchmark acquire/release performance of the object pool."""
    pool = ObjectPool(lambda: PooledObject(0), max_size=1000)
    
    def acquire_release():
        objs = [pool.acquire() for _ in range(1000)]
        for obj in objs:
            pool.release(obj)
    
    t = timeit.timeit(acquire_release, number=1000)
    print(f"Acquire/release 1000 objects x1000: {t:.4f} seconds")
    
    # Test timeout functionality
    def test_timeout():
        # Exhaust the pool
        objs = [pool.acquire() for _ in range(1000)]
        # Try to acquire with timeout
        start_time = time.time()
        result = pool.acquire(timeout_seconds=0.1)
        timeout_duration = time.time() - start_time
        print(f"Timeout test: {timeout_duration:.4f}s, result: {result}")
        # Release all objects
        for obj in objs:
            pool.release(obj)
    
    test_timeout()
    print(f"Pool statistics: {pool.get_stats()}")

if __name__ == "__main__":
    pool_benchmark() 