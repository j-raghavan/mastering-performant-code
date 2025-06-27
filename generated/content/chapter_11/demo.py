"""
Chapter 11 Demo: Binary Heap & Priority Queues

This module provides comprehensive demonstrations of binary heaps and priority queues,
including performance analysis and real-world applications.
"""

import timeit
import random
from typing import List, Dict, Any

from .binary_heap import BinaryHeap, HeapNode
from .priority_queue import PriorityQueue, PriorityQueueItem
from .heap_sort import heap_sort, heap_sort_inplace, benchmark_heap_sort, verify_heap_sort_correctness
from .analyzer import HeapAnalyzer, PerformanceMetrics
from .applications import (
    TaskScheduler, Task, TopKElements, MedianFinder, 
    SlidingWindowMax, EventSimulator
)

def demonstrate_basic_heap_operations() -> None:
    """Demonstrate basic heap operations with timing."""
    print("=== Basic Heap Operations ===")
    
    # Create min heap
    heap = BinaryHeap[int](heap_type="min")
    
    # Add elements with timing
    elements = [10, 4, 15, 20, 30, 40, 50, 60, 70, 80, 100]
    
    print("Adding elements to min-heap:")
    for element in elements:
        start_time = timeit.default_timer()
        heap.push(element)
        end_time = timeit.default_timer()
        print(f"  Added {element} in {(end_time - start_time) * 1_000_000:.2f} μs")
    
    print(f"\nHeap after insertion: {heap}")
    print(f"Peek (min element): {heap.peek()}")
    print(f"Heap is valid: {heap.is_valid()}")
    
    # Extract elements with timing
    print("\nExtracting elements in order:")
    extracted = []
    while not heap.is_empty():
        start_time = timeit.default_timer()
        value = heap.pop()
        end_time = timeit.default_timer()
        extracted.append(value)
        print(f"  Extracted {value} in {(end_time - start_time) * 1_000_000:.2f} μs")
    
    print(f"Extracted order: {extracted}")
    print(f"Correct order: {sorted(elements)}")
    print(f"Order correct: {extracted == sorted(elements)}")
    print()

def demonstrate_max_heap() -> None:
    """Demonstrate max heap operations."""
    print("=== Max Heap Operations ===")
    
    # Create max heap
    heap = BinaryHeap[int](heap_type="max")
    
    # Add elements
    elements = [10, 4, 15, 20, 30, 40, 50, 60, 70, 80, 100]
    for element in elements:
        heap.push(element)
    
    print(f"Max heap: {heap}")
    print(f"Peek (max element): {heap.peek()}")
    
    # Extract elements
    print("\nExtracting elements in descending order:")
    extracted = []
    while not heap.is_empty():
        extracted.append(heap.pop())
    
    print(f"Extracted order: {extracted}")
    print(f"Expected order: {sorted(elements, reverse=True)}")
    print(f"Order correct: {extracted == sorted(elements, reverse=True)}")
    print()

def demonstrate_heapify_methods() -> None:
    """Demonstrate different heapify methods with timing."""
    print("=== Heapify Methods Comparison ===")
    
    # Generate test data
    data = [random.randint(1, 1000) for _ in range(1000)]
    
    # Method 1: Push-based heapify
    start_time = timeit.default_timer()
    heap1 = BinaryHeap[int](heap_type="min")
    for item in data:
        heap1.push(item)
    push_time = timeit.default_timer() - start_time
    
    # Method 2: Bottom-up heapify
    start_time = timeit.default_timer()
    heap2 = BinaryHeap[int](heap_type="min")
    heap2.heapify_bottom_up(data)
    bottom_up_time = timeit.default_timer() - start_time
    
    print(f"Push-based heapify: {push_time * 1000:.2f} ms")
    print(f"Bottom-up heapify: {bottom_up_time * 1000:.2f} ms")
    print(f"Speedup: {push_time / bottom_up_time:.2f}x")
    
    # Verify both methods produce same result
    result1 = []
    while not heap1.is_empty():
        result1.append(heap1.pop())
    
    result2 = []
    while not heap2.is_empty():
        result2.append(heap2.pop())
    
    print(f"Results identical: {result1 == result2}")
    print()

def demonstrate_priority_queue() -> None:
    """Demonstrate priority queue operations."""
    print("=== Priority Queue Operations ===")
    
    # Create priority queue (max heap for higher priority first)
    pq = PriorityQueue[str](max_heap=True)
    
    # Add tasks with different priorities
    tasks = [
        ("Low priority task", 1),
        ("High priority task", 10),
        ("Medium priority task", 5),
        ("Critical task", 15),
        ("Minor task", 2)
    ]
    
    print("Adding tasks to priority queue:")
    for task, priority in tasks:
        start_time = timeit.default_timer()
        pq.put(task, priority)
        end_time = timeit.default_timer()
        print(f"  Added '{task}' (priority {priority}) in {(end_time - start_time) * 1_000_000:.2f} μs")
    
    print(f"\nQueue size: {len(pq)}")
    print(f"Next task: {pq.peek()}")
    
    # Process tasks in priority order
    print("\nProcessing tasks in priority order:")
    processed = []
    while not pq.is_empty():
        start_time = timeit.default_timer()
        task = pq.get()
        end_time = timeit.default_timer()
        processed.append(task)
        print(f"  Processed '{task}' in {(end_time - start_time) * 1_000_000:.2f} μs")
    
    print(f"Processing order: {processed}")
    print()

def demonstrate_heap_sort() -> None:
    """Demonstrate heap sort with timing."""
    print("=== Heap Sort Demonstration ===")
    
    # Test data
    data = [64, 34, 25, 12, 22, 11, 90, 45, 67, 89, 23, 56, 78, 90, 12]
    print(f"Original data: {data}")
    
    # Functional heap sort
    start_time = timeit.default_timer()
    sorted_asc = heap_sort(data)
    func_time = timeit.default_timer() - start_time
    
    # In-place heap sort
    data_copy = data.copy()
    start_time = timeit.default_timer()
    heap_sort_inplace(data_copy)
    inplace_time = timeit.default_timer() - start_time
    
    # Built-in sort for comparison
    start_time = timeit.default_timer()
    builtin_sorted = sorted(data)
    builtin_time = timeit.default_timer() - start_time
    
    print(f"Functional heap sort: {sorted_asc}")
    print(f"In-place heap sort: {data_copy}")
    print(f"Built-in sort: {builtin_sorted}")
    
    print(f"\nTiming comparison:")
    print(f"  Functional heap sort: {func_time * 1000:.3f} ms")
    print(f"  In-place heap sort: {inplace_time * 1000:.3f} ms")
    print(f"  Built-in sort: {builtin_time * 1000:.3f} ms")
    
    print(f"\nCorrectness check:")
    print(f"  Functional correct: {sorted_asc == builtin_sorted}")
    print(f"  In-place correct: {data_copy == builtin_sorted}")
    print()

def demonstrate_task_scheduling() -> None:
    """Demonstrate task scheduling using priority queues."""
    print("=== Task Scheduling Demonstration ===")
    
    scheduler = TaskScheduler()
    
    # Add tasks with different priorities and durations
    tasks = [
        ("High priority bug fix", 10, 2.0),
        ("Low priority documentation", 3, 1.0),
        ("Medium priority feature", 7, 3.0),
        ("Critical security patch", 15, 1.5),
        ("Minor UI improvement", 5, 0.5),
        ("Database optimization", 8, 4.0),
        ("Code review", 6, 1.0)
    ]
    
    print("Adding tasks to scheduler:")
    for task_name, priority, duration in tasks:
        task_id = scheduler.add_task(task_name, priority, duration)
        print(f"  Added task {task_id}: {task_name} (priority {priority}, duration {duration}h)")
    
    print(f"\nTotal tasks in queue: {len(scheduler)}")
    
    # Process tasks
    print("\nProcessing tasks in priority order:")
    completed = scheduler.run_scheduler()
    
    for task in completed:
        print(f"  Completed: {task.name} (priority {task.priority}, duration {task.duration}h)")
    
    print(f"\nTotal simulation time: {scheduler.get_current_time():.1f} hours")
    print()

def demonstrate_top_k_elements() -> None:
    """Demonstrate finding top K elements using heaps."""
    print("=== Top K Elements Demonstration ===")
    
    # Generate random data
    data = [random.randint(1, 1000) for _ in range(100)]
    print(f"Generated {len(data)} random numbers")
    
    # Find top 5 largest elements
    print("\nFinding top 5 largest elements:")
    top_k_largest = TopKElements(5, find_largest=True)
    
    start_time = timeit.default_timer()
    for value in data:
        top_k_largest.add(value)
    end_time = timeit.default_timer()
    
    largest_5 = top_k_largest.get_top_k()
    print(f"Top 5 largest: {largest_5}")
    print(f"Time taken: {(end_time - start_time) * 1000:.3f} ms")
    
    # Find top 5 smallest elements
    print("\nFinding top 5 smallest elements:")
    top_k_smallest = TopKElements(5, find_largest=False)
    
    start_time = timeit.default_timer()
    for value in data:
        top_k_smallest.add(value)
    end_time = timeit.default_timer()
    
    smallest_5 = top_k_smallest.get_top_k()
    print(f"Top 5 smallest: {smallest_5}")
    print(f"Time taken: {(end_time - start_time) * 1000:.3f} ms")
    
    # Verify correctness
    sorted_data = sorted(data)
    expected_largest = sorted_data[-5:][::-1]
    expected_smallest = sorted_data[:5]
    
    print(f"\nCorrectness check:")
    print(f"  Largest 5 correct: {largest_5 == expected_largest}")
    print(f"  Smallest 5 correct: {smallest_5 == expected_smallest}")
    print()

def demonstrate_median_finder() -> None:
    """Demonstrate median finding using two heaps."""
    print("=== Median Finder Demonstration ===")
    
    median_finder = MedianFinder()
    
    # Add numbers and track median
    numbers = [5, 10, 2, 3, 7, 8, 1, 9, 4, 6]
    
    print("Adding numbers and tracking median:")
    for num in numbers:
        median_finder.add_num(num)
        current_median = median_finder.find_median()
        print(f"  Added {num}, Median: {current_median}")
    
    # Verify final median
    sorted_numbers = sorted(numbers)
    expected_median = sorted_numbers[len(sorted_numbers) // 2] if len(sorted_numbers) % 2 == 1 else \
                     (sorted_numbers[len(sorted_numbers) // 2 - 1] + sorted_numbers[len(sorted_numbers) // 2]) / 2
    
    final_median = median_finder.find_median()
    print(f"\nFinal median: {final_median}")
    print(f"Expected median: {expected_median}")
    print(f"Correct: {abs(final_median - expected_median) < 0.001}")
    print()

def demonstrate_sliding_window_max() -> None:
    """Demonstrate sliding window maximum using heaps."""
    print("=== Sliding Window Maximum Demonstration ===")
    
    # Test data
    values = [1, 3, -1, -3, 5, 3, 6, 7]
    window_size = 3
    
    print(f"Values: {values}")
    print(f"Window size: {window_size}")
    
    # Find maximum in each sliding window
    sliding_max = SlidingWindowMax(window_size)
    
    start_time = timeit.default_timer()
    max_values = sliding_max.get_max_in_window(values)
    end_time = timeit.default_timer()
    
    print(f"Maximum values in each window: {max_values}")
    print(f"Time taken: {(end_time - start_time) * 1000:.3f} ms")
    
    # Verify manually
    expected = []
    for i in range(len(values) - window_size + 1):
        window = values[i:i + window_size]
        expected.append(max(window))
    
    print(f"Expected: {expected}")
    print(f"Correct: {max_values == expected}")
    print()

def demonstrate_event_simulation() -> None:
    """Demonstrate event simulation using priority queues."""
    print("=== Event Simulation Demonstration ===")
    
    simulator = EventSimulator()
    
    # Add various events
    events = [
        ("user_login", 5, 0.1),
        ("database_query", 3, 0.5),
        ("critical_error", 10, 0.2),
        ("file_upload", 4, 2.0),
        ("email_send", 2, 0.3),
        ("system_backup", 8, 10.0),
        ("cache_update", 6, 0.1)
    ]
    
    print("Adding events to simulator:")
    for event_type, priority, processing_time in events:
        event_id = simulator.add_event(event_type, priority, processing_time)
        print(f"  Added event {event_id}: {event_type} (priority {priority}, time {processing_time}s)")
    
    # Run simulation
    print(f"\nRunning simulation...")
    start_time = timeit.default_timer()
    processed_events = simulator.run_simulation()
    end_time = timeit.default_timer()
    
    print(f"Simulation completed in {(end_time - start_time) * 1000:.3f} ms")
    
    # Show results
    print(f"\nProcessed events:")
    for event in processed_events:
        print(f"  {event.event_type} (priority {event.priority}, time {event.processing_time}s)")
    
    # Show statistics
    stats = simulator.get_statistics()
    print(f"\nSimulation statistics:")
    print(f"  Total events: {stats['total_events']}")
    print(f"  Total time: {stats['total_time']:.2f}s")
    print(f"  Average processing time: {stats['avg_processing_time']:.2f}s")
    print(f"  Event type distribution: {stats['event_type_distribution']}")
    print()

def demonstrate_performance_analysis() -> None:
    """Demonstrate performance analysis and comparison with heapq."""
    print("=== Performance Analysis ===")
    
    # Generate performance report
    print("Generating performance report...")
    start_time = timeit.default_timer()
    report = HeapAnalyzer.generate_performance_report()
    end_time = timeit.default_timer()
    
    print(f"Report generation time: {(end_time - start_time) * 1000:.2f} ms")
    print("\n" + report)
    
    # Memory analysis
    print("\nMemory Usage Analysis:")
    heap = BinaryHeap[str]()
    
    # Add some items
    items = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    for item in items:
        heap.push(item, len(item))  # Priority based on string length
    
    memory_info = HeapAnalyzer.analyze_memory_usage(heap)
    
    print(f"  Number of elements: {memory_info['num_elements']}")
    print(f"  Heap array size: {memory_info['heap_array_size']} bytes")
    print(f"  Total node size: {memory_info['total_node_size']} bytes")
    print(f"  Total data size: {memory_info['total_data_size']} bytes")
    print(f"  Total memory: {memory_info['total_size']} bytes")
    print(f"  Memory per element: {memory_info['total_size'] / memory_info['num_elements']:.1f} bytes")
    print()

def demonstrate_heap_sort_benchmark() -> None:
    """Demonstrate heap sort benchmarking."""
    print("=== Heap Sort Benchmark ===")
    
    # Run heap sort benchmark
    data_sizes = [100, 1000, 10000]
    print("Running heap sort benchmark...")
    
    start_time = timeit.default_timer()
    benchmark_results = benchmark_heap_sort(data_sizes, iterations=50)
    end_time = timeit.default_timer()
    
    print(f"Benchmark completed in {(end_time - start_time) * 1000:.2f} ms")
    
    print("\nBenchmark Results:")
    for size, results in benchmark_results.items():
        print(f"\nSize {size}:")
        print(f"  Functional heap sort: {results['functional_heap_sort'] * 1000:.3f} ms")
        print(f"  In-place heap sort: {results['inplace_heap_sort'] * 1000:.3f} ms")
        print(f"  Built-in sort: {results['builtin_sort'] * 1000:.3f} ms")
        print(f"  Functional vs Built-in: {results['func_vs_builtin_ratio']:.2f}x")
        print(f"  In-place vs Built-in: {results['inplace_vs_builtin_ratio']:.2f}x")
    
    # Verify correctness
    print(f"\nCorrectness verification:")
    is_correct = verify_heap_sort_correctness()
    print(f"  All tests passed: {is_correct}")
    print()

def main() -> None:
    """Main demonstration function."""
    print("Binary Heap & Priority Queues Demonstration")
    print("=" * 60)
    print()
    
    # Run all demonstrations
    demonstrations = [
        demonstrate_basic_heap_operations,
        demonstrate_max_heap,
        demonstrate_heapify_methods,
        demonstrate_priority_queue,
        demonstrate_heap_sort,
        demonstrate_task_scheduling,
        demonstrate_top_k_elements,
        demonstrate_median_finder,
        demonstrate_sliding_window_max,
        demonstrate_event_simulation,
        demonstrate_performance_analysis,
        demonstrate_heap_sort_benchmark
    ]
    
    for i, demo in enumerate(demonstrations, 1):
        try:
            print(f"Running demonstration {i}/{len(demonstrations)}...")
            demo()
        except Exception as e:
            print(f"Error in demonstration {i}: {e}")
            import traceback
            traceback.print_exc()
        print("-" * 60)
        print()
    
    print("All demonstrations completed!")

if __name__ == "__main__":
    main() 