"""
Skip list analyzer for performance and memory analysis.

This module provides tools to analyze the memory usage, performance,
and structural characteristics of skip lists.
"""

import timeit
import random
import sys
from typing import TypeVar, Generic, Optional, List, Iterator, Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from .skip_list import SkipList

T = TypeVar('T')

@dataclass
class SkipListMemoryInfo:
    """Information about memory usage of a skip list."""
    object_size: int
    total_size: int
    overhead: int
    node_count: int
    average_height: float
    level_distribution: List[int]

class SkipListAnalyzer:
    """
    Analyzer for skip list performance and memory characteristics.
    
    This class provides tools to analyze the memory usage, performance,
    and structural characteristics of skip lists.
    """
    
    @staticmethod
    def analyze_memory(skip_list: SkipList[T]) -> SkipListMemoryInfo:
        """Analyze memory usage of a skip list."""
        object_size = sys.getsizeof(skip_list)
        
        # Calculate total size including all nodes
        total_size = object_size
        node_count = 0
        total_height = 0
        
        current = skip_list.head.forward[0]
        while current is not None:
            node_size = sys.getsizeof(current) + sys.getsizeof(current.data)
            total_size += node_size
            node_count += 1
            total_height += current.height
            current = current.forward[0]
        
        average_height = total_height / node_count if node_count > 0 else 0
        overhead = object_size - (node_count * 8)  # Rough estimate
        
        return SkipListMemoryInfo(
            object_size=object_size,
            total_size=total_size,
            overhead=overhead,
            node_count=node_count,
            average_height=average_height,
            level_distribution=skip_list.get_level_distribution()
        )
    
    @staticmethod
    def benchmark_operations(skip_list: SkipList[T], 
                           operations: List[str], 
                           iterations: int = 1000) -> Dict[str, float]:
        """Benchmark common operations on a skip list."""
        results = {}
        
        # Prepare test data
        test_values = list(range(1000))
        random.shuffle(test_values)
        
        for operation in operations:
            if operation == "insert":
                setup = f"from mastering_performant_code.chapter_05 import SkipList; sl = SkipList()"
                stmt = "[sl.insert(i) for i in range(100)]"
            elif operation == "search":
                setup = f"from mastering_performant_code.chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in range(1000)]"
                stmt = "[sl.search(i) for i in range(100)]"
            elif operation == "delete":
                setup = f"from mastering_performant_code.chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in range(1000)]"
                stmt = "[sl.delete(i) for i in range(100)]"
            elif operation == "range_query":
                setup = f"from mastering_performant_code.chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in range(1000)]"
                stmt = "list(sl.range_query(100, 200))"
            else:
                continue
            
            time = timeit.timeit(stmt, setup=setup, number=iterations)
            results[operation] = time
        
        return results
    
    @staticmethod
    def analyze_height_distribution(skip_list: SkipList[T], 
                                  num_samples: int = 10000) -> Dict[int, float]:
        """Analyze the distribution of node heights."""
        height_counts = defaultdict(int)
        
        # Generate many random heights using the same probability
        for _ in range(num_samples):
            height = 1
            while (random.random() < skip_list.probability and 
                   height < skip_list.max_height):
                height += 1
            height_counts[height] += 1
        
        # Convert to probabilities
        total = sum(height_counts.values())
        distribution = {height: count / total for height, count in height_counts.items()}
        
        return distribution
    
    @staticmethod
    def compare_with_alternatives(skip_list: SkipList[T], 
                                test_data: List[T]) -> Dict[str, Dict[str, float]]:
        """Compare skip list performance with alternative data structures."""
        results = {}
        
        # Create a smaller test set for search/delete operations
        search_data = test_data[:min(100, len(test_data))]
        
        # Skip list operations
        skip_insert = timeit.timeit(
            "[sl.insert(i) for i in test_data]",
            setup=f"from mastering_performant_code.chapter_05 import SkipList; sl = SkipList(); test_data = {test_data}",
            number=1
        )
        
        skip_search = timeit.timeit(
            "[sl.search(i) for i in search_data]",
            setup=f"from mastering_performant_code.chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in {test_data}]; search_data = {search_data}",
            number=100
        )
        
        skip_delete = timeit.timeit(
            "[sl.delete(i) for i in search_data]",
            setup=f"from mastering_performant_code.chapter_05 import SkipList; sl = SkipList(); [sl.insert(i) for i in {test_data}]; search_data = {search_data}",
            number=1
        )
        
        results['skip_list'] = {
            'insert': skip_insert,
            'search': skip_search,
            'delete': skip_delete
        }
        
        # List operations (for comparison)
        list_insert = timeit.timeit(
            "[lst.append(i) for i in test_data]",
            setup=f"lst = []; test_data = {test_data}",
            number=1
        )
        
        list_search = timeit.timeit(
            "[i in lst for i in search_data]",
            setup=f"lst = {test_data}; search_data = {search_data}",
            number=100
        )
        
        list_delete = timeit.timeit(
            "[lst.remove(i) for i in search_data if i in lst]",
            setup=f"lst = {test_data.copy()}; search_data = {search_data}",
            number=1
        )
        
        results['list'] = {
            'insert': list_insert,
            'search': list_search,
            'delete': list_delete
        }
        
        # Set operations (for comparison)
        set_insert = timeit.timeit(
            "[st.add(i) for i in test_data]",
            setup=f"st = set(); test_data = {test_data}",
            number=1
        )
        
        set_search = timeit.timeit(
            "[i in st for i in search_data]",
            setup=f"st = set({test_data}); search_data = {search_data}",
            number=100
        )
        
        set_delete = timeit.timeit(
            "[st.discard(i) for i in search_data]",
            setup=f"st = set({test_data}); search_data = {search_data}",
            number=1
        )
        
        results['set'] = {
            'insert': set_insert,
            'search': set_search,
            'delete': set_delete
        }
        
        return results
    
    @staticmethod
    def analyze_memory_comparison(skip_list: SkipList[T], 
                                test_data: List[T]) -> Dict[str, Dict[str, Any]]:
        """Compare memory usage with alternative data structures."""
        results = {}
        
        # Skip list memory
        skip_memory = SkipListAnalyzer.analyze_memory(skip_list)
        results['skip_list'] = {
            'total_size': skip_memory.total_size,
            'node_count': skip_memory.node_count,
            'average_height': skip_memory.average_height,
            'overhead': skip_memory.overhead
        }
        
        # List memory
        lst = list(test_data)
        list_memory = sys.getsizeof(lst)
        results['list'] = {
            'total_size': list_memory,
            'node_count': len(lst),
            'average_height': 1.0,  # Lists don't have height concept
            'overhead': list_memory - (len(lst) * 8)  # Rough estimate
        }
        
        # Set memory
        st = set(test_data)
        set_memory = sys.getsizeof(st)
        results['set'] = {
            'total_size': set_memory,
            'node_count': len(st),
            'average_height': 1.0,  # Sets don't have height concept
            'overhead': set_memory - (len(st) * 8)  # Rough estimate
        }
        
        return results
    
    @staticmethod
    def generate_performance_report(skip_list: SkipList[T], 
                                  test_data: List[T]) -> str:
        """Generate a comprehensive performance report."""
        report = []
        report.append("=== Skip List Performance Report ===\n")
        
        # Memory analysis
        report.append("Memory Analysis:")
        report.append("-" * 20)
        memory_info = SkipListAnalyzer.analyze_memory(skip_list)
        report.append(f"Total memory usage: {memory_info.total_size} bytes")
        report.append(f"Node count: {memory_info.node_count}")
        report.append(f"Average height: {memory_info.average_height:.2f}")
        report.append(f"Memory overhead: {memory_info.overhead} bytes")
        report.append("")
        
        # Level distribution
        report.append("Level Distribution:")
        report.append("-" * 20)
        for level, count in enumerate(memory_info.level_distribution[:8]):
            if count > 0:
                percentage = (count / memory_info.node_count) * 100
                report.append(f"Level {level}: {count} nodes ({percentage:.1f}%)")
        report.append("")
        
        # Performance comparison
        report.append("Performance Comparison:")
        report.append("-" * 25)
        perf_results = SkipListAnalyzer.compare_with_alternatives(skip_list, test_data)
        
        for structure, times in perf_results.items():
            report.append(f"{structure.title()}:")
            for operation, time_taken in times.items():
                report.append(f"  {operation}: {time_taken:.6f} seconds")
            report.append("")
        
        # Memory comparison
        report.append("Memory Comparison:")
        report.append("-" * 20)
        mem_results = SkipListAnalyzer.analyze_memory_comparison(skip_list, test_data)
        
        for structure, info in mem_results.items():
            report.append(f"{structure.title()}:")
            report.append(f"  Total size: {info['total_size']} bytes")
            report.append(f"  Node count: {info['node_count']}")
            report.append(f"  Average height: {info['average_height']:.2f}")
            report.append(f"  Overhead: {info['overhead']} bytes")
            report.append("")
        
        return "\n".join(report) 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running analyzer demonstration...")
    print("=" * 50)

    # Create instance of SkipListAnalyzer
    try:
        instance = SkipListAnalyzer()
        print(f"✓ Created SkipListAnalyzer instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.append(1)
        instance.append(2)
        instance.append(3)
        print(f"  After adding elements: {instance}")
        print(f"  Length: {len(instance)}")
    except Exception as e:
        print(f"✗ Error creating SkipListAnalyzer instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
