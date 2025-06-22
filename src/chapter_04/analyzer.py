"""
Memory and performance analysis tools for linked lists.

This module provides tools to analyze the memory usage and performance
characteristics of linked list implementations.
"""

import sys
import timeit
from typing import TypeVar, Generic, Optional, Iterator, List, Dict, Any
from dataclasses import dataclass

# Type variables for generic implementations
T = TypeVar('T')

@dataclass
class MemoryInfo:
    """
    Information about memory usage of a linked list.
    
    This class provides detailed information about the memory usage
    of linked list implementations including object size, total size,
    overhead, and efficiency metrics.
    
    Attributes:
        object_size: Size of the main object in bytes
        total_size: Total memory usage including all nodes in bytes
        overhead: Memory overhead in bytes
        node_count: Number of nodes in the list
        average_node_size: Average size per node in bytes
    """
    object_size: int
    total_size: int
    overhead: int
    node_count: int
    average_node_size: float

class LinkedListAnalyzer:
    """
    Analyzer for linked list data structures.
    
    This class provides tools to analyze the memory usage and performance
    characteristics of linked list implementations. It includes methods for
    memory analysis, performance benchmarking, and comparison with built-in
    Python data structures.
    """
    
    @staticmethod
    def analyze_singly_linked_list(lst: 'SinglyLinkedList') -> MemoryInfo:
        """
        Analyze memory usage of a singly linked list.
        
        Args:
            lst: The singly linked list to analyze
            
        Returns:
            MemoryInfo object containing detailed memory statistics
        """
        object_size = sys.getsizeof(lst)
        node_count = len(lst)
        
        # Calculate total size including nodes
        total_size = object_size
        current = lst._head_sentinel.next
        while current != lst._tail_sentinel:
            total_size += sys.getsizeof(current)
            total_size += sys.getsizeof(current.data)
            current = current.next
        
        # Add sentinel nodes
        total_size += sys.getsizeof(lst._head_sentinel) * 2
        
        overhead = total_size - (node_count * 8)  # Rough estimate
        average_node_size = total_size / (node_count + 2) if node_count > 0 else 0
        
        return MemoryInfo(
            object_size=object_size,
            total_size=total_size,
            overhead=overhead,
            node_count=node_count,
            average_node_size=average_node_size
        )
    
    @staticmethod
    def analyze_doubly_linked_list(lst: 'DoublyLinkedList') -> MemoryInfo:
        """
        Analyze memory usage of a doubly linked list.
        
        Args:
            lst: The doubly linked list to analyze
            
        Returns:
            MemoryInfo object containing detailed memory statistics
        """
        object_size = sys.getsizeof(lst)
        node_count = len(lst)
        
        # Calculate total size including nodes
        total_size = object_size
        current = lst._head_sentinel.next
        while current != lst._tail_sentinel:
            total_size += sys.getsizeof(current)
            total_size += sys.getsizeof(current.data)
            current = current.next
        
        # Add sentinel nodes
        total_size += sys.getsizeof(lst._head_sentinel) * 2
        
        overhead = total_size - (node_count * 12)  # Rough estimate for doubly linked
        average_node_size = total_size / (node_count + 2) if node_count > 0 else 0
        
        return MemoryInfo(
            object_size=object_size,
            total_size=total_size,
            overhead=overhead,
            node_count=node_count,
            average_node_size=average_node_size
        )
    
    @staticmethod
    def benchmark_operations(linked_list, operations: List[str], 
                           iterations: int = 1000) -> Dict[str, float]:
        """
        Benchmark common operations on a linked list.
        
        Args:
            linked_list: The linked list to benchmark
            operations: List of operation names to benchmark
            iterations: Number of iterations for each benchmark
            
        Returns:
            Dictionary mapping operation names to execution times in seconds
        """
        results = {}
        
        for operation in operations:
            if operation == "append":
                setup = f"from src.chapter_04 import {type(linked_list).__name__}; ds = {type(linked_list).__name__}()"
                stmt = "ds.append(42)"
            elif operation == "prepend":
                setup = f"from src.chapter_04 import {type(linked_list).__name__}; ds = {type(linked_list).__name__}()"
                stmt = "ds.prepend(42)"
            elif operation == "get_first":
                setup = f"from src.chapter_04 import {type(linked_list).__name__}; ds = {type(linked_list).__name__}(); [ds.append(i) for i in range(1000)]"
                stmt = "ds.get_at_index(0)"
            elif operation == "get_last":
                setup = f"from src.chapter_04 import {type(linked_list).__name__}; ds = {type(linked_list).__name__}(); [ds.append(i) for i in range(1000)]"
                stmt = "ds.get_at_index(999)"
            elif operation == "get_middle":
                setup = f"from src.chapter_04 import {type(linked_list).__name__}; ds = {type(linked_list).__name__}(); [ds.append(i) for i in range(1000)]"
                stmt = "ds.get_at_index(500)"
            elif operation == "delete_first":
                setup = f"from src.chapter_04 import {type(linked_list).__name__}; ds = {type(linked_list).__name__}(); [ds.append(i) for i in range(1000)]"
                stmt = "ds.delete_first(500)"
            elif operation == "iteration":
                setup = f"from src.chapter_04 import {type(linked_list).__name__}; ds = {type(linked_list).__name__}(); [ds.append(i) for i in range(1000)]"
                stmt = "list(ds)"
            else:
                continue
            
            time = timeit.timeit(stmt, setup=setup, number=iterations)
            results[operation] = time
        
        return results
    
    @staticmethod
    def compare_with_builtin(linked_list, size: int = 1000) -> Dict[str, Dict[str, float]]:
        """
        Compare linked list performance with Python built-in list.
        
        Args:
            linked_list: The linked list to compare
            size: Size of data structures for comparison
            
        Returns:
            Dictionary containing performance comparisons
        """
        results = {}
        
        # Benchmark append operations
        print(f"Benchmarking append operations with {size} elements...")
        
        # Python list append
        list_append = timeit.timeit(
            f"lst.append(i) for i in range({size})",
            setup="lst = []",
            number=1
        )
        
        # Linked list append
        linked_list_append = timeit.timeit(
            f"lst.append(i) for i in range({size})",
            setup=f"from src.chapter_04 import {type(linked_list).__name__}; lst = {type(linked_list).__name__}()",
            number=1
        )
        
        results["append"] = {
            "python_list": list_append,
            "linked_list": linked_list_append,
            "ratio": linked_list_append / list_append if list_append > 0 else float('inf')
        }
        
        # Benchmark prepend operations
        print(f"Benchmarking prepend operations with {size} elements...")
        
        # Python list insert at beginning
        list_prepend = timeit.timeit(
            f"lst.insert(0, i) for i in range({size})",
            setup="lst = []",
            number=1
        )
        
        # Linked list prepend
        linked_list_prepend = timeit.timeit(
            f"lst.prepend(i) for i in range({size})",
            setup=f"from src.chapter_04 import {type(linked_list).__name__}; lst = {type(linked_list).__name__}()",
            number=1
        )
        
        results["prepend"] = {
            "python_list": list_prepend,
            "linked_list": linked_list_prepend,
            "ratio": linked_list_prepend / list_prepend if list_prepend > 0 else float('inf')
        }
        
        # Benchmark access operations
        print(f"Benchmarking access operations...")
        
        # Python list access
        list_access = timeit.timeit(
            "lst[500]",
            setup=f"lst = list(range({size}))",
            number=10000
        )
        
        # Linked list access
        linked_list_access = timeit.timeit(
            "lst.get_at_index(500)",
            setup=f"from src.chapter_04 import {type(linked_list).__name__}; lst = {type(linked_list).__name__}(); [lst.append(i) for i in range({size})]",
            number=10000
        )
        
        results["access"] = {
            "python_list": list_access,
            "linked_list": linked_list_access,
            "ratio": linked_list_access / list_access if list_access > 0 else float('inf')
        }
        
        # Benchmark iteration
        print(f"Benchmarking iteration...")
        
        # Python list iteration
        list_iteration = timeit.timeit(
            "list(lst)",
            setup=f"lst = list(range({size}))",
            number=1000
        )
        
        # Linked list iteration
        linked_list_iteration = timeit.timeit(
            "list(lst)",
            setup=f"from src.chapter_04 import {type(linked_list).__name__}; lst = {type(linked_list).__name__}(); [lst.append(i) for i in range({size})]",
            number=1000
        )
        
        results["iteration"] = {
            "python_list": list_iteration,
            "linked_list": linked_list_iteration,
            "ratio": linked_list_iteration / list_iteration if list_iteration > 0 else float('inf')
        }
        
        return results
    
    @staticmethod
    def analyze_memory_efficiency(linked_list) -> Dict[str, Any]:
        """
        Analyze memory efficiency of a linked list.
        
        Args:
            linked_list: The linked list to analyze
            
        Returns:
            Dictionary containing memory efficiency metrics
        """
        if hasattr(linked_list, '_head_sentinel') and hasattr(linked_list, '_tail_sentinel'):
            if hasattr(linked_list._head_sentinel, 'prev'):
                memory_info = LinkedListAnalyzer.analyze_doubly_linked_list(linked_list)
            else:
                memory_info = LinkedListAnalyzer.analyze_singly_linked_list(linked_list)
        else:
            raise ValueError("Unsupported linked list type")
        
        # Calculate efficiency metrics
        data_size = sum(sys.getsizeof(item) for item in linked_list)
        efficiency_ratio = data_size / memory_info.total_size if memory_info.total_size > 0 else 0
        overhead_ratio = memory_info.overhead / memory_info.total_size if memory_info.total_size > 0 else 0
        
        return {
            "memory_info": memory_info,
            "data_size": data_size,
            "efficiency_ratio": efficiency_ratio,
            "overhead_ratio": overhead_ratio,
            "bytes_per_element": memory_info.total_size / len(linked_list) if len(linked_list) > 0 else 0
        }
    
    @staticmethod
    def generate_performance_report(linked_list, sizes: List[int] = None) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report for a linked list.
        
        Args:
            linked_list: The linked list to analyze
            sizes: List of sizes to test for scaling analysis
            
        Returns:
            Dictionary containing comprehensive performance analysis
        """
        if sizes is None:
            sizes = [100, 1000, 10000]
        
        report = {
            "linked_list_type": type(linked_list).__name__,
            "memory_analysis": {},
            "performance_comparison": {},
            "scaling_analysis": {}
        }
        
        # Memory analysis
        print("Performing memory analysis...")
        report["memory_analysis"] = LinkedListAnalyzer.analyze_memory_efficiency(linked_list)
        
        # Performance comparison
        print("Performing performance comparison...")
        report["performance_comparison"] = LinkedListAnalyzer.compare_with_builtin(linked_list)
        
        # Scaling analysis
        print("Performing scaling analysis...")
        scaling_data = {}
        for size in sizes:
            print(f"Testing size {size}...")
            
            # Create test list
            test_list = type(linked_list)()
            for i in range(size):
                test_list.append(i)
            
            # Benchmark operations
            operations = ["append", "prepend", "get_first", "get_last", "iteration"]
            scaling_data[size] = LinkedListAnalyzer.benchmark_operations(test_list, operations, 100)
        
        report["scaling_analysis"] = scaling_data
        
        return report
    
    @staticmethod
    def print_performance_report(report: Dict[str, Any]) -> None:
        """
        Print a formatted performance report.
        
        Args:
            report: The performance report to print
        """
        print(f"\n=== Performance Report for {report['linked_list_type']} ===")
        
        # Memory analysis
        print("\n--- Memory Analysis ---")
        memory_info = report["memory_analysis"]["memory_info"]
        print(f"Object size: {memory_info.object_size} bytes")
        print(f"Total size: {memory_info.total_size} bytes")
        print(f"Overhead: {memory_info.overhead} bytes")
        print(f"Node count: {memory_info.node_count}")
        print(f"Average node size: {memory_info.average_node_size:.2f} bytes")
        print(f"Efficiency ratio: {report['memory_analysis']['efficiency_ratio']:.2%}")
        print(f"Overhead ratio: {report['memory_analysis']['overhead_ratio']:.2%}")
        print(f"Bytes per element: {report['memory_analysis']['bytes_per_element']:.2f}")
        
        # Performance comparison
        print("\n--- Performance Comparison vs Python List ---")
        for operation, data in report["performance_comparison"].items():
            print(f"{operation.capitalize()}:")
            print(f"  Python list: {data['python_list']:.6f} seconds")
            print(f"  Linked list: {data['linked_list']:.6f} seconds")
            print(f"  Ratio: {data['ratio']:.2f}x")
        
        # Scaling analysis
        print("\n--- Scaling Analysis ---")
        for size, operations in report["scaling_analysis"].items():
            print(f"\nSize {size}:")
            for operation, time in operations.items():
                print(f"  {operation}: {time:.6f} seconds") 