"""
Comprehensive benchmarking module for hash table implementations.

This module provides detailed performance analysis and comparison of all
hash table implementations against Python's built-in dict.
"""

import timeit
import random
import string
from typing import Type, Dict, List, Any, Callable
from collections import defaultdict
import statistics

from .hash_table import (
    HashTableInterface,
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
)


def generate_random_strings(count: int, length: int = 10) -> List[str]:
    """Generate random strings for testing."""
    return [''.join(random.choices(string.ascii_letters, k=length)) 
            for _ in range(count)]


def generate_random_integers(count: int, max_val: int = 1000000) -> List[int]:
    """Generate random integers for testing."""
    return [random.randint(0, max_val) for _ in range(count)]


def benchmark_operation(
    hash_table_class: Type[HashTableInterface],
    operation: str,
    data_size: int,
    data_type: str = "strings"
) -> float:
    """Benchmark a specific operation on a hash table implementation."""
    
    if data_type == "strings":
        keys = generate_random_strings(data_size)
        values = generate_random_strings(data_size)
    else:
        keys = generate_random_integers(data_size)
        values = generate_random_integers(data_size)
    
    def setup():
        return hash_table_class(), keys, values
    
    def insert_operation():
        ht, k, v = setup()
        for key, value in zip(k, v):
            ht[key] = value
        return ht
    
    def lookup_operation():
        ht, k, v = setup()
        for key, value in zip(k, v):
            ht[key] = value
        
        # Lookup all keys
        for key in k:
            _ = ht[key]
        return ht
    
    def delete_operation():
        ht, k, v = setup()
        for key, value in zip(k, v):
            ht[key] = value
        
        # Delete half the keys
        for key in k[:len(k)//2]:
            del ht[key]
        return ht
    
    def mixed_operation():
        ht, k, v = setup()
        # Insert all
        for key, value in zip(k, v):
            ht[key] = value
        
        # Lookup some
        for key in k[:len(k)//3]:
            _ = ht[key]
        
        # Delete some
        for key in k[len(k)//3:2*len(k)//3]:
            del ht[key]
        
        # Insert more
        for key, value in zip(k[2*len(k)//3:], v[2*len(k)//3:]):
            ht[key] = value
        
        return ht
    
    operations = {
        'insert': insert_operation,
        'lookup': lookup_operation,
        'delete': delete_operation,
        'mixed': mixed_operation
    }
    
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    
    # Run benchmark
    timer = timeit.Timer(operations[operation])
    times = timer.repeat(repeat=5, number=1)
    
    # Return median time
    return statistics.median(times)


def benchmark_python_dict(
    operation: str,
    data_size: int,
    data_type: str = "strings"
) -> float:
    """Benchmark Python's built-in dict for comparison."""
    
    if data_type == "strings":
        keys = generate_random_strings(data_size)
        values = generate_random_strings(data_size)
    else:
        keys = generate_random_integers(data_size)
        values = generate_random_integers(data_size)
    
    def insert_operation():
        d = {}
        for key, value in zip(keys, values):
            d[key] = value
        return d
    
    def lookup_operation():
        d = {}
        for key, value in zip(keys, values):
            d[key] = value
        
        for key in keys:
            _ = d[key]
        return d
    
    def delete_operation():
        d = {}
        for key, value in zip(keys, values):
            d[key] = value
        
        for key in keys[:len(keys)//2]:
            del d[key]
        return d
    
    def mixed_operation():
        d = {}
        # Insert all
        for key, value in zip(keys, values):
            d[key] = value
        
        # Lookup some
        for key in keys[:len(keys)//3]:
            _ = d[key]
        
        # Delete some
        for key in keys[len(keys)//3:2*len(keys)//3]:
            del d[key]
        
        # Insert more
        for key, value in zip(keys[2*len(keys)//3:], values[2*len(keys)//3:]):
            d[key] = value
        
        return d
    
    operations = {
        'insert': insert_operation,
        'lookup': lookup_operation,
        'delete': delete_operation,
        'mixed': mixed_operation
    }
    
    timer = timeit.Timer(operations[operation])
    times = timer.repeat(repeat=5, number=1)
    
    return statistics.median(times)


def comprehensive_benchmark(
    data_sizes: List[int] = None,
    operations: List[str] = None,
    data_types: List[str] = None
) -> Dict[str, Any]:
    """
    Run comprehensive benchmark comparing all implementations.
    
    Args:
        data_sizes: List of data sizes to test
        operations: List of operations to test
        data_types: List of data types to test
    
    Returns:
        Dictionary containing benchmark results
    """
    if data_sizes is None:
        data_sizes = [100, 1000, 10000]
    if operations is None:
        operations = ['insert', 'lookup', 'delete', 'mixed']
    if data_types is None:
        data_types = ['strings', 'integers']
    
    implementations = [
        ('SeparateChaining', SeparateChainingHashTable),
        ('LinearProbing', LinearProbingHashTable),
        ('QuadraticProbing', QuadraticProbingHashTable),
        ('DoubleHashing', DoubleHashingHashTable),
        ('PythonDict', None)  # Special case for built-in dict
    ]
    
    results = {
        'implementations': [impl[0] for impl in implementations],
        'data_sizes': data_sizes,
        'operations': operations,
        'data_types': data_types,
        'benchmarks': {}
    }
    
    for impl_name, impl_class in implementations:
        print(f"\nBenchmarking {impl_name}...")
        results['benchmarks'][impl_name] = {}
        
        for data_type in data_types:
            results['benchmarks'][impl_name][data_type] = {}
            
            for size in data_sizes:
                results['benchmarks'][impl_name][data_type][size] = {}
                
                for operation in operations:
                    try:
                        if impl_name == 'PythonDict':
                            time_taken = benchmark_python_dict(operation, size, data_type)
                        else:
                            time_taken = benchmark_operation(impl_class, operation, size, data_type)
                        
                        results['benchmarks'][impl_name][data_type][size][operation] = time_taken
                        print(f"  {operation} {size} {data_type}: {time_taken:.6f} seconds")
                        
                    except Exception as e:
                        print(f"  Error benchmarking {operation} {size} {data_type}: {e}")
                        results['benchmarks'][impl_name][data_type][size][operation] = None
    
    return results


def analyze_performance_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze benchmark results and generate insights."""
    analysis = {
        'fastest_implementation': {},
        'performance_ratios': {},
        'scalability_analysis': {},
        'recommendations': []
    }
    
    for data_type in results['data_types']:
        analysis['fastest_implementation'][data_type] = {}
        analysis['performance_ratios'][data_type] = {}
        
        for operation in results['operations']:
            for size in results['data_sizes']:
                # Find fastest implementation
                times = {}
                for impl in results['implementations']:
                    if impl in results['benchmarks']:
                        time_val = results['benchmarks'][impl][data_type][size][operation]
                        if time_val is not None:
                            times[impl] = time_val
                
                if times:
                    fastest = min(times, key=times.get)
                    analysis['fastest_implementation'][data_type][f"{operation}_{size}"] = fastest
                    
                    # Calculate performance ratios relative to Python dict
                    if 'PythonDict' in times:
                        python_time = times['PythonDict']
                        ratios = {impl: time_val / python_time for impl, time_val in times.items()}
                        analysis['performance_ratios'][data_type][f"{operation}_{size}"] = ratios
    
    # Generate recommendations
    recommendations = []
    
    # Check for best overall performance
    total_wins = defaultdict(int)
    for data_type in results['data_types']:
        for key, winner in analysis['fastest_implementation'][data_type].items():
            total_wins[winner] += 1
    
    if total_wins:
        best_overall = max(total_wins, key=total_wins.get)
        recommendations.append(f"Best overall performance: {best_overall} ({total_wins[best_overall]} wins)")
    
    # Check for scalability issues
    for impl in results['implementations']:
        if impl == 'PythonDict':
            continue
        
        for data_type in results['data_types']:
            for operation in results['operations']:
                times = []
                for size in results['data_sizes']:
                    time_val = results['benchmarks'][impl][data_type][size][operation]
                    if time_val is not None:
                        times.append(time_val)
                
                if len(times) >= 2:
                    # Check if performance degrades significantly
                    if times[-1] > times[0] * 10:  # 10x slower
                        recommendations.append(
                            f"{impl} shows poor scalability for {operation} with {data_type}: "
                            f"{times[0]:.6f}s -> {times[-1]:.6f}s"
                        )
    
    analysis['recommendations'] = recommendations
    return analysis


def print_benchmark_report(results: Dict[str, Any], analysis: Dict[str, Any]):
    """Print a formatted benchmark report."""
    print("\n" + "="*80)
    print("HASH TABLE IMPLEMENTATION BENCHMARK REPORT")
    print("="*80)
    
    print("\n1. PERFORMANCE SUMMARY")
    print("-" * 40)
    
    for data_type in results['data_types']:
        print(f"\n{data_type.upper()} DATA:")
        for operation in results['operations']:
            print(f"\n  {operation.upper()} OPERATION:")
            for size in results['data_sizes']:
                print(f"    Size {size}:")
                times = []
                for impl in results['implementations']:
                    if impl in results['benchmarks']:
                        time_val = results['benchmarks'][impl][data_type][size][operation]
                        if time_val is not None:
                            times.append((impl, time_val))
                
                # Sort by time
                times.sort(key=lambda x: x[1])
                for impl, time_val in times:
                    print(f"      {impl:20}: {time_val:.6f}s")
    
    print("\n2. FASTEST IMPLEMENTATIONS")
    print("-" * 40)
    for data_type in results['data_types']:
        print(f"\n{data_type.upper()} DATA:")
        for operation in results['operations']:
            for size in results['data_sizes']:
                key = f"{operation}_{size}"
                if key in analysis['fastest_implementation'][data_type]:
                    fastest = analysis['fastest_implementation'][data_type][key]
                    print(f"  {operation} {size} items: {fastest}")
    
    print("\n3. PERFORMANCE RATIOS (vs Python Dict)")
    print("-" * 40)
    for data_type in results['data_types']:
        print(f"\n{data_type.upper()} DATA:")
        for operation in results['operations']:
            for size in results['data_sizes']:
                key = f"{operation}_{size}"
                if key in analysis['performance_ratios'][data_type]:
                    ratios = analysis['performance_ratios'][data_type][key]
                    print(f"\n  {operation} {size} items:")
                    for impl, ratio in sorted(ratios.items(), key=lambda x: x[1]):
                        print(f"    {impl:20}: {ratio:.2f}x")
    
    print("\n4. RECOMMENDATIONS")
    print("-" * 40)
    for rec in analysis['recommendations']:
        print(f"  • {rec}")


def run_load_factor_analysis(
    hash_table_class: Type[HashTableInterface],
    data_size: int = 10000
) -> Dict[str, Any]:
    """Analyze performance at different load factors."""
    load_factors = [0.25, 0.5, 0.75, 0.9, 0.95]
    results = {}
    
    for lf in load_factors:
        print(f"Testing load factor {lf}...")
        
        # Create hash table with specific load factor
        ht = hash_table_class(load_factor=lf)
        
        # Insert data
        keys = generate_random_strings(data_size)
        values = generate_random_strings(data_size)
        
        insert_start = timeit.default_timer()
        for key, value in zip(keys, values):
            ht[key] = value
        insert_time = timeit.default_timer() - insert_start
        
        # Lookup performance
        lookup_start = timeit.default_timer()
        for key in keys:
            _ = ht[key]
        lookup_time = timeit.default_timer() - lookup_start
        
        # Get statistics
        stats = ht.get_statistics()
        
        results[lf] = {
            'insert_time': insert_time,
            'lookup_time': lookup_time,
            'statistics': stats,
            'memory_info': ht.get_memory_info(),
            'hash_distribution': ht.analyze_hash_distribution()
        }
    
    return results


if __name__ == "__main__":
    # Run comprehensive benchmark
    print("Running comprehensive hash table benchmark...")
    results = comprehensive_benchmark()
    analysis = analyze_performance_results(results)
    print_benchmark_report(results, analysis)
    
    # Run load factor analysis
    print("\n" + "="*80)
    print("LOAD FACTOR ANALYSIS")
    print("="*80)
    
    for impl_name, impl_class in [
        ('SeparateChaining', SeparateChainingHashTable),
        ('LinearProbing', LinearProbingHashTable),
        ('QuadraticProbing', QuadraticProbingHashTable),
        ('DoubleHashing', DoubleHashingHashTable)
    ]:
        print(f"\n{impl_name} Load Factor Analysis:")
        lf_results = run_load_factor_analysis(impl_class)
        
        for lf, data in lf_results.items():
            print(f"  Load Factor {lf}:")
            print(f"    Insert: {data['insert_time']:.6f}s")
            print(f"    Lookup: {data['lookup_time']:.6f}s")
            print(f"    Resize Count: {data['statistics']['resize_count']}")
            print(f"    Average Probes: {data['statistics']['average_probes']:.2f}")
            print(f"    Max Bucket Size: {data['hash_distribution']['max_bucket_size']}") 