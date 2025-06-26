"""
Bloom Filter Analyzer

This module provides tools for analyzing the performance characteristics
and accuracy of Bloom filter implementations.
"""

import sys
import timeit
from typing import Any, List, Optional, Tuple, Dict
from dataclasses import dataclass

@dataclass
class BloomFilterStats:
    """Statistics for Bloom filter performance analysis."""
    expected_elements: int
    actual_elements: int
    size: int
    hash_count: int
    false_positive_rate: float
    memory_usage: int
    load_factor: float
    theoretical_fpr: float

class BloomFilterAnalyzer:
    """
    Analyzer for Bloom filter performance and accuracy.
    
    This class provides tools to analyze the performance characteristics
    and accuracy of Bloom filter implementations.
    """
    
    @staticmethod
    def analyze_bloom_filter(bf) -> BloomFilterStats:
        """
        Analyze a Bloom filter and return statistics.
        
        Args:
            bf: Bloom filter instance to analyze
            
        Returns:
            BloomFilterStats object with analysis results
        """
        return BloomFilterStats(
            expected_elements=bf.expected_elements,
            actual_elements=len(bf),
            size=bf.size,
            hash_count=bf.hash_count,
            false_positive_rate=bf.get_false_positive_rate(),
            memory_usage=bf.get_memory_usage(),
            load_factor=bf.get_load_factor(),
            theoretical_fpr=bf.false_positive_rate
        )
    
    @staticmethod
    def benchmark_operations(bf, test_items: List[Any], 
                           non_member_items: List[Any]) -> Dict[str, float]:
        """
        Benchmark Bloom filter operations.
        
        Args:
            bf: Bloom filter instance to benchmark
            test_items: List of items to add/query
            non_member_items: List of items not in the filter for false positive testing
            
        Returns:
            Dictionary with benchmark results
        """
        results = {}
        
        # Benchmark add operations
        add_time = timeit.timeit(
            lambda: [bf.add(item) for item in test_items],
            number=1
        )
        results['add_time'] = add_time / len(test_items)
        
        # Benchmark contains operations (members)
        contains_member_time = timeit.timeit(
            lambda: [bf.contains(item) for item in test_items],
            number=10
        )
        results['contains_member_time'] = contains_member_time / (len(test_items) * 10)
        
        # Benchmark contains operations (non-members)
        contains_non_member_time = timeit.timeit(
            lambda: [bf.contains(item) for item in non_member_items],
            number=10
        )
        results['contains_non_member_time'] = contains_non_member_time / (len(non_member_items) * 10)
        
        return results
    
    @staticmethod
    def measure_false_positives(bf, test_items: List[Any], 
                               non_member_items: List[Any]) -> Dict[str, float]:
        """
        Measure actual false positive rate.
        
        Args:
            bf: Bloom filter instance to test
            test_items: List of items to add to the filter
            non_member_items: List of items not in the filter
            
        Returns:
            Dictionary with false positive analysis results
        """
        # Add test items
        for item in test_items:
            bf.add(item)
        
        # Count false positives
        false_positives = sum(1 for item in non_member_items if bf.contains(item))
        actual_fpr = false_positives / len(non_member_items)
        
        return {
            'actual_false_positive_rate': actual_fpr,
            'theoretical_false_positive_rate': bf.get_false_positive_rate(),
            'false_positives': false_positives,
            'total_queries': len(non_member_items),
            'accuracy': 1 - actual_fpr,
            'fpr_error': abs(actual_fpr - bf.get_false_positive_rate())
        }
    
    @staticmethod
    def compare_with_set(bf, test_items: List[Any], 
                        query_items: List[Any]) -> Dict[str, Any]:
        """
        Compare Bloom filter performance with Python set.
        
        Args:
            bf: Bloom filter instance to compare
            test_items: List of items to add
            query_items: List of items to query
            
        Returns:
            Dictionary with comparison results
        """
        # Test Bloom filter
        bf_start = timeit.default_timer()
        for item in test_items:
            bf.add(item)
        bf_add_time = timeit.default_timer() - bf_start
        
        bf_query_start = timeit.default_timer()
        bf_results = [bf.contains(item) for item in query_items]
        bf_query_time = timeit.default_timer() - bf_query_start
        
        # Test Python set
        test_set = set()
        set_start = timeit.default_timer()
        for item in test_items:
            test_set.add(item)
        set_add_time = timeit.default_timer() - set_start
        
        set_query_start = timeit.default_timer()
        set_results = [item in test_set for item in query_items]
        set_query_time = timeit.default_timer() - set_query_start
        
        # Compare results
        correct_results = sum(1 for bf_res, set_res in zip(bf_results, set_results) 
                            if bf_res == set_res)
        accuracy = correct_results / len(query_items)
        
        return {
            'bloom_add_time': bf_add_time,
            'set_add_time': set_add_time,
            'bloom_query_time': bf_query_time,
            'set_query_time': set_query_time,
            'bloom_memory': bf.get_memory_usage(),
            'set_memory': sys.getsizeof(test_set) + sum(sys.getsizeof(item) for item in test_set),
            'accuracy': accuracy,
            'speedup_add': set_add_time / bf_add_time if bf_add_time > 0 else float('inf'),
            'speedup_query': set_query_time / bf_query_time if bf_query_time > 0 else float('inf'),
            'memory_ratio': bf.get_memory_usage() / (sys.getsizeof(test_set) + sum(sys.getsizeof(item) for item in test_set))
        }
    
    @staticmethod
    def analyze_memory_efficiency(bf, test_items: List[Any]) -> Dict[str, Any]:
        """
        Analyze memory efficiency of Bloom filter.
        
        Args:
            bf: Bloom filter instance to analyze
            test_items: List of items to add
            
        Returns:
            Dictionary with memory efficiency metrics
        """
        # Add items to Bloom filter
        for item in test_items:
            bf.add(item)
        
        bloom_memory = bf.get_memory_usage()
        
        # Compare with Python set
        test_set = set(test_items)
        set_memory = sys.getsizeof(test_set) + sum(sys.getsizeof(item) for item in test_set)
        
        # Calculate efficiency metrics
        memory_ratio = bloom_memory / set_memory
        memory_savings = (set_memory - bloom_memory) / set_memory
        
        return {
            'bloom_memory': bloom_memory,
            'set_memory': set_memory,
            'memory_ratio': memory_ratio,
            'memory_savings': memory_savings,
            'bits_per_element': bf.size / len(bf),
            'load_factor': bf.get_load_factor(),
            'false_positive_rate': bf.get_false_positive_rate()
        }
    
    @staticmethod
    def benchmark_scalability(bf_class, sizes: List[int], 
                            false_positive_rate: float = 0.01) -> Dict[str, List[float]]:
        """
        Benchmark Bloom filter scalability across different sizes.
        
        Args:
            bf_class: Bloom filter class to benchmark
            sizes: List of sizes to test
            false_positive_rate: False positive rate to use
            
        Returns:
            Dictionary with scalability benchmark results
        """
        results = {
            'sizes': sizes,
            'add_times': [],
            'query_times': [],
            'memory_usage': [],
            'false_positive_rates': []
        }
        
        for size in sizes:
            # Create Bloom filter
            bf = bf_class(expected_elements=size, false_positive_rate=false_positive_rate)
            
            # Generate test data
            test_items = [f"item_{i}" for i in range(size)]
            query_items = test_items + [f"query_{i}" for i in range(size)]
            
            # Benchmark add operations
            add_time = timeit.timeit(
                lambda: [bf.add(item) for item in test_items],
                number=1
            )
            results['add_times'].append(add_time / size)
            
            # Benchmark query operations
            query_time = timeit.timeit(
                lambda: [bf.contains(item) for item in query_items],
                number=5
            )
            results['query_times'].append(query_time / (len(query_items) * 5))
            
            # Record memory usage and false positive rate
            results['memory_usage'].append(bf.get_memory_usage())
            results['false_positive_rates'].append(bf.get_false_positive_rate())
        
        return results
    
    @staticmethod
    def analyze_hash_function_impact(bf_class, test_items: List[Any], 
                                   hash_counts: List[int]) -> Dict[str, List[float]]:
        """
        Analyze the impact of different numbers of hash functions.
        
        Args:
            bf_class: Bloom filter class to test
            test_items: List of items to test
            hash_counts: List of hash function counts to test
            
        Returns:
            Dictionary with hash function impact analysis
        """
        results = {
            'hash_counts': hash_counts,
            'false_positive_rates': [],
            'add_times': [],
            'query_times': [],
            'memory_usage': []
        }
        
        for hash_count in hash_counts:
            # Create Bloom filter with custom hash count
            bf = bf_class(expected_elements=len(test_items), false_positive_rate=0.01)
            
            # Override hash count for testing
            bf.hash_count = hash_count
            bf.hash_seeds = bf._generate_hash_seeds(hash_count)
            
            # Generate non-member items
            non_member_items = [f"non_member_{i}" for i in range(len(test_items))]
            
            # Add items and measure false positive rate
            for item in test_items:
                bf.add(item)
            
            false_positives = sum(1 for item in non_member_items if bf.contains(item))
            actual_fpr = false_positives / len(non_member_items)
            
            # Benchmark operations
            add_time = timeit.timeit(
                lambda: [bf.add(item) for item in test_items[:100]],
                number=1
            )
            
            query_time = timeit.timeit(
                lambda: [bf.contains(item) for item in test_items[:100]],
                number=10
            )
            
            results['false_positive_rates'].append(actual_fpr)
            results['add_times'].append(add_time / 100)
            results['query_times'].append(query_time / (100 * 10))
            results['memory_usage'].append(bf.get_memory_usage())
        
        return results
    
    @staticmethod
    def generate_performance_report(bf, test_items: List[Any], 
                                  non_member_items: List[Any]) -> str:
        """
        Generate a comprehensive performance report.
        
        Args:
            bf: Bloom filter instance to analyze
            test_items: List of items to add
            non_member_items: List of items not in the filter
            
        Returns:
            Formatted performance report string
        """
        # Gather all analysis data
        stats = BloomFilterAnalyzer.analyze_bloom_filter(bf)
        benchmark_results = BloomFilterAnalyzer.benchmark_operations(bf, test_items, non_member_items)
        false_positive_results = BloomFilterAnalyzer.measure_false_positives(bf, test_items, non_member_items)
        comparison_results = BloomFilterAnalyzer.compare_with_set(bf, test_items, test_items + non_member_items)
        memory_results = BloomFilterAnalyzer.analyze_memory_efficiency(bf, test_items)
        
        # Generate report
        report = []
        report.append("=" * 60)
        report.append("BLOOM FILTER PERFORMANCE REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Basic statistics
        report.append("BASIC STATISTICS:")
        report.append(f"  Expected elements: {stats.expected_elements}")
        report.append(f"  Actual elements: {stats.actual_elements}")
        report.append(f"  Bit array size: {stats.size}")
        report.append(f"  Hash functions: {stats.hash_count}")
        report.append(f"  Load factor: {stats.load_factor:.2%}")
        report.append("")
        
        # Performance metrics
        report.append("PERFORMANCE METRICS:")
        report.append(f"  Add time per element: {benchmark_results['add_time']:.6f} seconds")
        report.append(f"  Query time (members): {benchmark_results['contains_member_time']:.6f} seconds")
        report.append(f"  Query time (non-members): {benchmark_results['contains_non_member_time']:.6f} seconds")
        report.append("")
        
        # Accuracy metrics
        report.append("ACCURACY METRICS:")
        report.append(f"  Theoretical FPR: {stats.theoretical_fpr:.4f}")
        report.append(f"  Actual FPR: {false_positive_results['actual_false_positive_rate']:.4f}")
        report.append(f"  FPR error: {false_positive_results['fpr_error']:.4f}")
        report.append(f"  Accuracy: {false_positive_results['accuracy']:.2%}")
        report.append("")
        
        # Memory efficiency
        report.append("MEMORY EFFICIENCY:")
        report.append(f"  Bloom filter memory: {memory_results['bloom_memory']} bytes")
        report.append(f"  Set memory: {memory_results['set_memory']} bytes")
        report.append(f"  Memory ratio: {memory_results['memory_ratio']:.2f}x")
        report.append(f"  Memory savings: {memory_results['memory_savings']:.2%}")
        report.append("")
        
        # Comparison with set
        report.append("COMPARISON WITH PYTHON SET:")
        report.append(f"  Add speedup: {comparison_results['speedup_add']:.2f}x")
        report.append(f"  Query speedup: {comparison_results['speedup_query']:.2f}x")
        report.append(f"  Overall accuracy: {comparison_results['accuracy']:.2%}")
        report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report) 