"""
Task scheduler using skip list priority queue.

This module demonstrates a real-world application of skip lists in
scheduling systems where tasks have priorities and deadlines.
"""

import timeit
from typing import List, Tuple, Optional
from .priority_queue import SkipListPriorityQueue

class TaskScheduler:
    """
    A task scheduler using skip list priority queue.
    
    This demonstrates a real-world application of skip lists in
    scheduling systems where tasks have priorities and deadlines.
    """
    
    def __init__(self):
        """Initialize the task scheduler."""
        self.priority_queue = SkipListPriorityQueue[int, str]()
        self.task_count = 0
    
    def add_task(self, task_name: str, priority: int) -> None:
        """
        Add a task to the scheduler.
        
        Args:
            task_name: Name of the task
            priority: Priority level (lower = higher priority)
        """
        # If task already exists, remove it first
        if task_name in self.priority_queue:
            self.priority_queue.remove(task_name)
            self.task_count -= 1
        
        # Add the new task
        self.priority_queue.put(priority, task_name)
        self.task_count += 1
        print(f"Added task: {task_name} with priority {priority}")
    
    def execute_next_task(self) -> Optional[str]:
        """
        Execute the next highest priority task.
        
        Returns:
            Name of the executed task, or None if no tasks available
        """
        if len(self.priority_queue) == 0:
            return None
        
        priority, task_name = self.priority_queue.get()
        self.task_count -= 1
        print(f"Executing task: {task_name} (priority: {priority})")
        return task_name
    
    def remove_task(self, task_name: str) -> bool:
        """
        Remove a specific task from the scheduler.
        
        Args:
            task_name: Name of the task to remove
            
        Returns:
            True if task was found and removed, False otherwise
        """
        if self.priority_queue.remove(task_name):
            self.task_count -= 1
            print(f"Removed task: {task_name}")
            return True
        return False
    
    def update_task_priority(self, task_name: str, new_priority: int) -> bool:
        """
        Update the priority of an existing task.
        
        Args:
            task_name: Name of the task to update
            new_priority: New priority value
            
        Returns:
            True if task was found and updated, False otherwise
        """
        if self.priority_queue.update_priority(task_name, new_priority):
            print(f"Updated task {task_name} priority to {new_priority}")
            return True
        return False
    
    def list_tasks(self) -> List[Tuple[int, str]]:
        """List all tasks in priority order."""
        return list(self.priority_queue)
    
    def get_task_count(self) -> int:
        """Get the number of pending tasks."""
        return self.task_count
    
    def get_task_priority(self, task_name: str) -> Optional[int]:
        """Get the priority of a specific task."""
        return self.priority_queue.get_priority(task_name)
    
    def peek_next_task(self) -> Optional[Tuple[int, str]]:
        """
        Peek at the next task without executing it.
        
        Returns:
            Tuple of (priority, task_name) or None if no tasks
        """
        if len(self.priority_queue) == 0:
            return None
        
        return self.priority_queue.peek()
    
    def clear_all_tasks(self) -> None:
        """Remove all tasks from the scheduler."""
        while len(self.priority_queue) > 0:
            self.priority_queue.get()
        self.task_count = 0
        print("Cleared all tasks")
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics for the scheduler."""
        return {
            'task_count': self.task_count,
            'queue_size': len(self.priority_queue),
            'is_empty': len(self.priority_queue) == 0
        }

def demonstrate_task_scheduler():
    """Demonstrate the task scheduler with performance analysis."""
    print("=== Task Scheduler Demonstration ===\n")
    
    # Create task scheduler
    scheduler = TaskScheduler()
    
    # Add some tasks with different priorities
    print("Adding tasks...")
    scheduler.add_task("Send email", 3)
    scheduler.add_task("Backup database", 1)
    scheduler.add_task("Update website", 2)
    scheduler.add_task("Review code", 4)
    scheduler.add_task("Fix critical bug", 0)
    
    # Show current task list
    print(f"\nCurrent tasks ({scheduler.get_task_count()}):")
    for priority, task in scheduler.list_tasks():
        print(f"  Priority {priority}: {task}")
    
    # Execute tasks in priority order
    print("\nExecuting tasks in priority order:")
    while scheduler.get_task_count() > 0:
        scheduler.execute_next_task()
    
    # Performance analysis
    print("\n=== Performance Analysis ===")
    
    # Benchmark task operations
    pq = SkipListPriorityQueue[int, str]()
    
    # Benchmark put operations
    put_time = timeit.timeit(
        lambda: (pq.put(i % 10, f"task{i}") for i in range(1000)),
        number=1
    )
    print(f"Put 1000 tasks: {put_time:.4f} seconds")
    
    # Benchmark get operations
    get_time = timeit.timeit(
        lambda: pq.get() if len(pq) > 0 else None,
        number=1000
    )
    print(f"Get 1000 tasks: {get_time:.4f} seconds")
    
    # Benchmark priority updates
    update_time = timeit.timeit(
        lambda: (pq.update_priority(f"task{i % 100}", i % 5) for i in range(100)),
        number=1
    )
    print(f"Update 100 task priorities: {update_time:.4f} seconds")
    
    # Memory analysis
    print("\n=== Memory Analysis ===")
    from .analyzer import SkipListAnalyzer
    analyzer = SkipListAnalyzer()
    memory_info = analyzer.analyze_memory(pq.skip_list)
    
    print(f"Skip list memory usage: {memory_info.total_size} bytes")
    print(f"Node count: {memory_info.node_count}")
    print(f"Average height: {memory_info.average_height:.2f}")
    print(f"Level distribution: {memory_info.level_distribution}")

def demonstrate_advanced_features():
    """Demonstrate advanced features of the task scheduler."""
    print("\n=== Advanced Features Demonstration ===\n")
    
    scheduler = TaskScheduler()
    
    # Add tasks
    tasks = [
        ("Low priority task", 10),
        ("Medium priority task", 5),
        ("High priority task", 1),
        ("Critical task", 0),
        ("Another medium task", 5)
    ]
    
    for task_name, priority in tasks:
        scheduler.add_task(task_name, priority)
    
    print(f"Added {scheduler.get_task_count()} tasks")
    
    # Peek at next task
    next_task = scheduler.peek_next_task()
    if next_task:
        priority, task_name = next_task
        print(f"Next task to execute: {task_name} (priority: {priority})")
    
    # Update priority
    print("\nUpdating task priorities...")
    scheduler.update_task_priority("Low priority task", 2)
    scheduler.update_task_priority("Another medium task", 8)
    
    # Show updated task list
    print(f"\nUpdated tasks ({scheduler.get_task_count()}):")
    for priority, task in scheduler.list_tasks():
        print(f"  Priority {priority}: {task}")
    
    # Remove a task
    print("\nRemoving a task...")
    scheduler.remove_task("Medium priority task")
    
    # Execute remaining tasks
    print("\nExecuting remaining tasks:")
    while scheduler.get_task_count() > 0:
        scheduler.execute_next_task()
    
    # Performance stats
    stats = scheduler.get_performance_stats()
    print(f"\nFinal stats: {stats}")

if __name__ == "__main__":
    demonstrate_task_scheduler()
    demonstrate_advanced_features() 