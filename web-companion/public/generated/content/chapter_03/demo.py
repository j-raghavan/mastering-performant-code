#!/usr/bin/env python3
"""
Demo script for Chapter 3: Dynamic Array with Manual Resizing

This script demonstrates the key features of the dynamic array implementations
and shows performance comparisons.
"""

import timeit
from dynamic_array import (
    DynamicArray,
    AdvancedDynamicArray,
    ProductionDynamicArray,
    GrowthStrategy
)
from applications import TextBuffer, SimpleDatabase, CircularBuffer


def demo_basic_dynamic_array():
    """Demonstrate basic dynamic array functionality."""
    print("=" * 60)
    print("BASIC DYNAMIC ARRAY DEMO")
    print("=" * 60)
    
    # Create a basic dynamic array
    arr = DynamicArray[int](initial_capacity=4)
    
    print(f"Initial capacity: {arr.capacity}")
    print(f"Initial size: {len(arr)}")
    print(f"Initial load factor: {arr.load_factor:.3f}")
    
    # Add elements
    for i in range(10):
        arr.append(i)
        print(f"After adding {i}: size={len(arr)}, capacity={arr.capacity}, load_factor={arr.load_factor:.3f}")
    
    print(f"\nFinal array: {arr}")
    print(f"Contains 5: {5 in arr}")
    print(f"Contains 15: {15 in arr}")


def demo_growth_strategies():
    """Demonstrate different growth strategies."""
    print("\n" + "=" * 60)
    print("GROWTH STRATEGIES COMPARISON")
    print("=" * 60)
    
    strategies = [
        GrowthStrategy.DOUBLING,
        GrowthStrategy.FIXED,
        GrowthStrategy.GOLDEN_RATIO,
        GrowthStrategy.ADAPTIVE
    ]
    
    for strategy in strategies:
        arr = AdvancedDynamicArray[int](strategy=strategy)
        capacities = [arr.capacity]
        
        # Add elements and track capacity changes
        for i in range(15):
            arr.append(i)
            if arr.capacity != capacities[-1]:
                capacities.append(arr.capacity)
        
        print(f"\n{strategy.value.upper()} Strategy:")
        print(f"  Capacity progression: {capacities}")
        print(f"  Final size: {len(arr)}")
        print(f"  Final capacity: {arr.capacity}")
        print(f"  Memory efficiency: {arr.memory_efficiency:.3f}")
        print(f"  Resize count: {arr.resize_count}")


def demo_text_buffer():
    """Demonstrate text buffer application."""
    print("\n" + "=" * 60)
    print("TEXT BUFFER APPLICATION")
    print("=" * 60)
    
    buffer = TextBuffer()
    
    # Add some lines
    buffer.append_line("Hello, World!")
    buffer.append_line("This is a test.")
    buffer.append_line("Dynamic arrays are cool!")
    
    print(f"Buffer has {buffer.line_count()} lines:")
    for i, line in enumerate(buffer.get_all_lines()):
        print(f"  Line {i}: {line}")
    
    # Insert a line
    buffer.insert_line(1, "Inserted line!")
    print(f"\nAfter inserting line 1:")
    for i, line in enumerate(buffer.get_all_lines()):
        print(f"  Line {i}: {line}")
    
    # Delete a line
    deleted = buffer.delete_line(2)
    print(f"\nDeleted line: '{deleted}'")
    print(f"After deletion:")
    for i, line in enumerate(buffer.get_all_lines()):
        print(f"  Line {i}: {line}")


def demo_database():
    """Demonstrate database application."""
    print("\n" + "=" * 60)
    print("SIMPLE DATABASE APPLICATION")
    print("=" * 60)
    
    db = SimpleDatabase()
    
    # Insert some records
    db.insert("Alice", 95.5)
    db.insert("Bob", 87.2)
    db.insert("Charlie", 92.1)
    db.insert("Alice", 88.9)  # Another Alice
    
    print(f"Database has {db.record_count()} records")
    
    # Get records by name
    alice_records = db.get_by_name("Alice")
    print(f"\nRecords for Alice: {alice_records}")
    
    # Get records by value range
    high_scores = db.get_by_value_range(90.0, 100.0)
    print(f"High scores (90+): {high_scores}")
    
    # Get statistics
    stats = db.get_stats()
    print(f"\nDatabase stats: {stats}")


def demo_circular_buffer():
    """Demonstrate circular buffer application."""
    print("\n" + "=" * 60)
    print("CIRCULAR BUFFER APPLICATION")
    print("=" * 60)
    
    buffer = CircularBuffer(5)
    
    print(f"Buffer capacity: {buffer.capacity()}")
    print(f"Buffer empty: {buffer.is_empty()}")
    print(f"Buffer full: {buffer.is_full()}")
    
    # Add elements
    for i in range(7):
        buffer.put(f"Item {i}")
        print(f"After putting Item {i}: size={buffer.size()}, full={buffer.is_full()}")
    
    print(f"\nBuffer contents: {buffer.to_list()}")
    
    # Get elements
    print("\nGetting elements:")
    for _ in range(3):
        item = buffer.get()
        print(f"  Got: {item}")
    
    print(f"Remaining: {buffer.to_list()}")


def demo_performance_comparison():
    """Demonstrate performance comparison with built-in list."""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    # Test append performance
    def builtin_append():
        lst = []
        for i in range(1000):
            lst.append(i)
        return lst
    
    def custom_append():
        arr = ProductionDynamicArray[int]()
        for i in range(1000):
            arr.append(i)
        return arr
    
    # Benchmark
    builtin_time = timeit.timeit(builtin_append, number=100)
    custom_time = timeit.timeit(custom_append, number=100)
    
    print(f"Built-in list append time: {builtin_time:.4f}s")
    print(f"Custom array append time: {custom_time:.4f}s")
    print(f"Custom is {custom_time/builtin_time:.2f}x slower")
    
    # Test memory usage
    import sys
    
    lst = list(range(1000))
    arr = ProductionDynamicArray[int]()
    for i in range(1000):
        arr.append(i)
    
    print(f"\nMemory usage:")
    print(f"Built-in list: {sys.getsizeof(lst)} bytes")
    print(f"Custom array: {sys.getsizeof(arr._array)} bytes")
    print(f"Custom array stats: {arr.stats}")


def main():
    """Run all demos."""
    print("Chapter 3: Dynamic Array with Manual Resizing")
    print("Demonstration of implementations and applications")
    
    demo_basic_dynamic_array()
    demo_growth_strategies()
    demo_text_buffer()
    demo_database()
    demo_circular_buffer()
    demo_performance_comparison()
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main() 