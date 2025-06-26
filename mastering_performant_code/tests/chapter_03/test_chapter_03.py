#!/usr/bin/env python3
"""
Simple test script for Chapter 3 functionality.
"""

from chapter_03.dynamic_array import DynamicArray, ProductionDynamicArray, GrowthStrategy
from chapter_03.applications import TextBuffer, SimpleDatabase

def test_basic_functionality():
    """Test basic dynamic array functionality."""
    print("Testing basic dynamic array...")
    
    # Test basic array
    arr = DynamicArray[int](initial_capacity=4)
    for i in range(10):
        arr.append(i)
    
    print(f"Array: {arr}")
    print(f"Size: {len(arr)}")
    print(f"Capacity: {arr.capacity}")
    print(f"Load factor: {arr.load_factor:.3f}")
    
    # Test production array
    prod_arr = ProductionDynamicArray[int](strategy=GrowthStrategy.DOUBLING)
    for i in range(10):
        prod_arr.append(i)
    
    print(f"Production array: {prod_arr}")
    print(f"Stats: {prod_arr.stats}")

def test_applications():
    """Test real-world applications."""
    print("\nTesting applications...")
    
    # Test text buffer
    buffer = TextBuffer()
    buffer.append_line("Hello, World!")
    buffer.append_line("This is a test.")
    
    print(f"Text buffer: {buffer}")
    print(f"Lines: {buffer.get_all_lines()}")
    
    # Test database
    db = SimpleDatabase()
    db.insert("Alice", 95.5)
    db.insert("Bob", 87.2)
    
    print(f"Database: {db}")
    print(f"Records: {db.get_all_records()}")

if __name__ == "__main__":
    print("Chapter 3: Dynamic Array with Manual Resizing")
    print("=" * 50)
    
    test_basic_functionality()
    test_applications()
    
    print("\nAll tests completed successfully!") 