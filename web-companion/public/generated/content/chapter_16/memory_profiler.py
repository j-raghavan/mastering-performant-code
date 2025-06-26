"""
Memory profiling utilities for Chapter 16.

This module provides tools for analyzing memory usage and identifying
optimization opportunities using only built-in Python modules.
"""

import sys
import tracemalloc
import gc
import timeit
import threading
from typing import Any, Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from contextlib import contextmanager


@dataclass
class MemorySnapshot:
    """Represents a memory snapshot with detailed information."""
    current_memory: int
    peak_memory: int
    object_count: int
    timestamp: float


@dataclass
class MemoryComparison:
    """Comparison between two memory snapshots."""
    baseline: MemorySnapshot
    optimized: MemorySnapshot
    memory_saved: int
    percentage_saved: float
    performance_impact: float  # Time difference in seconds


class MemoryProfiler:
    """
    A comprehensive memory profiler using built-in Python modules.
    
    This class provides tools for analyzing memory usage patterns,
    identifying memory leaks, and comparing optimization strategies.
    
    Thread-safe implementation with proper synchronization.
    """
    
    def __init__(self):
        self.snapshots: List[MemorySnapshot] = []
        self._tracing = False
        self._lock = threading.Lock()  # Thread safety lock
    
    def start_tracing(self) -> None:
        """Start memory tracing with thread safety."""
        with self._lock:
            if not self._tracing:
                tracemalloc.start()
                self._tracing = True
    
    def stop_tracing(self) -> None:
        """Stop memory tracing with thread safety."""
        with self._lock:
            if self._tracing:
                tracemalloc.stop()
                self._tracing = False
    
    def take_snapshot(self, label: str = "") -> MemorySnapshot:
        """
        Take a memory snapshot with thread safety.
        
        This method ensures that tracing state changes are synchronized
        to prevent race conditions in concurrent environments.
        """
        with self._lock:
            # Check if tracing is needed and start it if necessary
            if not self._tracing:
                # Release lock temporarily to avoid deadlock
                self._lock.release()
                tracemalloc.start()
                self._lock.acquire()
                self._tracing = True
            
            current, peak = tracemalloc.get_traced_memory()
            snapshot = tracemalloc.take_snapshot()
            
            memory_snapshot = MemorySnapshot(
                current_memory=current,
                peak_memory=peak,
                object_count=len(snapshot.statistics('filename')),
                timestamp=timeit.default_timer()
            )
            
            self.snapshots.append(memory_snapshot)
            return memory_snapshot
    
    def analyze_object_memory(self, obj: Any) -> Dict[str, Any]:
        """Analyze memory usage of a specific object."""
        size = sys.getsizeof(obj)
        ref_count = sys.getrefcount(obj) - 1  # Subtract the reference from getrefcount
        
        # For containers, analyze their contents
        container_info = {}
        if hasattr(obj, '__len__'):
            try:
                container_info['length'] = len(obj)
                if hasattr(obj, '__iter__'):
                    # Estimate total size of contained objects
                    total_content_size = 0
                    for item in obj:
                        total_content_size += sys.getsizeof(item)
                    container_info['content_size'] = total_content_size
                    container_info['total_size'] = size + total_content_size
            except (TypeError, RecursionError):
                pass
        
        return {
            'object_size': size,
            'reference_count': ref_count,
            'type': type(obj).__name__,
            'container_info': container_info
        }
    
    def compare_memory_usage(self, baseline_func: Callable, 
                           optimized_func: Callable, 
                           iterations: int = 1000) -> MemoryComparison:
        """Compare memory usage between baseline and optimized implementations."""
        # Force garbage collection before each test
        gc.collect()
        
        # Baseline measurement
        self.start_tracing()
        baseline_start = self.take_snapshot("baseline_start")
        
        baseline_time = timeit.timeit(baseline_func, number=iterations)
        baseline_end = self.take_snapshot("baseline_end")
        
        # Force garbage collection
        gc.collect()
        
        # Optimized measurement
        optimized_start = self.take_snapshot("optimized_start")
        
        optimized_time = timeit.timeit(optimized_func, number=iterations)
        optimized_end = self.take_snapshot("optimized_end")
        
        self.stop_tracing()
        
        # Calculate differences
        baseline_memory = baseline_end.current_memory - baseline_start.current_memory
        optimized_memory = optimized_end.current_memory - optimized_start.current_memory
        
        memory_saved = baseline_memory - optimized_memory
        percentage_saved = (memory_saved / baseline_memory * 100) if baseline_memory > 0 else 0
        performance_impact = optimized_time - baseline_time
        
        return MemoryComparison(
            baseline=MemorySnapshot(
                current_memory=baseline_memory,
                peak_memory=baseline_end.peak_memory,
                object_count=baseline_end.object_count,
                timestamp=baseline_time
            ),
            optimized=MemorySnapshot(
                current_memory=optimized_memory,
                peak_memory=optimized_end.peak_memory,
                object_count=optimized_end.object_count,
                timestamp=optimized_time
            ),
            memory_saved=memory_saved,
            percentage_saved=percentage_saved,
            performance_impact=performance_impact
        )
    
    def detect_memory_leaks(self, func: Callable, iterations: int = 100) -> Dict[str, Any]:
        """Detect potential memory leaks in a function."""
        self.start_tracing()
        
        initial_snapshot = self.take_snapshot("initial")
        
        # Run the function multiple times
        for i in range(iterations):
            func()
            if i % 10 == 0:  # Take snapshot every 10 iterations
                self.take_snapshot(f"iteration_{i}")
        
        final_snapshot = self.take_snapshot("final")
        
        # Force garbage collection
        gc.collect()
        after_gc_snapshot = self.take_snapshot("after_gc")
        
        self.stop_tracing()
        
        # Analyze for leaks
        memory_growth = final_snapshot.current_memory - initial_snapshot.current_memory
        memory_after_gc = after_gc_snapshot.current_memory - initial_snapshot.current_memory
        
        return {
            'memory_growth': memory_growth,
            'memory_after_gc': memory_after_gc,
            'potential_leak': memory_after_gc > 0,
            'leak_size': memory_after_gc,
            'snapshots': self.snapshots[-iterations-3:]  # Last few snapshots
        }
    
    def get_top_memory_users(self, limit: int = 10) -> List[Tuple[str, int]]:
        """Get the top memory users from the current snapshot."""
        with self._lock:
            if not self._tracing:
                return []
            
            # Take snapshot outside of lock to avoid potential issues
            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')
            
            return [(str(stat.traceback.format()[:100]), stat.size) 
                    for stat in top_stats[:limit]]


@contextmanager
def memory_context(profiler: MemoryProfiler, label: str = ""):
    """Context manager for memory profiling."""
    profiler.start_tracing()
    start_snapshot = profiler.take_snapshot(f"{label}_start")
    
    try:
        yield start_snapshot
    finally:
        end_snapshot = profiler.take_snapshot(f"{label}_end")
        profiler.stop_tracing()
        
        memory_used = end_snapshot.current_memory - start_snapshot.current_memory
        print(f"Memory used in {label}: {memory_used / 1024:.2f} KiB")


def demonstrate_memory_optimization():
    """Demonstrate memory optimization techniques."""
    profiler = MemoryProfiler()
    
    # Example 1: Regular class vs __slots__
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
    
    # Compare memory usage
    comparison = profiler.compare_memory_usage(
        create_regular_objects, 
        create_slots_objects
    )
    
    print("Memory Optimization Comparison:")
    print(f"Memory saved: {comparison.memory_saved / 1024:.2f} KiB")
    print(f"Percentage saved: {comparison.percentage_saved:.1f}%")
    print(f"Performance impact: {comparison.performance_impact:.6f} seconds")
    
    return comparison


if __name__ == "__main__":
    demonstrate_memory_optimization() 