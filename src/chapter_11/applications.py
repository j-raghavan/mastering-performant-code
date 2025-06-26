"""
Real-World Applications of Heaps and Priority Queues

This module provides practical applications demonstrating the use of
binary heaps and priority queues in real-world scenarios.
"""

import time
import random
from typing import TypeVar, Generic, Optional, List, Callable, Any, Dict, Tuple
from dataclasses import dataclass
from .binary_heap import BinaryHeap
from .priority_queue import PriorityQueue

T = TypeVar('T')

@dataclass
class Task:
    """A task with priority, duration, and metadata."""
    id: int
    name: str
    priority: int
    duration: float
    created_at: float
    deadline: Optional[float] = None
    
    def __repr__(self) -> str:
        return f"Task({self.name}, priority={self.priority}, duration={self.duration})"

@dataclass
class Event:
    """An event with priority, processing time, and type."""
    id: int
    event_type: str
    priority: int
    processing_time: float
    timestamp: float
    data: Any = None
    
    def __repr__(self) -> str:
        return f"Event({self.event_type}, priority={self.priority}, time={self.processing_time})"

class TaskScheduler:
    """
    A simple task scheduler using priority queues.
    
    This demonstrates a real-world application of priority queues
    for scheduling tasks with different priorities.
    """
    
    def __init__(self) -> None:
        self._queue = PriorityQueue[Task](max_heap=True)  # Use max-heap for higher priority first
        self._task_id_counter = 0
        self._completed_tasks = []
        self._current_time = 0.0
    
    def add_task(self, task_name: str, priority: int, duration: float = 1.0, 
                 deadline: Optional[float] = None) -> int:
        """Add a task to the scheduler."""
        task_id = self._task_id_counter
        self._task_id_counter += 1
        
        task = Task(
            id=task_id,
            name=task_name,
            priority=priority,
            duration=duration,
            created_at=self._current_time,
            deadline=deadline
        )
        
        self._queue.put(task, priority)
        return task_id
    
    def get_next_task(self) -> Optional[Task]:
        """Get the next highest priority task."""
        if self._queue.is_empty():
            return None
        return self._queue.get()
    
    def peek_next_task(self) -> Optional[Task]:
        """Peek at the next highest priority task without removing it."""
        if self._queue.is_empty():
            return None
        return self._queue.peek()
    
    def execute_task(self, task: Task) -> None:
        """Execute a task and update the current time."""
        self._current_time += task.duration
        self._completed_tasks.append(task)
    
    def run_scheduler(self, max_tasks: Optional[int] = None) -> List[Task]:
        """Run the scheduler and return completed tasks."""
        completed = []
        task_count = 0
        
        while not self._queue.is_empty() and (max_tasks is None or task_count < max_tasks):
            task = self.get_next_task()
            if task:
                self.execute_task(task)
                completed.append(task)
                task_count += 1
        
        return completed
    
    def __len__(self) -> int:
        return len(self._queue)
    
    def is_empty(self) -> bool:
        return self._queue.is_empty()
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return self._completed_tasks.copy()
    
    def get_current_time(self) -> float:
        """Get the current simulation time."""
        return self._current_time

class TopKElements:
    """
    Find the top K elements from a stream using a min-heap.
    
    This demonstrates how to use heaps for finding the largest
    or smallest K elements efficiently.
    """
    
    def __init__(self, k: int, find_largest: bool = True) -> None:
        """
        Initialize the top K finder.
        
        Args:
            k: Number of top elements to find
            find_largest: If True, find largest K elements; if False, find smallest
        """
        self.k = k
        self.find_largest = find_largest
        # Use min-heap for largest K, max-heap for smallest K
        heap_type = "min" if find_largest else "max"
        self._heap = BinaryHeap[int](heap_type=heap_type)
    
    def add(self, value: int) -> None:
        """Add a value to the top K finder."""
        if len(self._heap) < self.k:
            self._heap.push(value)
        else:
            if self.find_largest:
                # For largest K: if value > min_heap_root, replace root
                if value > self._heap.peek():
                    self._heap.pop()
                    self._heap.push(value)
            else:
                # For smallest K: if value < max_heap_root, replace root
                if value < self._heap.peek():
                    self._heap.pop()
                    self._heap.push(value)
    
    def get_top_k(self) -> List[int]:
        """Get the current top K elements."""
        result = []
        temp_heap = BinaryHeap[int](heap_type=self._heap._heap_type)
        
        # Extract all elements
        while not self._heap.is_empty():
            value = self._heap.pop()
            result.append(value)
            temp_heap.push(value)
        
        # Restore the heap
        while not temp_heap.is_empty():
            self._heap.push(temp_heap.pop())
        
        # Sort result appropriately
        if self.find_largest:
            result.sort(reverse=True)
        else:
            result.sort()
        
        return result
    
    def clear(self) -> None:
        """Clear all elements."""
        self._heap.clear()

class MedianFinder:
    """
    Find the median of a stream of numbers using two heaps.
    
    This demonstrates how to use heaps to efficiently find the median
    of a data stream.
    """
    
    def __init__(self) -> None:
        """Initialize the median finder with two heaps."""
        # Max heap for the lower half (smaller numbers)
        self._lower_heap = BinaryHeap[int](heap_type="max")
        # Min heap for the upper half (larger numbers)
        self._upper_heap = BinaryHeap[int](heap_type="min")
    
    def add_num(self, num: int) -> None:
        """Add a number to the data stream."""
        # Always add to lower heap first
        self._lower_heap.push(num)
        
        # Balance the heaps
        if len(self._lower_heap) > len(self._upper_heap) + 1:
            # Move largest from lower to upper
            value = self._lower_heap.pop()
            self._upper_heap.push(value)
        elif len(self._upper_heap) > len(self._lower_heap):
            # Move smallest from upper to lower
            value = self._upper_heap.pop()
            self._lower_heap.push(value)
        
        # Additional balancing: ensure lower heap root <= upper heap root
        if (not self._lower_heap.is_empty() and not self._upper_heap.is_empty() and
            self._lower_heap.peek() > self._upper_heap.peek()):
            # Swap the roots
            lower_val = self._lower_heap.pop()
            upper_val = self._upper_heap.pop()
            self._lower_heap.push(upper_val)
            self._upper_heap.push(lower_val)
    
    def find_median(self) -> float:
        """Find the median of the current data stream."""
        if len(self._lower_heap) == 0 and len(self._upper_heap) == 0:
            raise ValueError("No numbers in the stream")
        
        if len(self._lower_heap) > len(self._upper_heap):
            return float(self._lower_heap.peek())
        elif len(self._upper_heap) > len(self._lower_heap):
            return float(self._upper_heap.peek())
        else:
            # Both heaps have same size, return average of roots
            return (self._lower_heap.peek() + self._upper_heap.peek()) / 2.0
    
    def get_all_numbers(self) -> List[int]:
        """Get all numbers in sorted order."""
        result = []
        
        # Extract from lower heap (max heap, so reverse order)
        lower_nums = []
        while not self._lower_heap.is_empty():
            lower_nums.append(self._lower_heap.pop())
        
        # Extract from upper heap (min heap, so correct order)
        upper_nums = []
        while not self._upper_heap.is_empty():
            upper_nums.append(self._upper_heap.pop())
        
        # Combine and sort
        result = sorted(lower_nums + upper_nums)
        
        # Restore heaps
        for num in lower_nums:
            self._lower_heap.push(num)
        for num in upper_nums:
            self._upper_heap.push(num)
        
        return result

class SlidingWindowMax:
    """
    Find the maximum element in each sliding window using a deque.
    
    This demonstrates how to use a deque for sliding window problems.
    """
    
    def __init__(self, window_size: int) -> None:
        """
        Initialize the sliding window maximum finder.
        
        Args:
            window_size: Size of the sliding window
        """
        self.window_size = window_size
        self._deque = []  # Store (value, index) pairs
        self._current_index = 0
    
    def add_element(self, value: int) -> Optional[int]:
        """
        Add an element and return the maximum in the current window.
        
        Returns:
            Maximum value in the current window, or None if window not full
        """
        # Remove elements outside the current window
        while self._deque and self._deque[0][1] <= self._current_index - self.window_size:
            self._deque.pop(0)
        
        # Remove elements smaller than current value from the back
        while self._deque and self._deque[-1][0] <= value:
            self._deque.pop()
        
        # Add current element
        self._deque.append((value, self._current_index))
        self._current_index += 1
        
        # Return maximum if window is full
        if self._current_index >= self.window_size:
            return self._deque[0][0]
        return None
    
    def get_max_in_window(self, values: List[int]) -> List[int]:
        """
        Get maximum values for all sliding windows in a list.
        
        Args:
            values: List of values to process
            
        Returns:
            List of maximum values for each window
        """
        result = []
        for value in values:
            max_val = self.add_element(value)
            if max_val is not None:
                result.append(max_val)
        return result

class EventSimulator:
    """
    Simulate events with different priorities and processing times.
    
    This demonstrates a more complex real-world scenario using priority queues.
    """
    
    def __init__(self) -> None:
        """Initialize the event simulator."""
        self._event_queue = PriorityQueue[Event](max_heap=True)
        self._current_time = 0.0
        self._processed_events = []
        self._event_id_counter = 0
    
    def add_event(self, event_type: str, priority: int, processing_time: float, 
                  data: Any = None) -> int:
        """Add an event to the simulator."""
        event_id = self._event_id_counter
        self._event_id_counter += 1
        
        event = Event(
            id=event_id,
            event_type=event_type,
            priority=priority,
            processing_time=processing_time,
            timestamp=self._current_time,
            data=data
        )
        
        self._event_queue.put(event, priority)
        return event_id
    
    def process_next_event(self) -> Optional[Event]:
        """Process the next highest priority event."""
        if self._event_queue.is_empty():
            return None
        
        event = self._event_queue.get()
        self._current_time += event.processing_time
        self._processed_events.append(event)
        return event
    
    def run_simulation(self, max_events: Optional[int] = None) -> List[Event]:
        """Run the event simulation."""
        processed = []
        event_count = 0
        
        while not self._event_queue.is_empty() and (max_events is None or event_count < max_events):
            event = self.process_next_event()
            if event:
                processed.append(event)
                event_count += 1
        
        return processed
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get simulation statistics."""
        if not self._processed_events:
            return {}
        
        event_types = {}
        total_processing_time = 0.0
        
        for event in self._processed_events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
            total_processing_time += event.processing_time
        
        return {
            "total_events": len(self._processed_events),
            "total_time": self._current_time,
            "avg_processing_time": total_processing_time / len(self._processed_events),
            "event_type_distribution": event_types,
            "priority_distribution": self._event_queue.get_priority_distribution()
        } 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running applications demonstration...")
    print("=" * 50)

    # Create instance of Task
    try:
        instance = Task()
        print(f"✓ Created Task instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating Task instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
