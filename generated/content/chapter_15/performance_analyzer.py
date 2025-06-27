"""
Performance analysis tools for cache implementations.

This module provides comprehensive benchmarking and analysis tools
for comparing different cache implementations (LRU, LFU) across
various workloads and configurations.
"""

import timeit
import random
import time
from typing import List, Dict, Any, Callable, Tuple
from dataclasses import dataclass
from .lru_cache import LRUCacheOrderedDict, LRUCacheDLL
from .lfu_cache import LFUCache

@dataclass
class BenchmarkResult:
    """Container for benchmark results."""
    cache_type: str
    capacity: int
    operation: str
    time_per_op: float
    total_time: float
    operations_count: int
    memory_usage: int
    hit_ratio: float

class CacheAnalyzer:
    """Comprehensive cache performance analyzer."""
    
    def __init__(self):
        self.cache_implementations = {
            'LRU_OrderedDict': LRUCacheOrderedDict,
            'LRU_DoublyLinkedList': LRUCacheDLL,
            'LFU': LFUCache
        }
    
    def benchmark_cache_operations(self, 
                                 cache_class: Callable, 
                                 capacity: int, 
                                 operations: int,
                                 workload_type: str = "mixed") -> Dict[str, float]:
        """
        Benchmark cache operations and return timing results.
        
        Args:
            cache_class: The cache class to benchmark
            capacity: Cache capacity
            operations: Number of operations to perform
            workload_type: Type of workload ("mixed", "read_heavy", "write_heavy")
            
        Returns:
            Dictionary containing timing results
        """
        cache = cache_class(capacity)
        
        # Generate workload based on type
        if workload_type == "read_heavy":
            # 90% reads, 10% writes
            read_ratio = 0.9
        elif workload_type == "write_heavy":
            # 10% reads, 90% writes
            read_ratio = 0.1
        else:  # mixed
            # 70% reads, 30% writes
            read_ratio = 0.7
        
        # Pre-populate cache for read operations
        for i in range(min(capacity, operations // 2)):
            cache.put(f"key_{i}", f"value_{i}")
        
        def benchmark_workload():
            for i in range(operations):
                if random.random() < read_ratio:
                    # Read operation
                    key = f"key_{random.randint(0, capacity * 2)}"
                    cache.get(key)
                else:
                    # Write operation
                    key = f"key_{random.randint(0, capacity * 2)}"
                    value = f"value_{i}"
                    cache.put(key, value)
        
        # Benchmark operations
        total_time = timeit.timeit(benchmark_workload, number=1)
        
        # Calculate per-operation time
        time_per_op = total_time / operations
        
        # Get final statistics
        stats = cache.get_stats()
        
        return {
            'put_time_per_op': time_per_op,
            'get_time_per_op': time_per_op,
            'total_time': total_time,
            'operations_count': operations,
            'hit_ratio': stats['hit_ratio'],
            'memory_usage': stats['memory_usage'],
            'evictions': stats['evictions']
        }
    
    def compare_implementations(self, 
                              capacities: List[int],
                              operations: int = 10000,
                              workload_type: str = "mixed") -> Dict[str, List[BenchmarkResult]]:
        """
        Compare different cache implementations across various capacities.
        
        Args:
            capacities: List of cache capacities to test
            operations: Number of operations per benchmark
            workload_type: Type of workload to simulate
            
        Returns:
            Dictionary mapping cache types to lists of benchmark results
        """
        results = {name: [] for name in self.cache_implementations.keys()}
        
        for capacity in capacities:
            for name, cache_class in self.cache_implementations.items():
                benchmark = self.benchmark_cache_operations(
                    cache_class, capacity, operations, workload_type
                )
                
                # Create benchmark result for put operations
                put_result = BenchmarkResult(
                    cache_type=name,
                    capacity=capacity,
                    operation="put",
                    time_per_op=benchmark['put_time_per_op'],
                    total_time=benchmark['total_time'],
                    operations_count=operations,
                    memory_usage=benchmark['memory_usage'],
                    hit_ratio=benchmark['hit_ratio']
                )
                
                results[name].append(put_result)
        
        return results
    
    def benchmark_memory_efficiency(self, 
                                  capacities: List[int],
                                  items_per_test: int = 1000) -> Dict[str, List[Tuple[int, int]]]:
        """
        Benchmark memory efficiency across different cache implementations.
        
        Args:
            capacities: List of cache capacities to test
            items_per_test: Number of items to store in each test
            
        Returns:
            Dictionary mapping cache types to (capacity, memory_usage) tuples
        """
        memory_results = {name: [] for name in self.cache_implementations.keys()}
        
        for capacity in capacities:
            for name, cache_class in self.cache_implementations.items():
                cache = cache_class(capacity)
                
                # Add items up to the test limit
                for i in range(min(items_per_test, capacity * 2)):
                    cache.put(f"key_{i}", f"value_{i}" * 100)  # Large values
                
                stats = cache.get_stats()
                memory_results[name].append((capacity, stats['memory_usage']))
        
        return memory_results
    
    def generate_performance_report(self, 
                                  capacities: List[int] = None,
                                  operations: int = 10000) -> str:
        """
        Generate a comprehensive performance report.
        
        Args:
            capacities: List of cache capacities to test
            operations: Number of operations per benchmark
            
        Returns:
            Formatted performance report string
        """
        if capacities is None:
            capacities = [10, 100, 1000, 10000]
        
        report = []
        report.append("=" * 60)
        report.append("CACHE PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 60)
        report.append(f"Operations per benchmark: {operations:,}")
        report.append(f"Capacities tested: {capacities}")
        report.append("")
        
        # Test different workload types
        workload_types = ["mixed", "read_heavy", "write_heavy"]
        
        for workload in workload_types:
            report.append(f"WORKLOAD TYPE: {workload.upper()}")
            report.append("-" * 40)
            
            results = self.compare_implementations(capacities, operations, workload)
            
            # Create comparison table
            report.append(f"{'Cache Type':<20} {'Capacity':<10} {'Time/Op (μs)':<12} {'Hit Ratio':<10} {'Memory (KB)':<12}")
            report.append("-" * 70)
            
            for cache_type, cache_results in results.items():
                for result in cache_results:
                    time_us = result.time_per_op * 1_000_000  # Convert to microseconds
                    memory_kb = result.memory_usage / 1024  # Convert to KB
                    report.append(
                        f"{cache_type:<20} {result.capacity:<10} {time_us:<12.2f} "
                        f"{result.hit_ratio:<10.3f} {memory_kb:<12.1f}"
                    )
            
            report.append("")
        
        # Memory efficiency analysis
        report.append("MEMORY EFFICIENCY ANALYSIS")
        report.append("-" * 40)
        memory_results = self.benchmark_memory_efficiency(capacities)
        
        report.append(f"{'Cache Type':<20} {'Capacity':<10} {'Memory/Item (bytes)':<20}")
        report.append("-" * 55)
        
        for cache_type, memory_data in memory_results.items():
            for capacity, memory_usage in memory_data:
                items_stored = min(capacity, 1000)  # Approximate items stored
                if items_stored > 0:
                    memory_per_item = memory_usage / items_stored
                    report.append(f"{cache_type:<20} {capacity:<10} {memory_per_item:<20.1f}")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)

class RealWorldSimulator:
    """Simulator for real-world cache usage patterns."""
    
    def __init__(self):
        self.cache_implementations = {
            'LRU': LRUCacheOrderedDict,
            'LFU': LFUCache
        }
    
    def simulate_web_cache(self, 
                          cache_type: str,
                          capacity: int,
                          requests: int,
                          popular_urls_ratio: float = 0.2) -> Dict[str, Any]:
        """
        Simulate web page caching with realistic access patterns.
        
        Args:
            cache_type: Type of cache to use ("LRU" or "LFU")
            capacity: Cache capacity
            requests: Number of requests to simulate
            popular_urls_ratio: Ratio of popular URLs (Zipf distribution)
            
        Returns:
            Dictionary containing simulation results
        """
        if cache_type not in self.cache_implementations:
            raise ValueError(f"Unsupported cache type: {cache_type}")
        
        cache_class = self.cache_implementations[cache_type]
        cache = cache_class(capacity)
        
        # Generate URL distribution (Zipf-like)
        total_urls = capacity * 10
        popular_urls = int(total_urls * popular_urls_ratio)
        
        # Simulate requests
        start_time = time.time()
        
        for i in range(requests):
            # Generate URL with Zipf-like distribution
            if random.random() < popular_urls_ratio:
                # Popular URL
                url_id = random.randint(0, popular_urls - 1)
            else:
                # Random URL
                url_id = random.randint(popular_urls, total_urls - 1)
            
            url = f"/page/{url_id}"
            
            # Try to get from cache
            content = cache.get(url)
            
            if content is None:
                # Cache miss - simulate backend request
                time.sleep(0.001)  # 1ms simulated latency
                content = f"<html>Content for {url}</html>"
                cache.put(url, content)
        
        end_time = time.time()
        
        # Collect statistics
        stats = cache.get_stats()
        
        return {
            'cache_type': cache_type,
            'total_requests': requests,
            'simulation_time': end_time - start_time,
            'hit_ratio': stats['hit_ratio'],
            'cache_hits': stats['hits'],
            'cache_misses': stats['misses'],
            'evictions': stats['evictions'],
            'memory_usage': stats['memory_usage'],
            'requests_per_second': requests / (end_time - start_time)
        }
    
    def simulate_database_cache(self, 
                               cache_type: str,
                               capacity: int,
                               queries: int,
                               query_pattern: str = "mixed") -> Dict[str, Any]:
        """
        Simulate database query caching.
        
        Args:
            cache_type: Type of cache to use ("LRU" or "LFU")
            capacity: Cache capacity
            queries: Number of queries to simulate
            query_pattern: Query pattern ("mixed", "repeated", "unique")
            
        Returns:
            Dictionary containing simulation results
        """
        if cache_type not in self.cache_implementations:
            raise ValueError(f"Unsupported cache type: {cache_type}")
        
        cache_class = self.cache_implementations[cache_type]
        cache = cache_class(capacity)
        
        # Generate query patterns
        if query_pattern == "repeated":
            # Many repeated queries
            unique_queries = capacity // 2
        elif query_pattern == "unique":
            # Mostly unique queries
            unique_queries = capacity * 5
        else:  # mixed
            # Balanced mix
            unique_queries = capacity
        
        start_time = time.time()
        
        for i in range(queries):
            if query_pattern == "repeated":
                # High chance of repeated queries
                query_id = random.randint(0, unique_queries - 1)
            elif query_pattern == "unique":
                # Mostly unique queries
                query_id = random.randint(0, unique_queries - 1)
            else:
                # Mixed pattern
                if random.random() < 0.7:
                    query_id = random.randint(0, unique_queries - 1)
                else:
                    query_id = random.randint(0, unique_queries * 2 - 1)
            
            query_key = f"SELECT * FROM table_{query_id} WHERE id = {random.randint(1, 1000)}"
            
            # Try to get from cache
            result = cache.get(query_key)
            
            if result is None:
                # Cache miss - simulate database query
                time.sleep(0.005)  # 5ms simulated latency
                result = f"Result for query {query_id}: {random.randint(1000, 9999)} rows"
                cache.put(query_key, result)
        
        end_time = time.time()
        
        # Collect statistics
        stats = cache.get_stats()
        
        return {
            'cache_type': cache_type,
            'total_queries': queries,
            'simulation_time': end_time - start_time,
            'hit_ratio': stats['hit_ratio'],
            'cache_hits': stats['hits'],
            'cache_misses': stats['misses'],
            'evictions': stats['evictions'],
            'memory_usage': stats['memory_usage'],
            'queries_per_second': queries / (end_time - start_time)
        }
    
    def compare_real_world_scenarios(self, 
                                   capacity: int = 1000,
                                   requests: int = 10000) -> str:
        """
        Compare cache performance across different real-world scenarios.
        
        Args:
            capacity: Cache capacity
            requests: Number of requests/queries
            
        Returns:
            Formatted comparison report
        """
        report = []
        report.append("=" * 70)
        report.append("REAL-WORLD CACHE PERFORMANCE COMPARISON")
        report.append("=" * 70)
        report.append(f"Cache Capacity: {capacity:,}")
        report.append(f"Total Requests: {requests:,}")
        report.append("")
        
        # Web cache simulation
        report.append("WEB CACHE SIMULATION")
        report.append("-" * 30)
        
        web_results = {}
        for cache_type in ['LRU', 'LFU']:
            web_results[cache_type] = self.simulate_web_cache(
                cache_type, capacity, requests, popular_urls_ratio=0.2
            )
        
        report.append(f"{'Cache Type':<10} {'Hit Ratio':<10} {'RPS':<10} {'Memory (KB)':<12}")
        report.append("-" * 45)
        
        for cache_type, results in web_results.items():
            memory_kb = results['memory_usage'] / 1024
            report.append(
                f"{cache_type:<10} {results['hit_ratio']:<10.3f} "
                f"{results['requests_per_second']:<10.1f} {memory_kb:<12.1f}"
            )
        
        report.append("")
        
        # Database cache simulation
        report.append("DATABASE CACHE SIMULATION")
        report.append("-" * 30)
        
        db_results = {}
        for cache_type in ['LRU', 'LFU']:
            db_results[cache_type] = self.simulate_database_cache(
                cache_type, capacity, requests, query_pattern="mixed"
            )
        
        report.append(f"{'Cache Type':<10} {'Hit Ratio':<10} {'QPS':<10} {'Memory (KB)':<12}")
        report.append("-" * 45)
        
        for cache_type, results in db_results.items():
            memory_kb = results['memory_usage'] / 1024
            report.append(
                f"{cache_type:<10} {results['hit_ratio']:<10.3f} "
                f"{results['queries_per_second']:<10.1f} {memory_kb:<12.1f}"
            )
        
        report.append("")
        report.append("=" * 70)
        
        return "\n".join(report)

def run_comprehensive_analysis():
    """Run comprehensive cache analysis and print results."""
    print("Running comprehensive cache performance analysis...")
    print()
    
    # Performance analyzer
    analyzer = CacheAnalyzer()
    report = analyzer.generate_performance_report()
    print(report)
    
    print("\n" + "="*80 + "\n")
    
    # Real-world simulator
    simulator = RealWorldSimulator()
    real_world_report = simulator.compare_real_world_scenarios()
    print(real_world_report)

if __name__ == "__main__":
    run_comprehensive_analysis() 