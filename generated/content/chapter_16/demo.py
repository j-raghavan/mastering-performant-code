#!/usr/bin/env python3
"""
Chapter 16: Performance Optimization & Real-World Integration
Comprehensive demonstration of optimization techniques and their application
to data structures from previous chapters.
"""

import time
import timeit
import tracemalloc
import threading
from typing import List, Dict, Any, Optional
from collections import deque

# Import our optimization modules
from .object_pool import ObjectPool, PooledObject
from .memory_profiler import MemoryProfiler
from .integration_patterns import ThreadSafeCache, PluginManager

class OptimizationDemo:
    """
    Comprehensive demonstration of Chapter 16 optimization techniques
    and their application to data structures from previous chapters.
    """
    
    def __init__(self):
        self.memory_profiler = MemoryProfiler()
        self.cache = ThreadSafeCache(max_size=1000)
        self.plugin_manager = PluginManager()
        
    def demonstrate_slots_optimization(self):
        """Demonstrate __slots__ optimization with data structures from previous chapters."""
        print("=== __slots__ Optimization Demo ===")
        
        # Regular BST Node (from Chapter 6)
        class RegularBSTNode:
            def __init__(self, key, value=None):
                self.key = key
                self.value = value
                self.left = None
                self.right = None
                self.parent = None
        
        # Optimized BST Node with __slots__
        class OptimizedBSTNode:
            __slots__ = ('key', 'value', 'left', 'right', 'parent')
            
            def __init__(self, key, value=None):
                self.key = key
                self.value = value
                self.left = None
                self.right = None
                self.parent = None
        
        # Regular Heap Node (from Chapter 11)
        class RegularHeapNode:
            def __init__(self, value, priority=0):
                self.value = value
                self.priority = priority
                self.index = 0
        
        # Optimized Heap Node with __slots__
        class OptimizedHeapNode:
            __slots__ = ('value', 'priority', 'index')
            
            def __init__(self, value, priority=0):
                self.value = value
                self.priority = priority
                self.index = 0
        
        # Create large numbers of nodes
        num_nodes = 10000
        
        # BST Nodes comparison
        regular_bst_nodes = [RegularBSTNode(i, f"value_{i}") for i in range(num_nodes)]
        optimized_bst_nodes = [OptimizedBSTNode(i, f"value_{i}") for i in range(num_nodes)]
        
        regular_bst_size = sum(sys.getsizeof(node) for node in regular_bst_nodes)
        optimized_bst_size = sum(sys.getsizeof(node) for node in optimized_bst_nodes)
        
        print(f"BST Nodes Memory Usage:")
        print(f"  Regular: {regular_bst_size:,} bytes")
        print(f"  Optimized: {optimized_bst_size:,} bytes")
        print(f"  Memory saved: {regular_bst_size - optimized_bst_size:,} bytes")
        print(f"  Percentage saved: {((regular_bst_size - optimized_bst_size) / regular_bst_size * 100):.1f}%")
        
        # Heap Nodes comparison
        regular_heap_nodes = [RegularHeapNode(i, i) for i in range(num_nodes)]
        optimized_heap_nodes = [OptimizedHeapNode(i, i) for i in range(num_nodes)]
        
        regular_heap_size = sum(sys.getsizeof(node) for node in regular_heap_nodes)
        optimized_heap_size = sum(sys.getsizeof(node) for node in optimized_heap_nodes)
        
        print(f"\nHeap Nodes Memory Usage:")
        print(f"  Regular: {regular_heap_size:,} bytes")
        print(f"  Optimized: {optimized_heap_size:,} bytes")
        print(f"  Memory saved: {regular_heap_size - optimized_heap_size:,} bytes")
        print(f"  Percentage saved: {((regular_heap_size - optimized_heap_size) / regular_heap_size * 100):.1f}%")
        
        # Performance comparison
        def create_regular_bst_nodes():
            return [RegularBSTNode(i, f"value_{i}") for i in range(1000)]
        
        def create_optimized_bst_nodes():
            return [OptimizedBSTNode(i, f"value_{i}") for i in range(1000)]
        
        regular_time = timeit.timeit(create_regular_bst_nodes, number=100)
        optimized_time = timeit.timeit(create_optimized_bst_nodes, number=100)
        
        print(f"\nBST Node Creation Performance:")
        print(f"  Regular: {regular_time:.4f} seconds")
        print(f"  Optimized: {optimized_time:.4f} seconds")
        print(f"  Speedup: {regular_time / optimized_time:.2f}x")
    
    def demonstrate_object_pool(self):
        """Demonstrate object pooling with timeout and statistics."""
        print("\n=== Object Pool Demo ===")
        
        # Create a pool of expensive objects
        pool = ObjectPool(lambda: PooledObject(0), max_size=100)
        
        # Simulate concurrent access
        def worker(worker_id: int, num_operations: int):
            """Worker function that uses the object pool."""
            for i in range(num_operations):
                obj = pool.acquire(timeout_seconds=1.0)
                if obj:
                    obj.value = worker_id * 1000 + i
                    # Simulate work
                    time.sleep(0.001)
                    pool.release(obj)
                else:
                    print(f"Worker {worker_id}: Failed to acquire object on iteration {i}")
        
        # Run multiple workers
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i, 20))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Show pool statistics
        stats = pool.get_stats()
        print(f"\nPool Statistics:")
        print(f"  Total acquires: {stats['acquires']}")
        print(f"  Total releases: {stats['releases']}")
        print(f"  Timeouts: {stats['timeouts']}")
        print(f"  Average wait time: {stats['avg_wait_time']:.4f} seconds")
        print(f"  Available objects: {pool.available()}")
        print(f"  Objects in use: {pool.in_use_count()}")
    
    def demonstrate_memory_profiling(self):
        """Demonstrate memory profiling with leak detection."""
        print("\n=== Memory Profiling Demo ===")
        
        self.memory_profiler.start_tracing()
        
        # Take initial snapshot
        initial_snapshot = self.memory_profiler.take_snapshot("Initial state")
        print(f"Initial memory: {initial_snapshot.current_memory / 1024:.1f} KiB")
        
        # Simulate memory allocation
        large_data = []
        for i in range(1000):
            large_data.append([j for j in range(100)])
        
        # Take snapshot after allocation
        allocation_snapshot = self.memory_profiler.take_snapshot("After allocation")
        print(f"After allocation: {allocation_snapshot.current_memory / 1024:.1f} KiB")
        
        # Simulate memory leak (don't clear the data)
        # In a real scenario, this would be unintentional
        
        # Take final snapshot
        final_snapshot = self.memory_profiler.take_snapshot("Final state")
        print(f"Final memory: {final_snapshot.current_memory / 1024:.1f} KiB")
        
        # Calculate memory growth
        memory_growth = final_snapshot.current_memory - initial_snapshot.current_memory
        print(f"Memory growth: {memory_growth / 1024:.1f} KiB")
        
        # Show all snapshots
        print(f"\nAll snapshots taken: {len(self.memory_profiler.snapshots)}")
        for i, snapshot in enumerate(self.memory_profiler.snapshots):
            print(f"  Snapshot {i}: {snapshot.current_memory / 1024:.1f} KiB")
        
        self.memory_profiler.stop_tracing()
    
    def demonstrate_thread_safe_cache(self):
        """Demonstrate thread-safe caching with performance monitoring."""
        print("\n=== Thread-Safe Cache Demo ===")
        
        # Simulate expensive computation
        def expensive_computation(key: str) -> str:
            """Simulate an expensive computation."""
            time.sleep(0.01)  # Simulate work
            return f"computed_value_for_{key}"
        
        # Worker function that uses the cache
        def cache_worker(worker_id: int, keys: List[str]):
            """Worker function that uses the thread-safe cache."""
            for key in keys:
                # Try to get from cache first
                cached_value = self.cache.get(key)
                if cached_value is None:
                    # Compute if not in cache
                    value = expensive_computation(key)
                    self.cache.set(key, value)
                    print(f"Worker {worker_id}: Computed value for {key}")
                else:
                    print(f"Worker {worker_id}: Found cached value for {key}")
        
        # Create test keys
        test_keys = [f"key_{i}" for i in range(20)]
        
        # Run multiple workers
        threads = []
        for i in range(3):
            thread = threading.Thread(target=cache_worker, args=(i, test_keys))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Show cache statistics
        print(f"\nCache Statistics:")
        print(f"  Cache size: {self.cache.size()}")
        print(f"  Cache capacity: {self.cache.max_size}")
    
    def demonstrate_performance_comparisons(self):
        """Demonstrate comprehensive performance comparisons."""
        print("\n=== Performance Comparisons Demo ===")
        
        # Test different optimization techniques
        results = {}
        
        # 1. __slots__ vs regular classes
        class RegularClass:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
        
        class SlotsClass:
            __slots__ = ('x', 'y', 'z')
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z
        
        def create_regular_objects():
            return [RegularClass(i, i, i) for i in range(1000)]
        
        def create_slots_objects():
            return [SlotsClass(i, i, i) for i in range(1000)]
        
        regular_time = timeit.timeit(create_regular_objects, number=100)
        slots_time = timeit.timeit(create_slots_objects, number=100)
        
        results['__slots__'] = {
            'regular_time': regular_time,
            'optimized_time': slots_time,
            'speedup': regular_time / slots_time
        }
        
        # 2. Object pool vs direct creation
        def direct_object_creation():
            objects = []
            for i in range(1000):
                obj = PooledObject(i)
                objects.append(obj)
            return objects
        
        def pooled_object_creation():
            pool = ObjectPool(lambda: PooledObject(0), max_size=1000)
            objects = []
            for i in range(1000):
                obj = pool.acquire()
                if obj:
                    obj.value = i
                    objects.append(obj)
            for obj in objects:
                pool.release(obj)
            return objects
        
        direct_time = timeit.timeit(direct_object_creation, number=100)
        pooled_time = timeit.timeit(pooled_object_creation, number=100)
        
        results['object_pool'] = {
            'regular_time': direct_time,
            'optimized_time': pooled_time,
            'speedup': direct_time / pooled_time
        }
        
        # 3. List vs deque operations
        def list_operations():
            lst = []
            for i in range(10000):
                lst.append(i)
            for _ in range(10000):
                if lst:
                    lst.pop(0)  # O(n) operation
            return lst
        
        def deque_operations():
            dq = deque()
            for i in range(10000):
                dq.append(i)
            for _ in range(10000):
                if dq:
                    dq.popleft()  # O(1) operation
            return dq
        
        list_time = timeit.timeit(list_operations, number=10)
        deque_time = timeit.timeit(deque_operations, number=10)
        
        results['deque_vs_list'] = {
            'regular_time': list_time,
            'optimized_time': deque_time,
            'speedup': list_time / deque_time
        }
        
        # Display results
        print("Performance Comparison Results:")
        print("-" * 60)
        for technique, data in results.items():
            print(f"{technique:15} | {data['regular_time']:8.4f}s | {data['optimized_time']:8.4f}s | {data['speedup']:6.2f}x")
    
    def demonstrate_integration_with_previous_chapters(self):
        """Demonstrate how optimizations apply to data structures from previous chapters."""
        print("\n=== Integration with Previous Chapters Demo ===")
        
        # Simulate optimized versions of data structures from previous chapters
        print("Optimizing data structures from previous chapters:")
        
        # Chapter 6: Binary Search Tree
        print("\n1. Chapter 6 - Binary Search Tree Optimization:")
        print("   - Apply __slots__ to BST nodes")
        print("   - Use object pooling for node allocation")
        print("   - Thread-safe operations for concurrent access")
        
        # Chapter 11: Binary Heap
        print("\n2. Chapter 11 - Binary Heap Optimization:")
        print("   - Optimize heap nodes with __slots__")
        print("   - Pool-based node management")
        print("   - Lock-free operations where possible")
        
        # Chapter 15: LRU/LFU Cache
        print("\n3. Chapter 15 - Cache Optimization:")
        print("   - Thread-safe cache operations")
        print("   - Memory-efficient eviction policies")
        print("   - Performance monitoring integration")
        
        # Show memory savings for a complete data structure
        print("\n4. Complete Data Structure Memory Analysis:")
        
        # Simulate a large BST with regular vs optimized nodes
        num_nodes = 50000
        
        # Regular BST nodes
        regular_nodes = []
        for i in range(num_nodes):
            node = type('RegularNode', (), {
                'key': i,
                'value': f"value_{i}",
                'left': None,
                'right': None,
                'parent': None
            })()
            regular_nodes.append(node)
        
        # Optimized BST nodes
        class OptimizedNode:
            __slots__ = ('key', 'value', 'left', 'right', 'parent')
            def __init__(self, key, value):
                self.key = key
                self.value = value
                self.left = None
                self.right = None
                self.parent = None
        
        optimized_nodes = [OptimizedNode(i, f"value_{i}") for i in range(num_nodes)]
        
        regular_size = sum(sys.getsizeof(node) for node in regular_nodes)
        optimized_size = sum(sys.getsizeof(node) for node in optimized_nodes)
        
        print(f"   Large BST Memory Usage ({num_nodes:,} nodes):")
        print(f"     Regular nodes: {regular_size / 1024 / 1024:.2f} MB")
        print(f"     Optimized nodes: {optimized_size / 1024 / 1024:.2f} MB")
        print(f"     Memory saved: {(regular_size - optimized_size) / 1024 / 1024:.2f} MB")
        print(f"     Percentage saved: {((regular_size - optimized_size) / regular_size * 100):.1f}%")
    
    def run_comprehensive_demo(self):
        """Run all demonstrations."""
        print("Chapter 16: Performance Optimization & Real-World Integration")
        print("=" * 70)
        
        try:
            self.demonstrate_slots_optimization()
            self.demonstrate_object_pool()
            self.demonstrate_memory_profiling()
            self.demonstrate_thread_safe_cache()
            self.demonstrate_performance_comparisons()
            self.demonstrate_integration_with_previous_chapters()
            
            print("\n" + "=" * 70)
            print("Demo completed successfully!")
            print("Key takeaways:")
            print("- __slots__ can save 40-60% memory for large numbers of objects")
            print("- Object pooling provides O(1) operations with timeout support")
            print("- Thread-safe operations are essential for concurrent systems")
            print("- Memory profiling helps identify optimization opportunities")
            print("- These techniques can be applied to optimize data structures from previous chapters")
            
        except Exception as e:
            print(f"Demo failed with error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main function to run the demonstration."""
    demo = OptimizationDemo()
    demo.run_comprehensive_demo()

if __name__ == "__main__":
    main() 