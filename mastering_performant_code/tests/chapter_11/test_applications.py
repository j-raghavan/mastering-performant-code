"""
Tests for Real-World Applications

This module provides comprehensive tests for the real-world applications
using heaps and priority queues.
"""

import pytest
import random
from typing import List
from chapter_11.applications import (
    TaskScheduler, Task, TopKElements, MedianFinder, 
    SlidingWindowMax, EventSimulator
)


class TestTaskScheduler:
    """Test cases for TaskScheduler class."""
    
    def test_task_scheduler_initialization(self):
        """Test TaskScheduler initialization."""
        scheduler = TaskScheduler()
        assert len(scheduler) == 0
        assert scheduler.is_empty()
        assert scheduler._task_id_counter == 0
    
    def test_task_scheduler_add_task(self):
        """Test adding tasks to scheduler."""
        scheduler = TaskScheduler()
        
        task_id1 = scheduler.add_task("Task 1", 5, 2.0)
        task_id2 = scheduler.add_task("Task 2", 3, 1.0)
        task_id3 = scheduler.add_task("Task 3", 7, 3.0)
        
        assert task_id1 == 0
        assert task_id2 == 1
        assert task_id3 == 2
        assert len(scheduler) == 3
        assert not scheduler.is_empty()
    
    def test_task_scheduler_get_next_task(self):
        """Test getting next task from scheduler."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("Low priority", 3, 1.0)
        scheduler.add_task("High priority", 7, 2.0)
        scheduler.add_task("Medium priority", 5, 1.5)
        
        # Should get highest priority task first
        task = scheduler.get_next_task()
        assert task.name == "High priority"
        assert task.priority == 7
        assert task.duration == 2.0
        
        task = scheduler.get_next_task()
        assert task.name == "Medium priority"
        assert task.priority == 5
        
        task = scheduler.get_next_task()
        assert task.name == "Low priority"
        assert task.priority == 3
        
        assert scheduler.is_empty()
    
    def test_task_scheduler_peek_next_task(self):
        """Test peeking at next task without removing it."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("Task 1", 5, 2.0)
        scheduler.add_task("Task 2", 3, 1.0)
        
        # Peek should not remove the task
        task = scheduler.peek_next_task()
        assert task.name == "Task 1"  # Highest priority first
        assert len(scheduler) == 2
        
        # Get should remove the task
        task = scheduler.get_next_task()
        assert task.name == "Task 1"
        assert len(scheduler) == 1
    
    def test_task_scheduler_execute_task(self):
        """Test executing a task."""
        scheduler = TaskScheduler()
        
        task_id = scheduler.add_task("Test task", 5, 2.0)
        task = scheduler.get_next_task()
        
        initial_time = scheduler.get_current_time()
        scheduler.execute_task(task)
        final_time = scheduler.get_current_time()
        
        assert final_time == initial_time + 2.0
        assert len(scheduler.get_completed_tasks()) == 1
        assert scheduler.get_completed_tasks()[0].name == "Test task"
    
    def test_task_scheduler_run_scheduler(self):
        """Test running the scheduler."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("Task 1", 5, 1.0)
        scheduler.add_task("Task 2", 3, 2.0)
        scheduler.add_task("Task 3", 7, 0.5)
        
        completed = scheduler.run_scheduler()
        
        assert len(completed) == 3
        assert completed[0].name == "Task 3"  # Highest priority first
        assert completed[1].name == "Task 1"
        assert completed[2].name == "Task 2"
        
        assert scheduler.get_current_time() == 3.5  # 0.5 + 1.0 + 2.0
    
    def test_task_scheduler_run_scheduler_with_limit(self):
        """Test running the scheduler with a limit."""
        scheduler = TaskScheduler()
        
        scheduler.add_task("Task 1", 5, 1.0)
        scheduler.add_task("Task 2", 3, 2.0)
        scheduler.add_task("Task 3", 7, 0.5)
        
        completed = scheduler.run_scheduler(max_tasks=2)
        
        assert len(completed) == 2
        assert completed[0].name == "Task 3"
        assert completed[1].name == "Task 1"
        assert len(scheduler) == 1  # Task 2 still in queue
    
    def test_task_scheduler_empty_queue(self):
        """Test scheduler behavior with empty queue."""
        scheduler = TaskScheduler()
        
        assert scheduler.get_next_task() is None
        assert scheduler.peek_next_task() is None
        assert scheduler.run_scheduler() == []
        assert scheduler.get_current_time() == 0.0


class TestTopKElements:
    """Test cases for TopKElements class."""
    
    def test_top_k_elements_initialization(self):
        """Test TopKElements initialization."""
        top_k = TopKElements(5, find_largest=True)
        assert top_k.k == 5
        assert top_k.find_largest is True
        assert len(top_k._heap) == 0
    
    def test_top_k_elements_find_largest(self):
        """Test finding largest K elements."""
        top_k = TopKElements(3, find_largest=True)
        
        # Add elements
        elements = [10, 5, 15, 3, 7, 20, 1]
        for element in elements:
            top_k.add(element)
        
        result = top_k.get_top_k()
        assert len(result) == 3
        assert result == [20, 15, 10]  # Largest 3 elements
    
    def test_top_k_elements_find_smallest(self):
        """Test finding smallest K elements."""
        top_k = TopKElements(3, find_largest=False)
        
        # Add elements
        elements = [10, 5, 15, 3, 7, 20, 1]
        for element in elements:
            top_k.add(element)
        
        result = top_k.get_top_k()
        assert len(result) == 3
        assert result == [1, 3, 5]  # Smallest 3 elements
    
    def test_top_k_elements_less_than_k_elements(self):
        """Test behavior when fewer than K elements are added."""
        top_k = TopKElements(5, find_largest=True)
        
        top_k.add(10)
        top_k.add(5)
        top_k.add(15)
        
        result = top_k.get_top_k()
        assert len(result) == 3
        assert result == [15, 10, 5]
    
    def test_top_k_elements_replace_elements(self):
        """Test replacing elements when heap is full."""
        top_k = TopKElements(3, find_largest=True)
        
        # Add 5 elements, only top 3 should remain
        top_k.add(10)
        top_k.add(5)
        top_k.add(15)
        top_k.add(3)  # Should not be in top 3
        top_k.add(20)  # Should replace smallest in top 3
        
        result = top_k.get_top_k()
        assert len(result) == 3
        assert 20 in result
        assert 15 in result
        assert 10 in result
        assert 5 not in result
        assert 3 not in result
    
    def test_top_k_elements_clear(self):
        """Test clearing the top K elements finder."""
        top_k = TopKElements(3, find_largest=True)
        
        top_k.add(10)
        top_k.add(5)
        top_k.add(15)
        
        top_k.clear()
        result = top_k.get_top_k()
        assert len(result) == 0
    
    def test_top_k_elements_large_dataset(self):
        """Test TopKElements with large dataset."""
        top_k = TopKElements(10, find_largest=True)
        
        # Add 1000 random elements
        elements = [random.randint(1, 1000) for _ in range(1000)]
        for element in elements:
            top_k.add(element)
        
        result = top_k.get_top_k()
        assert len(result) == 10
        
        # Verify these are indeed the largest 10 elements
        sorted_elements = sorted(elements, reverse=True)
        expected_top_10 = sorted_elements[:10]
        assert result == expected_top_10


class TestMedianFinder:
    """Test cases for MedianFinder class."""
    
    def test_median_finder_initialization(self):
        """Test MedianFinder initialization."""
        finder = MedianFinder()
        assert len(finder._lower_heap) == 0
        assert len(finder._upper_heap) == 0
    
    def test_median_finder_basic_operations(self):
        """Test basic median finder operations."""
        finder = MedianFinder()
        
        finder.add_num(5)
        assert finder.find_median() == 5.0
        
        finder.add_num(10)
        assert finder.find_median() == 7.5  # (5 + 10) / 2
        
        finder.add_num(3)
        assert finder.find_median() == 5.0  # Middle element
    
    def test_median_finder_odd_even_numbers(self):
        """Test median finder with odd and even number of elements."""
        finder = MedianFinder()
        
        # Odd number of elements
        finder.add_num(1)
        finder.add_num(2)
        finder.add_num(3)
        assert finder.find_median() == 2.0
        
        # Even number of elements
        finder.add_num(4)
        assert finder.find_median() == 2.5  # (2 + 3) / 2
    
    def test_median_finder_negative_numbers(self):
        """Test median finder with negative numbers."""
        finder = MedianFinder()
        
        finder.add_num(-5)
        finder.add_num(10)
        finder.add_num(-3)
        
        assert finder.find_median() == -3.0
    
    def test_median_finder_empty_stream(self):
        """Test median finder with empty stream."""
        finder = MedianFinder()
        
        with pytest.raises(ValueError, match="No numbers in the stream"):
            finder.find_median()
    
    def test_median_finder_get_all_numbers(self):
        """Test getting all numbers in sorted order."""
        finder = MedianFinder()
        
        numbers = [5, 10, 3, 7, 1]
        for num in numbers:
            finder.add_num(num)
        
        result = finder.get_all_numbers()
        assert result == [1, 3, 5, 7, 10]
    
    def test_median_finder_large_dataset(self):
        """Test median finder with large dataset."""
        finder = MedianFinder()
        
        # Add 100 random numbers
        numbers = [random.randint(1, 100) for _ in range(100)]
        for num in numbers:
            finder.add_num(num)
        
        # Verify median is correct
        sorted_numbers = sorted(numbers)
        # For 100 elements, median is average of 50th and 51st elements (indices 49 and 50)
        expected_median = (sorted_numbers[49] + sorted_numbers[50]) / 2
        assert finder.find_median() == expected_median


class TestSlidingWindowMax:
    """Test cases for SlidingWindowMax class."""
    
    def test_sliding_window_max_initialization(self):
        """Test SlidingWindowMax initialization."""
        window = SlidingWindowMax(3)
        assert window.window_size == 3
        assert window._current_index == 0
    
    def test_sliding_window_max_basic_operations(self):
        """Test basic sliding window maximum operations."""
        window = SlidingWindowMax(3)
        
        # Add elements one by one
        assert window.add_element(1) is None  # Window not full yet
        assert window.add_element(3) is None  # Window not full yet
        assert window.add_element(2) == 3  # Window full, max is 3
        assert window.add_element(4) == 4  # Window full, max is 4
        assert window.add_element(1) == 4  # Window full, max is 4
    
    def test_sliding_window_max_get_max_in_window(self):
        """Test getting maximum values for all sliding windows."""
        window = SlidingWindowMax(3)
        
        values = [1, 3, -1, -3, 5, 3, 6, 7]
        result = window.get_max_in_window(values)
        
        expected = [3, 3, 5, 5, 6, 7]  # Max values for each window
        assert result == expected
    
    def test_sliding_window_max_window_size_one(self):
        """Test sliding window with size 1."""
        window = SlidingWindowMax(1)
        
        values = [1, 3, 2, 4]
        result = window.get_max_in_window(values)
        
        assert result == [1, 3, 2, 4]  # Each element is its own max
    
    def test_sliding_window_max_window_size_larger_than_data(self):
        """Test sliding window with size larger than data."""
        window = SlidingWindowMax(5)
        
        values = [1, 2, 3]
        result = window.get_max_in_window(values)
        
        assert result == []  # No complete windows
    
    def test_sliding_window_max_duplicate_values(self):
        """Test sliding window with duplicate values."""
        window = SlidingWindowMax(3)
        
        values = [1, 1, 1, 2, 2, 2]
        result = window.get_max_in_window(values)
        
        # Windows: [1,1,1], [1,1,2], [1,2,2], [2,2,2] -> max values: 1, 2, 2, 2
        assert result == [1, 2, 2, 2]
    
    def test_sliding_window_max_negative_values(self):
        """Test sliding window with negative values."""
        window = SlidingWindowMax(3)
        
        values = [-5, -3, -1, -7, -2]
        result = window.get_max_in_window(values)
        
        # Windows: [-5,-3,-1], [-3,-1,-7], [-1,-7,-2] -> max values: -1, -1, -1
        assert result == [-1, -1, -1]


class TestEventSimulator:
    """Test cases for EventSimulator class."""
    
    def test_event_simulator_initialization(self):
        """Test EventSimulator initialization."""
        simulator = EventSimulator()
        assert len(simulator._event_queue) == 0
        assert simulator._current_time == 0.0
        assert len(simulator._processed_events) == 0
        assert simulator._event_id_counter == 0
    
    def test_event_simulator_add_event(self):
        """Test adding events to simulator."""
        simulator = EventSimulator()
        
        event_id1 = simulator.add_event("login", 5, 0.1)
        event_id2 = simulator.add_event("query", 3, 0.5)
        event_id3 = simulator.add_event("error", 10, 0.2)
        
        assert event_id1 == 0
        assert event_id2 == 1
        assert event_id3 == 2
        assert len(simulator._event_queue) == 3
    
    def test_event_simulator_process_next_event(self):
        """Test processing next event."""
        simulator = EventSimulator()
        
        simulator.add_event("low_priority", 3, 1.0)
        simulator.add_event("high_priority", 7, 0.5)
        
        # Should process highest priority event first
        event = simulator.process_next_event()
        assert event.event_type == "high_priority"
        assert event.priority == 7
        assert event.processing_time == 0.5
        assert simulator._current_time == 0.5
        
        event = simulator.process_next_event()
        assert event.event_type == "low_priority"
        assert event.priority == 3
        assert simulator._current_time == 1.5
    
    def test_event_simulator_run_simulation(self):
        """Test running the event simulation."""
        simulator = EventSimulator()
        
        simulator.add_event("event1", 5, 1.0)
        simulator.add_event("event2", 3, 2.0)
        simulator.add_event("event3", 7, 0.5)
        
        processed = simulator.run_simulation()
        
        assert len(processed) == 3
        assert processed[0].event_type == "event3"  # Highest priority first
        assert processed[1].event_type == "event1"
        assert processed[2].event_type == "event2"
        
        assert simulator._current_time == 3.5  # 0.5 + 1.0 + 2.0
    
    def test_event_simulator_run_simulation_with_limit(self):
        """Test running simulation with a limit."""
        simulator = EventSimulator()
        
        simulator.add_event("event1", 5, 1.0)
        simulator.add_event("event2", 3, 2.0)
        simulator.add_event("event3", 7, 0.5)
        
        processed = simulator.run_simulation(max_events=2)
        
        assert len(processed) == 2
        assert processed[0].event_type == "event3"
        assert processed[1].event_type == "event1"
        assert len(simulator._event_queue) == 1  # event2 still in queue
    
    def test_event_simulator_get_statistics(self):
        """Test getting simulation statistics."""
        simulator = EventSimulator()
        
        simulator.add_event("login", 5, 0.1)
        simulator.add_event("query", 3, 0.5)
        simulator.add_event("error", 10, 0.2)
        simulator.add_event("login", 5, 0.1)
        
        simulator.run_simulation()
        
        stats = simulator.get_statistics()
        
        assert stats["total_events"] == 4
        assert stats["total_time"] == 0.9  # 0.2 + 0.1 + 0.5 + 0.1
        assert stats["avg_processing_time"] == 0.225  # 0.9 / 4
        assert stats["event_type_distribution"]["login"] == 2
        assert stats["event_type_distribution"]["query"] == 1
        assert stats["event_type_distribution"]["error"] == 1
    
    def test_event_simulator_empty_queue(self):
        """Test simulator behavior with empty queue."""
        simulator = EventSimulator()
        
        assert simulator.process_next_event() is None
        assert simulator.run_simulation() == []
        assert simulator.get_statistics() == {}


if __name__ == "__main__":
    pytest.main([__file__]) 