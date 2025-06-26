import time
import random

from  src.chapter_01.dynamic_array import *

def benchmark_append(data_structure, n=100000):
    """Benchmark the append operation."""
    start_time = time.time()
    for i in range(n):
        data_structure.append(i)
    end_time = time.time()
    return end_time - start_time

# Test our implementation
custom_list = DynamicArray()
python_list = []

print(f"Custom list time: {benchmark_append(custom_list):.4f}s")
print(f"Python list time: {benchmark_append(python_list):.4f}s")
