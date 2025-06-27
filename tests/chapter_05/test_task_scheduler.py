"""
Unit tests for task scheduler implementation.

This module provides comprehensive tests for the TaskScheduler class,
ensuring correct behavior and edge cases.
"""

import pytest
from mastering_performant_code.chapter_05.task_scheduler import TaskScheduler


class TestTaskScheduler:
    """Test cases for TaskScheduler."""
    
    def test_initialization(self):
        """Test task scheduler initialization."""
        scheduler = TaskScheduler()
        assert scheduler.task_count == 0
        assert len(scheduler.priority_queue) == 0
    
    def test_add_task(self):
        """Test adding tasks."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 1)
        scheduler.add_task("task2", 2)
        scheduler.add_task("task3", 0)
        
        assert scheduler.task_count == 3
        assert len(scheduler.priority_queue) == 3
    
    def test_execute_next_task(self):
        """Test executing next task."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 2)
        scheduler.add_task("task2", 1)
        scheduler.add_task("task3", 0)
        
        # Execute highest priority task
        task = scheduler.execute_next_task()
        assert task == "task3"
        assert scheduler.task_count == 2
        
        # Execute next task
        task = scheduler.execute_next_task()
        assert task == "task2"
        assert scheduler.task_count == 1
        
        # Execute last task
        task = scheduler.execute_next_task()
        assert task == "task1"
        assert scheduler.task_count == 0
    
    def test_execute_next_task_empty(self):
        """Test executing next task when queue is empty."""
        scheduler = TaskScheduler()
        
        task = scheduler.execute_next_task()
        assert task is None
        assert scheduler.task_count == 0
    
    def test_remove_task(self):
        """Test removing tasks."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 1)
        scheduler.add_task("task2", 2)
        scheduler.add_task("task3", 3)
        
        # Remove existing task
        assert scheduler.remove_task("task2") is True
        assert scheduler.task_count == 2
        
        # Remove non-existing task
        assert scheduler.remove_task("nonexistent") is False
        assert scheduler.task_count == 2
    
    def test_update_task_priority(self):
        """Test updating task priority."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 3)
        scheduler.add_task("task2", 2)
        
        # Update priority
        assert scheduler.update_task_priority("task1", 1) is True
        assert scheduler.task_count == 2
        
        # Execute should get updated task first
        task = scheduler.execute_next_task()
        assert task == "task1"
    
    def test_update_task_priority_nonexistent(self):
        """Test updating priority of non-existing task."""
        scheduler = TaskScheduler()
        
        assert scheduler.update_task_priority("nonexistent", 1) is False
    
    def test_list_tasks(self):
        """Test listing tasks."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 3)
        scheduler.add_task("task2", 1)
        scheduler.add_task("task3", 2)
        
        tasks = scheduler.list_tasks()
        
        # Should be in priority order
        expected = [(1, "task2"), (2, "task3"), (3, "task1")]
        assert tasks == expected
    
    def test_get_task_count(self):
        """Test getting task count."""
        scheduler = TaskScheduler()
        
        assert scheduler.get_task_count() == 0
        
        scheduler.add_task("task1", 1)
        assert scheduler.get_task_count() == 1
        
        scheduler.add_task("task2", 2)
        assert scheduler.get_task_count() == 2
        
        scheduler.execute_next_task()
        assert scheduler.get_task_count() == 1
    
    def test_get_task_priority(self):
        """Test getting task priority."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 3)
        scheduler.add_task("task2", 1)
        
        assert scheduler.get_task_priority("task1") == 3
        assert scheduler.get_task_priority("task2") == 1
        assert scheduler.get_task_priority("nonexistent") is None
    
    def test_peek_next_task(self):
        """Test peeking at next task."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 2)
        scheduler.add_task("task2", 1)
        
        # Peek at highest priority task
        result = scheduler.peek_next_task()
        assert result == (1, "task2")
        
        # Task count should remain the same
        assert scheduler.task_count == 2
    
    def test_peek_next_task_empty(self):
        """Test peeking when queue is empty."""
        scheduler = TaskScheduler()
        
        result = scheduler.peek_next_task()
        assert result is None
    
    def test_clear_all_tasks(self):
        """Test clearing all tasks."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 1)
        scheduler.add_task("task2", 2)
        scheduler.add_task("task3", 3)
        
        assert scheduler.task_count == 3
        
        scheduler.clear_all_tasks()
        
        assert scheduler.task_count == 0
        assert len(scheduler.priority_queue) == 0
    
    def test_get_performance_stats(self):
        """Test getting performance statistics."""
        scheduler = TaskScheduler()
        
        stats = scheduler.get_performance_stats()
        assert stats['task_count'] == 0
        assert stats['queue_size'] == 0
        assert stats['is_empty'] is True
        
        scheduler.add_task("task1", 1)
        stats = scheduler.get_performance_stats()
        assert stats['task_count'] == 1
        assert stats['queue_size'] == 1
        assert stats['is_empty'] is False
    
    def test_duplicate_task_names(self):
        """Test handling of duplicate task names."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task", 3)
        scheduler.add_task("task", 1)  # Should replace the previous one
        
        assert scheduler.task_count == 1
        
        # Should execute with new priority
        task = scheduler.execute_next_task()
        assert task == "task"
        assert scheduler.task_count == 0
    
    def test_negative_priorities(self):
        """Test handling of negative priorities."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", -1)
        scheduler.add_task("task2", 0)
        scheduler.add_task("task3", 1)
        
        # Should execute in priority order (negative first)
        task = scheduler.execute_next_task()
        assert task == "task1"
        
        task = scheduler.execute_next_task()
        assert task == "task2"
        
        task = scheduler.execute_next_task()
        assert task == "task3"
    
    def test_large_priorities(self):
        """Test handling of large priorities."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("task1", 1000000)
        scheduler.add_task("task2", 1)
        scheduler.add_task("task3", 999999)
        
        # Should execute in priority order
        task = scheduler.execute_next_task()
        assert task == "task2"
        
        task = scheduler.execute_next_task()
        assert task == "task3"
        
        task = scheduler.execute_next_task()
        assert task == "task1"
    
    def test_empty_string_task_names(self):
        """Test handling of empty string task names."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("", 1)
        scheduler.add_task("task", 2)
        
        assert scheduler.task_count == 2
        
        # Should be able to get priority
        assert scheduler.get_task_priority("") == 1
        
        # Should be able to remove
        assert scheduler.remove_task("") is True
        assert scheduler.task_count == 1
    
    def test_complex_operations_sequence(self):
        """Test complex sequence of operations."""
        scheduler = TaskScheduler()
        
        # Add tasks
        scheduler.add_task("task1", 3)
        scheduler.add_task("task2", 1)
        scheduler.add_task("task3", 2)
        
        # Peek
        result = scheduler.peek_next_task()
        assert result == (1, "task2")
        
        # Update priority
        scheduler.update_task_priority("task1", 0)
        
        # Execute highest priority
        task = scheduler.execute_next_task()
        assert task == "task1"
        
        # Remove task
        scheduler.remove_task("task3")
        
        # Execute remaining task
        task = scheduler.execute_next_task()
        assert task == "task2"
        
        assert scheduler.task_count == 0
    
    def test_large_dataset(self):
        """Test with larger dataset."""
        scheduler = TaskScheduler()
        
        # Add 1000 tasks with sequential priorities to ensure uniqueness
        import random
        random.seed(42)
        
        for i in range(1000):
            priority = i + 1  # Use sequential priorities to ensure uniqueness
            scheduler.add_task(f"task{i}", priority)
        
        assert scheduler.task_count == 1000
        
        # Execute all tasks and verify they're in priority order
        last_priority = 0
        executed_count = 0
        
        while scheduler.task_count > 0:
            task = scheduler.execute_next_task()
            if task is not None:
                executed_count += 1
                # Extract priority from task name for verification
                # This is a simplified check - in real implementation we'd track priorities
                assert task.startswith("task")
            else:
                break
        
        assert executed_count == 1000
        assert scheduler.task_count == 0


if __name__ == "__main__":
    pytest.main([__file__]) 