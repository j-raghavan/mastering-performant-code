"""
Heap Performance Analyzer

This module provides tools to analyze the performance characteristics
of binary heaps and compare with Python's heapq module.
"""

import sys
import timeit
import random
from typing import TypeVar, Generic, Optional, List, Callable, Any, Dict, Tuple
from dataclasses import dataclass
import heapq
from .binary_heap import BinaryHeap

T = TypeVar('T')

@dataclass
class PerformanceMetrics:
    """Performance metrics for heap operations."""
    operation: str
    time_seconds: float
    iterations: int
    avg_time: float
    data_size: int

class HeapAnalyzer:
    """
    Analyzer for heap performance and memory usage.
    
    This class provides tools to analyze the performance characteristics
    of binary heaps and compare with Python's heapq module.
    """
    
    @staticmethod
    def benchmark_heap_operations(heap_class: type, data_sizes: List[int], 
                                iterations: int = 1000) -> Dict[str, List[PerformanceMetrics]]:
        """Benchmark heap operations across different data sizes."""
        results = {
            "push": [],
            "pop": [],
            "peek": [],
            "heapify": []
        }
        
        for size in data_sizes:
            # Benchmark push operations
            setup = f"heap = {heap_class.__name__}()"
            stmt = "heap.push(random.randint(1, 1000))"
            time_push = timeit.timeit(stmt, setup=setup, globals={"random": random}, number=iterations)
            
            results["push"].append(PerformanceMetrics(
                operation="push",
                time_seconds=time_push,
                iterations=iterations,
                avg_time=time_push / iterations,
                data_size=size
            ))
            
            # Benchmark pop operations
            setup = f"""
heap = {heap_class.__name__}()
for _ in range({size}):
    heap.push(random.randint(1, 1000))
"""
            stmt = "heap.pop()"
            time_pop = timeit.timeit(stmt, setup=setup, globals={"random": random}, number=iterations)
            
            results["pop"].append(PerformanceMetrics(
                operation="pop",
                time_seconds=time_pop,
                iterations=iterations,
                avg_time=time_pop / iterations,
                data_size=size
            ))
            
            # Benchmark peek operations
            setup = f"""
heap = {heap_class.__name__}()
for _ in range({size}):
    heap.push(random.randint(1, 1000))
"""
            stmt = "heap.peek()"
            time_peek = timeit.timeit(stmt, setup=setup, globals={"random": random}, number=iterations)
            
            results["peek"].append(PerformanceMetrics(
                operation="peek",
                time_seconds=time_peek,
                iterations=iterations,
                avg_time=time_peek / iterations,
                data_size=size
            ))
            
            # Benchmark heapify operations
            setup = f"items = [random.randint(1, 1000) for _ in range({size})]"
            stmt = f"heap = {heap_class.__name__}(); heap.heapify_bottom_up(items)"
            time_heapify = timeit.timeit(stmt, setup=setup, globals={"random": random}, number=iterations)
            
            results["heapify"].append(PerformanceMetrics(
                operation="heapify",
                time_seconds=time_heapify,
                iterations=iterations,
                avg_time=time_heapify / iterations,
                data_size=size
            ))
        
        return results
    
    @staticmethod
    def compare_with_heapq(heap_class: type, data_sizes: List[int], 
                          iterations: int = 1000) -> Dict[str, Dict[str, float]]:
        """Compare custom heap implementation with Python's heapq."""
        comparison = {}
        
        for size in data_sizes:
            # Custom heap push
            setup_custom = f"heap = {heap_class.__name__}()"
            stmt_custom = "heap.push(random.randint(1, 1000))"
            time_custom = timeit.timeit(stmt_custom, setup=setup_custom, 
                                      globals={"random": random}, number=iterations)
            
            # heapq push
            setup_heapq = "heap = []"
            stmt_heapq = "heapq.heappush(heap, random.randint(1, 1000))"
            time_heapq = timeit.timeit(stmt_heapq, setup=setup_heapq, 
                                     globals={"random": random, "heapq": heapq}, number=iterations)
            
            comparison[f"push_{size}"] = {
                "custom": time_custom,
                "heapq": time_heapq,
                "ratio": time_custom / time_heapq
            }
            
            # Custom heap pop
            setup_custom = f"""
heap = {heap_class.__name__}()
for _ in range({size}):
    heap.push(random.randint(1, 1000))
"""
            stmt_custom = "heap.pop()"
            time_custom = timeit.timeit(stmt_custom, setup=setup_custom, 
                                      globals={"random": random}, number=iterations)
            
            # heapq pop
            setup_heapq = f"""
heap = []
for _ in range({size}):
    heapq.heappush(heap, random.randint(1, 1000))
"""
            stmt_heapq = "heapq.heappop(heap)"
            time_heapq = timeit.timeit(stmt_heapq, setup=setup_heapq, 
                                     globals={"random": random, "heapq": heapq}, number=iterations)
            
            comparison[f"pop_{size}"] = {
                "custom": time_custom,
                "heapq": time_heapq,
                "ratio": time_custom / time_heapq
            }
        
        return comparison
    
    @staticmethod
    def analyze_memory_usage(heap: BinaryHeap) -> Dict[str, int]:
        """Analyze memory usage of a heap."""
        heap_size = sys.getsizeof(heap._heap)
        node_sizes = sum(sys.getsizeof(node) for node in heap._heap)
        data_sizes = sum(sys.getsizeof(node.data) for node in heap._heap if node.data is not None)
        
        return {
            "heap_array_size": heap_size,
            "total_node_size": node_sizes,
            "total_data_size": data_sizes,
            "total_size": heap_size + node_sizes + data_sizes,
            "num_elements": len(heap)
        }
    
    @staticmethod
    def benchmark_heap_variants(data_sizes: List[int], iterations: int = 100) -> Dict[str, Dict[int, float]]:
        """Benchmark different heap variants (min vs max)."""
        results = {
            "min_heap_push": {},
            "max_heap_push": {},
            "min_heap_pop": {},
            "max_heap_pop": {}
        }
        
        for size in data_sizes:
            # Min heap operations
            setup = "heap = BinaryHeap(heap_type='min')"
            stmt = "heap.push(random.randint(1, 1000))"
            time_min_push = timeit.timeit(stmt, setup=setup, 
                                        globals={"random": random, "BinaryHeap": BinaryHeap}, 
                                        number=iterations)
            
            setup = f"""
heap = BinaryHeap(heap_type='min')
for _ in range({size}):
    heap.push(random.randint(1, 1000))
"""
            stmt = "heap.pop()"
            time_min_pop = timeit.timeit(stmt, setup=setup, 
                                       globals={"random": random, "BinaryHeap": BinaryHeap}, 
                                       number=iterations)
            
            # Max heap operations
            setup = "heap = BinaryHeap(heap_type='max')"
            stmt = "heap.push(random.randint(1, 1000))"
            time_max_push = timeit.timeit(stmt, setup=setup, 
                                        globals={"random": random, "BinaryHeap": BinaryHeap}, 
                                        number=iterations)
            
            setup = f"""
heap = BinaryHeap(heap_type='max')
for _ in range({size}):
    heap.push(random.randint(1, 1000))
"""
            stmt = "heap.pop()"
            time_max_pop = timeit.timeit(stmt, setup=setup, 
                                       globals={"random": random, "BinaryHeap": BinaryHeap}, 
                                       number=iterations)
            
            results["min_heap_push"][size] = time_min_push
            results["max_heap_push"][size] = time_max_push
            results["min_heap_pop"][size] = time_min_pop
            results["max_heap_pop"][size] = time_max_pop
        
        return results
    
    @staticmethod
    def benchmark_heapify_methods(data_sizes: List[int], iterations: int = 50) -> Dict[str, Dict[int, float]]:
        """Benchmark different heapify methods."""
        results = {
            "push_heapify": {},
            "bottom_up_heapify": {}
        }
        
        for size in data_sizes:
            # Push-based heapify
            setup = f"items = [random.randint(1, 1000) for _ in range({size})]"
            stmt = """
heap = BinaryHeap()
for item in items:
    heap.push(item)
"""
            time_push = timeit.timeit(stmt, setup=setup, 
                                    globals={"random": random, "BinaryHeap": BinaryHeap}, 
                                    number=iterations)
            
            # Bottom-up heapify
            setup = f"items = [random.randint(1, 1000) for _ in range({size})]"
            stmt = """
heap = BinaryHeap()
heap.heapify_bottom_up(items)
"""
            time_bottom_up = timeit.timeit(stmt, setup=setup, 
                                         globals={"random": random, "BinaryHeap": BinaryHeap}, 
                                         number=iterations)
            
            results["push_heapify"][size] = time_push
            results["bottom_up_heapify"][size] = time_bottom_up
        
        return results
    
    @staticmethod
    def generate_performance_report(heap_class: type = BinaryHeap) -> str:
        """Generate a comprehensive performance report."""
        data_sizes = [100, 1000, 10000]
        
        # Benchmark operations
        operation_metrics = HeapAnalyzer.benchmark_heap_operations(heap_class, data_sizes, 100)
        
        # Compare with heapq
        heapq_comparison = HeapAnalyzer.compare_with_heapq(heap_class, data_sizes, 100)
        
        # Benchmark variants
        variant_metrics = HeapAnalyzer.benchmark_heap_variants(data_sizes, 50)
        
        # Benchmark heapify methods
        heapify_metrics = HeapAnalyzer.benchmark_heapify_methods(data_sizes, 25)
        
        report = []
        report.append("Heap Performance Report")
        report.append("=" * 50)
        report.append("")
        
        # Operation performance
        report.append("Operation Performance (microseconds per operation):")
        report.append("-" * 45)
        for operation, metrics in operation_metrics.items():
            report.append(f"{operation.upper()}:")
            for metric in metrics:
                avg_us = metric.avg_time * 1_000_000
                report.append(f"  Size {metric.data_size}: {avg_us:.2f} μs")
            report.append("")
        
        # heapq comparison
        report.append("Comparison with heapq (ratio > 1 means custom is slower):")
        report.append("-" * 55)
        for size in data_sizes:
            push_ratio = heapq_comparison[f"push_{size}"]["ratio"]
            pop_ratio = heapq_comparison[f"pop_{size}"]["ratio"]
            report.append(f"Size {size}: Push ratio = {push_ratio:.2f}x, Pop ratio = {pop_ratio:.2f}x")
        report.append("")
        
        # Variant comparison
        report.append("Min vs Max Heap Performance:")
        report.append("-" * 30)
        for size in data_sizes:
            min_push = variant_metrics["min_heap_push"][size] * 1_000_000
            max_push = variant_metrics["max_heap_push"][size] * 1_000_000
            min_pop = variant_metrics["min_heap_pop"][size] * 1_000_000
            max_pop = variant_metrics["max_heap_pop"][size] * 1_000_000
            report.append(f"Size {size}:")
            report.append(f"  Push - Min: {min_push:.2f} μs, Max: {max_push:.2f} μs")
            report.append(f"  Pop  - Min: {min_pop:.2f} μs, Max: {max_pop:.2f} μs")
        report.append("")
        
        # Heapify comparison
        report.append("Heapify Methods Performance:")
        report.append("-" * 30)
        for size in data_sizes:
            push_time = heapify_metrics["push_heapify"][size] * 1_000
            bottom_up_time = heapify_metrics["bottom_up_heapify"][size] * 1_000
            report.append(f"Size {size}:")
            report.append(f"  Push-based: {push_time:.2f} ms")
            report.append(f"  Bottom-up:  {bottom_up_time:.2f} ms")
            report.append(f"  Speedup: {push_time / bottom_up_time:.2f}x")
        report.append("")
        
        return "\n".join(report) 