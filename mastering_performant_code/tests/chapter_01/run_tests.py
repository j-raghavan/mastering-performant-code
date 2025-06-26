#!/usr/bin/env python3
"""
Test runner for Chapter 1: Built-ins Under the Hood

This script runs all unit tests for Chapter 1 implementations and provides
coverage reporting and performance benchmarks.
"""

import unittest
import sys
import os
import timeit
from typing import List, Dict, Any

# Try to import coverage, but make it optional
try:
    import coverage
    COVERAGE_AVAILABLE = True
except ImportError:
    COVERAGE_AVAILABLE = False
    print("Note: coverage package not available. Coverage analysis will be skipped.")

# Add the code directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def run_unit_tests() -> bool:
    """Run all unit tests for Chapter 1."""
    print("=" * 60)
    print("Running Unit Tests for Chapter 1")
    print("=" * 60)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(__file__)
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print(f"\nTest Results:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Success: {result.wasSuccessful()}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    return result.wasSuccessful()

def run_coverage_analysis() -> Dict[str, Any]:
    """Run coverage analysis for Chapter 1 code."""
    if not COVERAGE_AVAILABLE:
        print("\n" + "=" * 60)
        print("Coverage Analysis (Skipped - coverage package not available)")
        print("=" * 60)
        print("To enable coverage analysis, install the coverage package:")
        print("  pip install coverage")
        return {'total_coverage': 'N/A', 'coverage_data': None}
    
    print("\n" + "=" * 60)
    print("Running Coverage Analysis")
    print("=" * 60)
    
    # Start coverage measurement
    cov = coverage.Coverage()
    cov.start()
    
    # Import and run tests to measure coverage
    import test_dynamic_array
    import test_hash_table
    import test_simple_set
    import test_analyzer
    import test_config_manager
    
    # Run tests
    unittest.main(module=test_dynamic_array, exit=False, verbosity=0)
    unittest.main(module=test_hash_table, exit=False, verbosity=0)
    unittest.main(module=test_simple_set, exit=False, verbosity=0)
    unittest.main(module=test_analyzer, exit=False, verbosity=0)
    unittest.main(module=test_config_manager, exit=False, verbosity=0)
    
    # Stop coverage measurement
    cov.stop()
    cov.save()
    
    # Generate coverage report
    print("\nCoverage Report:")
    cov.report()
    
    # Get coverage data
    total_coverage = cov.report()
    
    return {
        'total_coverage': total_coverage,
        'coverage_data': cov.get_data()
    }

def run_performance_benchmarks() -> Dict[str, Any]:
    """Run performance benchmarks comparing our implementations with built-ins."""
    print("\n" + "=" * 60)
    print("Running Performance Benchmarks")
    print("=" * 60)
    
    from src.chapter_01.dynamic_array import DynamicArray
    from src.chapter_01.hash_table import HashTable
    from src.chapter_01.simple_set import SimpleSet
    
    results = {}
    
    # DynamicArray vs List benchmarks
    print("\nDynamicArray vs List Benchmarks:")
    print("-" * 40)
    
    # Append operations
    list_append_time = timeit.timeit(
        "lst.append(i) for i in range(1000)",
        setup="lst = []",
        number=1
    )
    
    array_append_time = timeit.timeit(
        "arr.append(i) for i in range(1000)",
        setup="from src.chapter_01.dynamic_array import DynamicArray; arr = DynamicArray()",
        number=1
    )
    
    print(f"Append 1000 items:")
    print(f"  Built-in list: {list_append_time:.6f} seconds")
    print(f"  DynamicArray:  {array_append_time:.6f} seconds")
    print(f"  Ratio: {array_append_time/list_append_time:.2f}x")
    
    results['append'] = {
        'list': list_append_time,
        'dynamic_array': array_append_time,
        'ratio': array_append_time / list_append_time
    }
    
    # Access operations
    list_access_time = timeit.timeit(
        "lst[i] for i in range(1000)",
        setup="lst = list(range(1000))",
        number=100
    )
    
    array_access_time = timeit.timeit(
        "arr[i] for i in range(1000)",
        setup="from src.chapter_01.dynamic_array import DynamicArray; arr = DynamicArray(); [arr.append(i) for i in range(1000)]",
        number=100
    )
    
    print(f"\nAccess 1000 items:")
    print(f"  Built-in list: {list_access_time:.6f} seconds")
    print(f"  DynamicArray:  {array_access_time:.6f} seconds")
    print(f"  Ratio: {array_access_time/list_access_time:.2f}x")
    
    results['access'] = {
        'list': list_access_time,
        'dynamic_array': array_access_time,
        'ratio': array_access_time / list_access_time
    }
    
    # HashTable vs Dict benchmarks
    print("\nHashTable vs Dict Benchmarks:")
    print("-" * 40)
    
    # Set operations
    dict_set_time = timeit.timeit(
        "dct[f'key{i}'] = i for i in range(1000)",
        setup="dct = {}",
        number=1
    )
    
    hash_set_time = timeit.timeit(
        "ht[f'key{i}'] = i for i in range(1000)",
        setup="from src.chapter_01.hash_table import HashTable; ht = HashTable()",
        number=1
    )
    
    print(f"Set 1000 items:")
    print(f"  Built-in dict: {dict_set_time:.6f} seconds")
    print(f"  HashTable:     {hash_set_time:.6f} seconds")
    print(f"  Ratio: {hash_set_time/dict_set_time:.2f}x")
    
    results['set'] = {
        'dict': dict_set_time,
        'hash_table': hash_set_time,
        'ratio': hash_set_time / dict_set_time
    }
    
    # Get operations
    dict_get_time = timeit.timeit(
        "dct[f'key{i}'] for i in range(1000)",
        setup="dct = {f'key{i}': i for i in range(1000)}",
        number=100
    )
    
    hash_get_time = timeit.timeit(
        "ht[f'key{i}'] for i in range(1000)",
        setup="from src.chapter_01.hash_table import HashTable; ht = HashTable(); [ht.__setitem__(f'key{i}', i) for i in range(1000)]",
        number=100
    )
    
    print(f"\nGet 1000 items:")
    print(f"  Built-in dict: {dict_get_time:.6f} seconds")
    print(f"  HashTable:     {hash_get_time:.6f} seconds")
    print(f"  Ratio: {hash_get_time/dict_get_time:.2f}x")
    
    results['get'] = {
        'dict': dict_get_time,
        'hash_table': hash_get_time,
        'ratio': hash_get_time / dict_get_time
    }
    
    # SimpleSet vs Set benchmarks
    print("\nSimpleSet vs Set Benchmarks:")
    print("-" * 40)
    
    # Add operations
    set_add_time = timeit.timeit(
        "st.add(i) for i in range(1000)",
        setup="st = set()",
        number=1
    )
    
    simple_add_time = timeit.timeit(
        "ss.add(i) for i in range(1000)",
        setup="from src.chapter_01.simple_set import SimpleSet; ss = SimpleSet()",
        number=1
    )
    
    print(f"Add 1000 items:")
    print(f"  Built-in set:  {set_add_time:.6f} seconds")
    print(f"  SimpleSet:     {simple_add_time:.6f} seconds")
    print(f"  Ratio: {simple_add_time/set_add_time:.2f}x")
    
    results['add'] = {
        'set': set_add_time,
        'simple_set': simple_add_time,
        'ratio': simple_add_time / set_add_time
    }
    
    # Contains operations
    set_contains_time = timeit.timeit(
        "i in st for i in range(1000)",
        setup="st = set(range(1000))",
        number=100
    )
    
    simple_contains_time = timeit.timeit(
        "i in ss for i in range(1000)",
        setup="from src.chapter_01.simple_set import SimpleSet; ss = SimpleSet(); [ss.add(i) for i in range(1000)]",
        number=100
    )
    
    print(f"\nContains 1000 items:")
    print(f"  Built-in set:  {set_contains_time:.6f} seconds")
    print(f"  SimpleSet:     {simple_contains_time:.6f} seconds")
    print(f"  Ratio: {simple_contains_time/set_contains_time:.2f}x")
    
    results['contains'] = {
        'set': set_contains_time,
        'simple_set': simple_contains_time,
        'ratio': simple_contains_time / set_contains_time
    }
    
    return results

def run_memory_analysis() -> Dict[str, Any]:
    """Run memory usage analysis."""
    print("\n" + "=" * 60)
    print("Running Memory Analysis")
    print("=" * 60)
    
    import sys
    from src.chapter_01.dynamic_array import MemoryTrackedDynamicArray
    from src.chapter_01.hash_table import MemoryTrackedHashTable
    from src.chapter_01.simple_set import SimpleSet
    from src.chapter_01.analyzer import BuiltinAnalyzer
    
    results = {}
    
    # Test with different data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"\nMemory usage with {size} elements:")
        print("-" * 40)
        
        # List comparison
        lst = list(range(size))
        arr = MemoryTrackedDynamicArray()
        for i in range(size):
            arr.append(i)
        
        list_memory = sys.getsizeof(lst)
        array_memory = arr.get_memory_info().object_size
        
        print(f"List:")
        print(f"  Built-in: {list_memory} bytes")
        print(f"  DynamicArray: {array_memory} bytes")
        print(f"  Ratio: {array_memory/list_memory:.2f}x")
        
        results[f'list_{size}'] = {
            'built_in': list_memory,
            'dynamic_array': array_memory,
            'ratio': array_memory / list_memory
        }
        
        # Dict comparison
        dct = {f"key{i}": i for i in range(size)}
        ht = MemoryTrackedHashTable()
        for i in range(size):
            ht[f"key{i}"] = i
        
        dict_memory = sys.getsizeof(dct)
        hash_memory = ht.get_memory_info().object_size
        
        print(f"Dict:")
        print(f"  Built-in: {dict_memory} bytes")
        print(f"  HashTable: {hash_memory} bytes")
        print(f"  Ratio: {hash_memory/dict_memory:.2f}x")
        
        results[f'dict_{size}'] = {
            'built_in': dict_memory,
            'hash_table': hash_memory,
            'ratio': hash_memory / dict_memory
        }
        
        # Set comparison
        st = set(range(size))
        ss = SimpleSet()
        for i in range(size):
            ss.add(i)
        
        set_memory = sys.getsizeof(st)
        simple_memory = ss._hash_table.get_memory_info().object_size
        
        print(f"Set:")
        print(f"  Built-in: {set_memory} bytes")
        print(f"  SimpleSet: {simple_memory} bytes")
        print(f"  Ratio: {simple_memory/set_memory:.2f}x")
        
        results[f'set_{size}'] = {
            'built_in': set_memory,
            'simple_set': simple_memory,
            'ratio': simple_memory / set_memory
        }
    
    return results

def main():
    """Main function to run all tests and analysis."""
    print("Chapter 1: Built-ins Under the Hood - Test Suite")
    print("=" * 60)
    
    # Run unit tests
    test_success = run_unit_tests()
    
    # Run coverage analysis
    if COVERAGE_AVAILABLE:
        coverage_data = run_coverage_analysis()
    else:
        coverage_data = {'total_coverage': 'N/A', 'coverage_data': None}
    
    # Run performance benchmarks
    benchmark_data = run_performance_benchmarks()
    
    # Run memory analysis
    memory_data = run_memory_analysis()
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    print(f"Unit Tests: {'PASSED' if test_success else 'FAILED'}")
    print(f"Coverage: {coverage_data.get('total_coverage', 'N/A')}")
    
    # Performance summary
    print("\nPerformance Summary:")
    print(f"  DynamicArray vs List: {benchmark_data['append']['ratio']:.2f}x slower for append")
    print(f"  HashTable vs Dict: {benchmark_data['set']['ratio']:.2f}x slower for set")
    print(f"  SimpleSet vs Set: {benchmark_data['add']['ratio']:.2f}x slower for add")
    
    # Memory summary
    print("\nMemory Summary (1000 elements):")
    print(f"  DynamicArray vs List: {memory_data['list_1000']['ratio']:.2f}x more memory")
    print(f"  HashTable vs Dict: {memory_data['dict_1000']['ratio']:.2f}x more memory")
    print(f"  SimpleSet vs Set: {memory_data['set_1000']['ratio']:.2f}x more memory")
    
    return test_success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 