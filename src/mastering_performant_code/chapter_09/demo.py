"""
B-Tree Demo and Performance Analysis

This script demonstrates the B-Tree implementation with comprehensive
examples, performance analysis, and real-world applications.
"""

import timeit
import random
import math
import sys
from typing import List, Dict, Any

# Add the parent directory to the path to import the chapter modules
sys.path.append('.')

from chapter_09 import (
    BTree, BTreeNode, BTreeAnalyzer, BTreeStats,
    DatabaseIndex, IndexEntry, MultiValueIndex, TimestampedIndex,
    b_tree_height_analysis
)

def demo_basic_operations():
    """Demonstrate basic B-Tree operations."""
    print("=" * 60)
    print("B-Tree Basic Operations Demo")
    print("=" * 60)
    
    # Create a B-Tree with minimum degree 3
    btree = BTree[int](min_degree=3)
    
    # Insert some keys
    keys = [10, 20, 5, 6, 12, 30, 7, 17]
    print(f"Inserting keys: {keys}")
    
    for key in keys:
        btree.insert(key)
        print(f"After inserting {key}: {list(btree.inorder_traversal())}")
    
    print(f"\nFinal B-Tree: {btree}")
    print(f"Size: {len(btree)}")
    print(f"Height: {btree.get_height()}")
    
    # Search for keys
    search_keys = [5, 15, 20, 25]
    print(f"\nSearching for keys: {search_keys}")
    for key in search_keys:
        result = btree.search(key)
        print(f"Search for {key}: {'Found' if result is not None else 'Not found'}")
    
    # Range query
    print(f"\nRange query [8, 18]: {btree.range_query(8, 18)}")
    
    # Delete some keys
    delete_keys = [6, 20, 10]
    print(f"\nDeleting keys: {delete_keys}")
    for key in delete_keys:
        deleted = btree.delete(key)
        print(f"Delete {key}: {'Success' if deleted else 'Not found'}")
        print(f"After deletion: {list(btree.inorder_traversal())}")

def demo_node_splitting():
    """Demonstrate B-Tree node splitting behavior."""
    print("\n" + "=" * 60)
    print("B-Tree Node Splitting Demo")
    print("=" * 60)
    
    # Create a B-Tree with minimum degree 2 (smaller for easier demonstration)
    btree = BTree[int](min_degree=2)
    
    # Insert keys to trigger splitting
    keys = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Inserting keys: {keys}")
    
    for i, key in enumerate(keys):
        btree.insert(key)
        print(f"After inserting {key} (step {i+1}):")
        print(f"  Size: {len(btree)}, Height: {btree.get_height()}")
        print(f"  Keys: {list(btree.inorder_traversal())}")
        
        # Show statistics
        stats = BTreeAnalyzer.analyze_btree(btree)
        print(f"  Memory usage: {stats.memory_usage:,} bytes")
        print(f"  Average keys per node: {stats.average_keys_per_node:.2f}")
        print(f"  Storage efficiency: {stats.storage_efficiency:.2f}")
        print()

def demo_different_min_degrees():
    """Compare B-Trees with different minimum degrees."""
    print("\n" + "=" * 60)
    print("B-Tree Minimum Degree Comparison")
    print("=" * 60)
    
    # Test data
    test_size = 1000
    test_data = list(range(test_size))
    random.shuffle(test_data)
    
    min_degrees = [2, 3, 5, 10]
    
    for min_degree in min_degrees:
        print(f"\nTesting B-Tree with minimum degree {min_degree}:")
        
        # Create B-Tree
        btree = BTree[int](min_degree=min_degree)
        
        # Insert data
        start_time = timeit.default_timer()
        for item in test_data:
            btree.insert(item)
        insert_time = timeit.default_timer() - start_time
        
        # Search test
        search_keys = random.sample(test_data, 100)
        start_time = timeit.default_timer()
        for key in search_keys:
            btree.search(key)
        search_time = timeit.default_timer() - start_time
        
        # Get statistics
        stats = BTreeAnalyzer.analyze_btree(btree)
        
        print(f"  Size: {stats.size}")
        print(f"  Height: {stats.height}")
        print(f"  Theoretical height: {stats.theoretical_height:.2f}")
        print(f"  Insert time: {insert_time:.4f}s")
        print(f"  Search time: {search_time:.4f}s")
        print(f"  Memory usage: {stats.memory_usage:,} bytes")
        print(f"  Average keys per node: {stats.average_keys_per_node:.2f}")
        print(f"  Storage efficiency: {stats.storage_efficiency:.2f}")

def demo_database_index():
    """Demonstrate the database index implementation."""
    print("\n" + "=" * 60)
    print("Database Index Demo")
    print("=" * 60)
    
    # Create a database index
    index = DatabaseIndex[str, str](min_degree=3)
    
    # Insert some data
    data = [
        ("user:1", "Alice Johnson"),
        ("user:2", "Bob Smith"),
        ("user:3", "Charlie Brown"),
        ("user:4", "Diana Prince"),
        ("user:5", "Eve Wilson"),
        ("order:1", "Product A"),
        ("order:2", "Product B"),
        ("order:3", "Product C"),
    ]
    
    print("Inserting data into index:")
    for key, value in data:
        index.insert(key, value)
        print(f"  {key} -> {value}")
    
    print(f"\nIndex size: {len(index)}")
    
    # Search for specific keys
    search_keys = ["user:2", "order:1", "user:10"]
    print(f"\nSearching for keys: {search_keys}")
    for key in search_keys:
        value = index.get(key)
        print(f"  {key} -> {value}")
    
    # Range query
    print(f"\nRange query ['order:', 'order:z']:")
    results = index.range_query("order:", "order:z")
    for key, value in results:
        print(f"  {key} -> {value}")
    
    # Get statistics
    stats = index.get_stats()
    print(f"\nIndex statistics:")
    print(f"  Height: {stats['height']}")
    print(f"  Memory usage: {stats['memory_usage']:,} bytes")
    print(f"  Storage efficiency: {stats['storage_efficiency']:.2f}")

def demo_multi_value_index():
    """Demonstrate the multi-value index."""
    print("\n" + "=" * 60)
    print("Multi-Value Index Demo")
    print("=" * 60)
    
    # Create a multi-value index
    index = MultiValueIndex[str, str](min_degree=3)
    
    # Insert data (multiple values per key)
    data = [
        ("tag:python", "data-structures"),
        ("tag:python", "algorithms"),
        ("tag:python", "tutorial"),
        ("tag:database", "indexing"),
        ("tag:database", "performance"),
        ("tag:algorithm", "sorting"),
        ("tag:algorithm", "searching"),
    ]
    
    print("Inserting data into multi-value index:")
    for key, value in data:
        index.insert(key, value)
        print(f"  {key} -> {value}")
    
    print(f"\nTotal values: {len(index)}")
    
    # Get all values for specific keys
    keys = ["tag:python", "tag:database", "tag:algorithm"]
    print(f"\nGetting values for keys: {keys}")
    for key in keys:
        values = index.get(key)
        print(f"  {key} -> {values}")
    
    # Delete specific values
    print(f"\nDeleting 'tutorial' from 'tag:python':")
    deleted = index.delete("tag:python", "tutorial")
    print(f"  Deleted: {deleted}")
    print(f"  Remaining values for 'tag:python': {index.get('tag:python')}")

def demo_timestamped_index():
    """Demonstrate the timestamped index."""
    print("\n" + "=" * 60)
    print("Timestamped Index Demo")
    print("=" * 60)
    
    import time
    
    # Create a timestamped index
    index = TimestampedIndex[str, str](min_degree=3)
    
    # Insert data with timestamps
    base_time = time.time()
    data = [
        ("session:1", "user_login", base_time),
        ("session:2", "user_login", base_time + 10),
        ("session:3", "user_login", base_time + 20),
        ("session:1", "user_logout", base_time + 30),
        ("session:2", "user_logout", base_time + 40),
    ]
    
    print("Inserting data into timestamped index:")
    for key, value, timestamp in data:
        index.insert(key, value, timestamp)
        print(f"  {key} -> {value} (at {timestamp:.2f})")
    
    print(f"\nIndex size: {len(index)}")
    
    # Get entries with timestamps
    print(f"\nGetting entries with timestamps:")
    for key, (value, ts) in index.get_all():
        print(f"  {key} -> {value} (at {ts:.2f})")
    
    # Get entries after a certain time
    cutoff_time = base_time + 15
    print(f"\nEntries after {cutoff_time:.2f}:")
    recent_entries = index.get_entries_after(cutoff_time)
    for key, (value, ts) in recent_entries:
        print(f"  {key} -> {value} (at {ts:.2f})")

def demo_performance_analysis():
    """Run comprehensive performance analysis."""
    print("\n" + "=" * 60)
    print("Performance Analysis")
    print("=" * 60)
    
    # Run the built-in performance analysis
    BTreeAnalyzer.benchmark_btree_variants()
    BTreeAnalyzer.compare_with_alternatives()

def demo_height_analysis():
    """Demonstrate B-Tree height analysis."""
    print("\n" + "=" * 60)
    print("B-Tree Height Analysis")
    print("=" * 60)
    
    # Analyze different configurations
    configurations = [
        (100, 2),
        (100, 3),
        (100, 5),
        (1000, 2),
        (1000, 3),
        (1000, 5),
        (10000, 3),
    ]
    
    print(f"{'Nodes':<8} {'Min Degree':<12} {'Min Height':<12} {'Max Height':<12} {'Actual':<8} {'Efficiency':<12}")
    print("-" * 80)
    
    for nodes, min_degree in configurations:
        analysis = b_tree_height_analysis(nodes, min_degree)
        print(f"{analysis['nodes']:<8} {analysis['min_degree']:<12} "
              f"{analysis['min_height']:<12.2f} {analysis['max_height']:<12.2f} "
              f"{analysis['actual_height']:<8} {analysis['storage_efficiency']:<12.2f}")

def main():
    """Run all demos."""
    print("B-Tree Fundamentals - Comprehensive Demo")
    print("=" * 80)
    
    try:
        # Run all demos
        demo_basic_operations()
        demo_node_splitting()
        demo_different_min_degrees()
        demo_database_index()
        demo_multi_value_index()
        demo_timestamped_index()
        demo_height_analysis()
        demo_performance_analysis()
        
        print("\n" + "=" * 80)
        print("All demos completed successfully!")
        print("=" * 80)
        
    except Exception as e:
        print(f"Error during demo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 