"""
B-Tree Analyzer and Performance Tools

This module provides tools for analyzing B-Tree performance, memory usage,
and comparing with other data structures.
"""

import sys
import timeit
import math
import random
from typing import TypeVar, Generic, List, Dict, Any
from dataclasses import dataclass
from .btree import BTree
from .btree_node import BTreeNode

T = TypeVar('T')

@dataclass
class BTreeStats:
    """Statistics about a B-Tree."""
    size: int
    height: int
    min_degree: int
    memory_usage: int
    average_keys_per_node: float
    storage_efficiency: float
    theoretical_height: float

class BTreeAnalyzer:
    """
    Analyzer for B-Tree performance and characteristics.
    
    This class provides tools to analyze the performance and memory
    characteristics of B-Trees with different configurations.
    """
    
    @staticmethod
    def analyze_btree(btree: BTree[T]) -> BTreeStats:
        """Analyze a B-Tree and return statistics."""
        if btree.root is None:
            return BTreeStats(
                size=0,
                height=0,
                min_degree=btree.min_degree,
                memory_usage=sys.getsizeof(btree),
                average_keys_per_node=0.0,
                storage_efficiency=0.0,
                theoretical_height=0.0
            )
        
        # Calculate memory usage
        memory_usage = btree.get_memory_usage()
        
        # Calculate average keys per node
        total_nodes = BTreeAnalyzer._count_nodes(btree.root)
        average_keys_per_node = btree.size / total_nodes if total_nodes > 0 else 0
        
        # Calculate storage efficiency
        max_possible_keys = total_nodes * btree.max_keys
        storage_efficiency = btree.size / max_possible_keys if max_possible_keys > 0 else 0
        
        # Calculate theoretical height
        theoretical_height = math.log((btree.size + 1) / 2, btree.min_degree)
        
        return BTreeStats(
            size=btree.size,
            height=btree.height,
            min_degree=btree.min_degree,
            memory_usage=memory_usage,
            average_keys_per_node=average_keys_per_node,
            storage_efficiency=storage_efficiency,
            theoretical_height=theoretical_height
        )
    
    @staticmethod
    def _count_nodes(node: BTreeNode[T]) -> int:
        """Count the number of nodes in a subtree."""
        if node.is_leaf:
            return 1
        
        count = 1
        for i in range(node.num_keys + 1):
            if node.children[i]:
                count += BTreeAnalyzer._count_nodes(node.children[i])
        return count
    
    @staticmethod
    def benchmark_operations(btree: BTree[T], operations: List[str], iterations: int = 1000) -> Dict[str, float]:
        """Benchmark common operations on a B-Tree."""
        results = {}
        
        # Generate test data
        test_keys = list(range(1000))
        random.shuffle(test_keys)
        
        for operation in operations:
            if operation == "insert":
                setup = f"btree = BTree(min_degree={btree.min_degree})"
                stmt = "btree.insert(random.randint(0, 999))"
            elif operation == "search":
                setup = f"btree = BTree(min_degree={btree.min_degree}); [btree.insert(k) for k in {test_keys[:100]}]; key = 50"
                stmt = "btree.search(key)"
            elif operation == "delete":
                setup = f"btree = BTree(min_degree={btree.min_degree}); [btree.insert(k) for k in {test_keys[:100]}]; key = 50"
                stmt = "btree.delete(key)"
            elif operation == "range_query":
                setup = f"btree = BTree(min_degree={btree.min_degree}); [btree.insert(k) for k in {test_keys[:100]}]"
                stmt = "btree.range_query(20, 80)"
            elif operation == "inorder_traversal":
                setup = f"btree = BTree(min_degree={btree.min_degree}); [btree.insert(k) for k in {test_keys[:100]}]"
                stmt = "list(btree.inorder_traversal())"
            else:
                continue
            
            time = timeit.timeit(stmt, setup=setup, number=iterations, globals={'random': random})
            results[operation] = time
        
        return results
    
    @staticmethod
    def compare_with_builtins(btree: BTree[T], data_size: int = 1000) -> Dict[str, Dict[str, float]]:
        """Compare B-Tree performance with built-in data structures."""
        # Generate test data
        test_data = list(range(data_size))
        random.shuffle(test_data)
        
        # Test B-Tree
        btree_test = BTree(min_degree=btree.min_degree)
        for item in test_data:
            btree_test.insert(item)
        
        btree_results = BTreeAnalyzer.benchmark_operations(btree_test, ["search", "insert", "delete"])
        
        # Test built-in set
        set_test = set(test_data)
        set_results = {
            "search": timeit.timeit("50 in set_test", globals={'set_test': set_test}, number=1000),
            "insert": timeit.timeit("set_test.add(random.randint(0, 999))", globals={'set_test': set_test, 'random': random}, number=1000),
            "delete": timeit.timeit("set_test.discard(50)", globals={'set_test': set_test}, number=1000)
        }
        
        # Test built-in list (for comparison)
        list_test = sorted(test_data)
        list_results = {
            "search": timeit.timeit("50 in list_test", globals={'list_test': list_test}, number=1000),
            "insert": timeit.timeit("list_test.append(random.randint(0, 999)); list_test.sort()", globals={'list_test': list_test, 'random': random}, number=1000),
            "delete": timeit.timeit("list_test.remove(50) if 50 in list_test else None", globals={'list_test': list_test}, number=1000)
        }
        
        return {
            "btree": btree_results,
            "set": set_results,
            "list": list_results
        }
    
    @staticmethod
    def analyze_height_distribution(min_degree: int, max_size: int = 10000) -> Dict[str, Any]:
        """Analyze how B-Tree height varies with size and minimum degree."""
        results = {
            'sizes': [],
            'actual_heights': [],
            'theoretical_heights': [],
            'min_degree': min_degree
        }
        
        for size in range(100, max_size + 1, 100):
            # Create B-Tree with random data
            btree = BTree(min_degree=min_degree)
            test_data = list(range(size))
            random.shuffle(test_data)
            
            for item in test_data:
                btree.insert(item)
            
            # Record statistics
            results['sizes'].append(size)
            results['actual_heights'].append(btree.height)
            results['theoretical_heights'].append(math.log((size + 1) / 2, min_degree))
        
        return results
    
    @staticmethod
    def benchmark_btree_variants():
        """Benchmark B-Trees with different minimum degrees."""
        print("B-Tree Performance Analysis")
        print("=" * 50)
        
        # Test data
        test_sizes = [100, 1000, 10000]
        min_degrees = [2, 3, 5, 10]
        
        for size in test_sizes:
            print(f"\nTest Size: {size}")
            print("-" * 30)
            
            for min_degree in min_degrees:
                # Create B-Tree
                btree = BTree[int](min_degree=min_degree)
                
                # Insert test data
                test_data = list(range(size))
                random.shuffle(test_data)
                
                start_time = timeit.default_timer()
                for item in test_data:
                    btree.insert(item)
                insert_time = timeit.default_timer() - start_time
                
                # Search test
                search_keys = random.sample(test_data, min(100, size))
                start_time = timeit.default_timer()
                for key in search_keys:
                    btree.search(key)
                search_time = timeit.default_timer() - start_time
                
                # Get statistics
                stats = BTreeAnalyzer.analyze_btree(btree)
                
                print(f"Min Degree {min_degree:2d}: "
                      f"Height={stats.height:2d}, "
                      f"Insert={insert_time:.4f}s, "
                      f"Search={search_time:.4f}s, "
                      f"Memory={stats.memory_usage:,} bytes")
    
    @staticmethod
    def compare_with_alternatives():
        """Compare B-Tree performance with alternative data structures."""
        print("\nB-Tree vs Alternatives Comparison")
        print("=" * 50)
        
        # Test data
        test_size = 1000
        test_data = list(range(test_size))
        random.shuffle(test_data)
        
        # B-Tree
        btree = BTree[int](min_degree=3)
        for item in test_data:
            btree.insert(item)
        
        # Built-in set
        set_data = set(test_data)
        
        # Built-in list (sorted)
        list_data = sorted(test_data)
        
        # Benchmark operations
        operations = ["search", "insert", "delete", "range_query"]
        
        print(f"{'Operation':<12} {'B-Tree':<12} {'Set':<12} {'List':<12}")
        print("-" * 50)
        
        for operation in operations:
            if operation == "search":
                btree_time = timeit.timeit("btree.search(500)", globals={'btree': btree}, number=1000)
                set_time = timeit.timeit("500 in set_data", globals={'set_data': set_data}, number=1000)
                list_time = timeit.timeit("500 in list_data", globals={'list_data': list_data}, number=1000)
            elif operation == "insert":
                btree_time = timeit.timeit("btree.insert(random.randint(1000, 2000))", globals={'btree': btree, 'random': random}, number=100)
                set_time = timeit.timeit("set_data.add(random.randint(1000, 2000))", globals={'set_data': set_data, 'random': random}, number=100)
                list_time = timeit.timeit("list_data.append(random.randint(1000, 2000)); list_data.sort()", globals={'list_data': list_data, 'random': random}, number=100)
            elif operation == "delete":
                btree_time = timeit.timeit("btree.delete(500)", globals={'btree': btree}, number=100)
                set_time = timeit.timeit("set_data.discard(500)", globals={'set_data': set_data}, number=100)
                list_time = timeit.timeit("list_data.remove(500) if 500 in list_data else None", globals={'list_data': list_data}, number=100)
            elif operation == "range_query":
                btree_time = timeit.timeit("btree.range_query(200, 800)", globals={'btree': btree}, number=100)
                set_time = timeit.timeit("[x for x in set_data if 200 <= x <= 800]", globals={'set_data': set_data}, number=100)
                list_time = timeit.timeit("[x for x in list_data if 200 <= x <= 800]", globals={'list_data': list_data}, number=100)
            else:
                continue
            
            print(f"{operation:<12} {btree_time:<12.6f} {set_time:<12.6f} {list_time:<12.6f}")

def b_tree_height_analysis(n: int, t: int) -> Dict[str, float]:
    """
    Analyze B-Tree height bounds.
    
    Args:
        n: Number of keys in the B-Tree
        t: Minimum degree of the B-Tree
        
    Returns:
        Dictionary containing height analysis
    """
    # Calculate theoretical bounds
    min_height = math.log((n + 1) / 2, t) if t > 1 else float('inf')
    max_height = math.log(n + 1, 2)  # Binary tree height
    
    # Maximum keys per node
    max_keys_per_node = 2 * t - 1
    
    # Minimum keys per node (except root)
    min_keys_per_node = t - 1
    
    # Maximum number of nodes at each level
    max_nodes_at_level = lambda h: (2 * t) ** h
    
    # Minimum number of nodes at each level
    min_nodes_at_level = lambda h: 2 * (t ** (h - 1)) if h > 0 else 1
    
    # Calculate actual height for given n and t
    actual_height = math.ceil(min_height) if min_height != float('inf') else 0
    
    # Storage efficiency (keys per node on average)
    storage_efficiency = n / (2 * t - 1) if t > 0 else 0
    
    return {
        'nodes': n,
        'min_degree': t,
        'min_height': min_height,
        'max_height': max_height,
        'actual_height': actual_height,
        'max_keys_per_node': max_keys_per_node,
        'min_keys_per_node': min_keys_per_node,
        'storage_efficiency': storage_efficiency,
        'max_nodes_at_height_1': max_nodes_at_level(1),
        'min_nodes_at_height_1': min_nodes_at_level(1),
        'height_ratio_vs_binary': min_height / max_height if max_height > 0 else 0
    } 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running analyzer demonstration...")
    print("=" * 50)

    # Create instance of BTreeStats
    try:
        instance = BTreeStats()
        print(f"✓ Created BTreeStats instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.insert(5)
        instance.insert(3)
        instance.insert(7)
        print(f"  After inserting elements: {instance}")
    except Exception as e:
        print(f"✗ Error creating BTreeStats instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
