"""
Comprehensive demonstration of skip list functionality.

This module provides a complete demonstration of skip list features
including basic operations, performance analysis, and real-world applications.
"""

import timeit
import random
import sys
from typing import List, Dict, Set
from skip_list import SkipList, SkipListWithStats
from priority_queue import SkipListPriorityQueue
from analyzer import SkipListAnalyzer
from task_scheduler import TaskScheduler

def demonstrate_basic_operations():
    """Demonstrate basic skip list operations."""
    print("=== Basic Skip List Operations ===\n")
    
    # Create skip list
    skip_list = SkipList[int]()
    
    # Insert elements
    print("Inserting elements...")
    elements = [3, 6, 7, 9, 12, 19, 17, 26, 21, 25]
    for element in elements:
        skip_list.insert(element)
        print(f"Inserted {element}, size: {len(skip_list)}")
    
    # Search for elements
    print(f"\nSearching for elements...")
    search_targets = [7, 19, 5, 25, 30]
    for target in search_targets:
        result = skip_list.search(target)
        if result is not None:
            print(f"Found {target}")
        else:
            print(f"Not found: {target}")
    
    # Range query
    print(f"\nRange query [10, 20):")
    range_results = list(skip_list.range_query(10, 20))
    print(f"Elements in range: {range_results}")
    
    # Delete elements
    print(f"\nDeleting elements...")
    delete_targets = [7, 19, 25]
    for target in delete_targets:
        if skip_list.delete(target):
            print(f"Deleted {target}, size: {len(skip_list)}")
        else:
            print(f"Could not delete {target}")
    
    # Show final state
    print(f"\nFinal skip list: {list(skip_list)}")
    print(f"Level distribution: {skip_list.get_level_distribution()}")

def demonstrate_performance_analysis():
    """Demonstrate performance analysis capabilities."""
    print("\n=== Performance Analysis ===\n")
    
    # Create skip list with statistics
    skip_list = SkipListWithStats[int]()
    
    # Insert random data
    print("Inserting 1000 random elements...")
    random.seed(42)  # For reproducible results
    test_data = list(range(1000))
    random.shuffle(test_data)
    
    for element in test_data:
        skip_list.insert(element)
    
    # Perform some operations
    print("Performing search operations...")
    for i in range(100):
        skip_list.search(i * 10)
    
    print("Performing delete operations...")
    for i in range(50):
        skip_list.delete(i * 20)
    
    # Get statistics
    stats = skip_list.get_stats()
    print(f"\nPerformance Statistics:")
    print(f"  Searches: {stats['searches']}")
    print(f"  Inserts: {stats['inserts']}")
    print(f"  Deletes: {stats['deletes']}")
    print(f"  Average search time: {stats.get('avg_search_time', 0):.8f} seconds")
    print(f"  Average insert time: {stats.get('avg_insert_time', 0):.8f} seconds")
    print(f"  Average delete time: {stats.get('avg_delete_time', 0):.8f} seconds")
    
    # Height distribution
    print(f"\nHeight Distribution:")
    for height, count in stats['height_distribution'].items():
        print(f"  Height {height}: {count} nodes")

def demonstrate_priority_queue():
    """Demonstrate skip list priority queue."""
    print("\n=== Skip List Priority Queue ===\n")
    
    # Create priority queue
    pq = SkipListPriorityQueue[int, str]()
    
    # Add tasks with different priorities
    tasks = [
        (3, "Send email"),
        (1, "Backup database"),
        (2, "Update website"),
        (4, "Review code"),
        (0, "Fix critical bug")
    ]
    
    print("Adding tasks to priority queue...")
    for priority, task in tasks:
        pq.put(priority, task)
        print(f"Added: {task} (priority: {priority})")
    
    # Show all tasks in priority order
    print(f"\nAll tasks in priority order:")
    for priority, task in pq:
        print(f"  Priority {priority}: {task}")
    
    # Execute tasks
    print(f"\nExecuting tasks in priority order:")
    while len(pq) > 0:
        priority, task = pq.get()
        print(f"  Executing: {task} (priority: {priority})")
    
    # Demonstrate priority updates
    print(f"\nDemonstrating priority updates...")
    pq.put(5, "Low priority task")
    pq.put(1, "High priority task")
    
    print(f"Before update: {list(pq)}")
    pq.update_priority("Low priority task", 0)
    print(f"After update: {list(pq)}")

def demonstrate_task_scheduler():
    """Demonstrate the task scheduler application."""
    print("\n=== Task Scheduler Application ===\n")
    
    # Create task scheduler
    scheduler = TaskScheduler()
    
    # Add various tasks
    print("Adding tasks to scheduler...")
    scheduler.add_task("Send email", 3)
    scheduler.add_task("Backup database", 1)
    scheduler.add_task("Update website", 2)
    scheduler.add_task("Review code", 4)
    scheduler.add_task("Fix critical bug", 0)
    scheduler.add_task("Update documentation", 5)
    
    # Show current state
    print(f"\nCurrent tasks ({scheduler.get_task_count()}):")
    for priority, task in scheduler.list_tasks():
        print(f"  Priority {priority}: {task}")
    
    # Peek at next task
    next_task = scheduler.peek_next_task()
    if next_task:
        priority, task_name = next_task
        print(f"\nNext task to execute: {task_name} (priority: {priority})")
    
    # Update some priorities
    print(f"\nUpdating task priorities...")
    scheduler.update_task_priority("Send email", 1)
    scheduler.update_task_priority("Update documentation", 2)
    
    # Execute a few tasks
    print(f"\nExecuting first 3 tasks:")
    for i in range(3):
        if scheduler.get_task_count() > 0:
            scheduler.execute_next_task()
    
    # Show remaining tasks
    print(f"\nRemaining tasks ({scheduler.get_task_count()}):")
    for priority, task in scheduler.list_tasks():
        print(f"  Priority {priority}: {task}")

def demonstrate_benchmarks():
    """Demonstrate comprehensive benchmarking."""
    print("\n=== Comprehensive Benchmarks ===\n")
    
    # Test data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"Testing with {size} elements:")
        print("-" * 40)
        
        # Prepare test data
        test_data = list(range(size))
        random.shuffle(test_data)
        
        # Skip List operations
        print("Skip List Operations:")
        
        # Insert operations
        skip_insert = timeit.timeit(
            f"sl.insert(i) for i in test_data",
            setup=f"from chapter_05 import SkipList; sl = SkipList(); test_data = {test_data}",
            number=1
        )
        
        # Search operations
        skip_search = timeit.timeit(
            "sl.search(i) for i in range(0, size, 10)",
            setup=f"from chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in {test_data}]",
            number=100
        )
        
        # Delete operations
        skip_delete = timeit.timeit(
            "sl.delete(i) for i in range(0, size, 10)",
            setup=f"from chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in {test_data}]",
            number=1
        )
        
        print(f"  Insert {size} items: {skip_insert:.6f} seconds")
        print(f"  Search {size//10} items: {skip_search:.6f} seconds")
        print(f"  Delete {size//10} items: {skip_delete:.6f} seconds")
        
        # List operations (for comparison)
        print("\nList Operations:")
        
        # Insert operations (append)
        list_insert = timeit.timeit(
            f"lst.append(i) for i in test_data",
            setup=f"lst = []; test_data = {test_data}",
            number=1
        )
        
        # Search operations (linear search)
        list_search = timeit.timeit(
            "i in lst for i in range(0, size, 10)",
            setup=f"lst = {test_data}",
            number=100
        )
        
        # Delete operations (remove)
        list_delete = timeit.timeit(
            "lst.remove(i) for i in range(0, size, 10) if i in lst",
            setup=f"lst = {test_data.copy()}",
            number=1
        )
        
        print(f"  Insert {size} items: {list_insert:.6f} seconds")
        print(f"  Search {size//10} items: {list_search:.6f} seconds")
        print(f"  Delete {size//10} items: {list_delete:.6f} seconds")
        
        # Performance ratios
        print(f"\nPerformance Ratios (Skip List / List):")
        print(f"  Insert: {skip_insert/list_insert:.2f}x")
        print(f"  Search: {skip_search/list_search:.2f}x")
        print(f"  Delete: {skip_delete/list_delete:.2f}x")
        
        print("\n" + "="*50 + "\n")

def demonstrate_memory_analysis():
    """Demonstrate memory usage analysis."""
    print("\n=== Memory Usage Analysis ===\n")
    
    # Test with different data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"Memory usage with {size} elements:")
        print("-" * 40)
        
        # Skip list
        skip_list = SkipList()
        for i in range(size):
            skip_list.insert(i)
        
        analyzer = SkipListAnalyzer()
        skip_memory = analyzer.analyze_memory(skip_list)
        
        # List (for comparison)
        lst = list(range(size))
        list_memory = sys.getsizeof(lst)
        
        # Set (for comparison)
        st = set(range(size))
        set_memory = sys.getsizeof(st)
        
        print(f"Skip List:")
        print(f"  Total memory: {skip_memory.total_size} bytes")
        print(f"  Node count: {skip_memory.node_count}")
        print(f"  Average height: {skip_memory.average_height:.2f}")
        
        print(f"List:")
        print(f"  Memory: {list_memory} bytes")
        print(f"  Ratio: {skip_memory.total_size/list_memory:.2f}x")
        
        print(f"Set:")
        print(f"  Memory: {set_memory} bytes")
        print(f"  Ratio: {skip_memory.total_size/set_memory:.2f}x")
        
        print()

def demonstrate_height_distribution():
    """Demonstrate height distribution analysis."""
    print("\n=== Height Distribution Analysis ===\n")
    
    # Test different probabilities
    probabilities = [0.25, 0.5, 0.75]
    sizes = [1000, 10000]
    
    for prob in probabilities:
        print(f"Probability: {prob}")
        print("-" * 30)
        
        for size in sizes:
            # Create skip list with specific probability
            skip_list = SkipList(max_height=16, probability=prob)
            
            # Insert random data
            test_data = list(range(size))
            random.shuffle(test_data)
            for item in test_data:
                skip_list.insert(item)
            
            # Analyze height distribution
            distribution = skip_list.get_level_distribution()
            
            print(f"  Size {size}:")
            for level, count in enumerate(distribution[:8]):  # Show first 8 levels
                if count > 0:
                    percentage = (count / size) * 100
                    print(f"    Level {level}: {count} nodes ({percentage:.1f}%)")
            
            print()
        
        print()

def demonstrate_range_queries():
    """Demonstrate range query performance."""
    print("\n=== Range Query Performance ===\n")
    
    # Test different data sizes
    sizes = [1000, 10000, 100000]
    
    for size in sizes:
        print(f"Testing with {size} elements:")
        print("-" * 40)
        
        # Create skip list with data
        skip_list = SkipList()
        test_data = list(range(size))
        random.shuffle(test_data)
        for item in test_data:
            skip_list.insert(item)
        
        # Test different range sizes
        range_sizes = [10, 100, 1000]
        
        for range_size in range_sizes:
            if range_size >= size:
                continue
            
            # Benchmark range queries
            start = size // 4
            end = start + range_size
            
            range_time = timeit.timeit(
                f"list(sl.range_query({start}, {end}))",
                setup=f"from chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in range({size})]",
                number=100
            )
            
            print(f"  Range [{start}, {end}): {range_time:.6f} seconds")
        
        print()

def main():
    """Run all demonstrations."""
    print("Skip List Comprehensive Demonstration")
    print("=" * 50)
    
    # Run all demonstrations
    demonstrate_basic_operations()
    demonstrate_performance_analysis()
    demonstrate_priority_queue()
    demonstrate_task_scheduler()
    demonstrate_benchmarks()
    demonstrate_memory_analysis()
    demonstrate_height_distribution()
    demonstrate_range_queries()
    
    print("\nDemonstration complete!")

if __name__ == "__main__":
    main() 
