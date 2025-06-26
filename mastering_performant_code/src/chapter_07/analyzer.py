"""
AVL Tree Performance Analyzer

This module provides comprehensive benchmarking tools to compare AVL trees
with other data structures and analyze their performance characteristics.
"""

import timeit
import random
from typing import List, Dict, Any
from .avl_tree import AVLTree

class AVLTreeAnalyzer:
    """
    Performance analyzer for AVL trees.
    
    This class provides comprehensive benchmarking tools to compare:
    - AVL tree vs regular BST performance
    - Insertion, deletion, and search operations
    - Memory usage and tree height analysis
    - Real-world performance characteristics
    """
    
    def __init__(self):
        self.results: Dict[str, List[float]] = {}
    
    def benchmark_insertion(self, data_sizes: List[int], num_trials: int = 5) -> Dict[str, List[float]]:
        """Benchmark insertion performance for different data sizes."""
        results = {
            'avl_tree': [],
            'bst': [],
            'list': [],
            'set': []
        }
        
        for size in data_sizes:
            print(f"Benchmarking insertion for size {size}...")
            
            # Generate test data
            data = list(range(size))
            random.shuffle(data)
            
            # AVL Tree insertion
            avl_times = []
            for _ in range(num_trials):
                avl_tree = AVLTree()
                start_time = timeit.default_timer()
                for value in data:
                    avl_tree.insert(value)
                end_time = timeit.default_timer()
                avl_times.append(end_time - start_time)
            results['avl_tree'].append(sum(avl_times) / len(avl_times))
            
            # Regular BST insertion (simplified for comparison)
            bst_times = []
            for _ in range(num_trials):
                bst_values = []
                start_time = timeit.default_timer()
                for value in data:
                    bst_values.append(value)
                    bst_values.sort()  # Simulate BST insertion
                end_time = timeit.default_timer()
                bst_times.append(end_time - start_time)
            results['bst'].append(sum(bst_times) / len(bst_times))
            
            # List insertion
            list_times = []
            for _ in range(num_trials):
                test_list = []
                start_time = timeit.default_timer()
                for value in data:
                    test_list.append(value)
                end_time = timeit.default_timer()
                list_times.append(end_time - start_time)
            results['list'].append(sum(list_times) / len(list_times))
            
            # Set insertion
            set_times = []
            for _ in range(num_trials):
                test_set = set()
                start_time = timeit.default_timer()
                for value in data:
                    test_set.add(value)
                end_time = timeit.default_timer()
                set_times.append(end_time - start_time)
            results['set'].append(sum(set_times) / len(set_times))
        
        return results
    
    def benchmark_search(self, data_sizes: List[int], num_trials: int = 5) -> Dict[str, List[float]]:
        """Benchmark search performance for different data sizes."""
        results = {
            'avl_tree': [],
            'set': [],
            'list': []
        }
        
        for size in data_sizes:
            print(f"Benchmarking search for size {size}...")
            
            # Prepare test data
            data = list(range(size))
            random.shuffle(data)
            
            # Build AVL tree
            avl_tree = AVLTree()
            for value in data:
                avl_tree.insert(value)
            
            # Build set
            test_set = set(data)
            
            # Build list
            test_list = data.copy()
            
            # Search queries (mix of existing and non-existing values)
            search_queries = data[:size//2] + [x + size for x in range(size//2)]
            random.shuffle(search_queries)
            
            # AVL Tree search
            avl_times = []
            for _ in range(num_trials):
                start_time = timeit.default_timer()
                for query in search_queries:
                    avl_tree.search(query)
                end_time = timeit.default_timer()
                avl_times.append(end_time - start_time)
            results['avl_tree'].append(sum(avl_times) / len(avl_times))
            
            # Set search
            set_times = []
            for _ in range(num_trials):
                start_time = timeit.default_timer()
                for query in search_queries:
                    query in test_set
                end_time = timeit.default_timer()
                set_times.append(end_time - start_time)
            results['set'].append(sum(set_times) / len(set_times))
            
            # List search
            list_times = []
            for _ in range(num_trials):
                start_time = timeit.default_timer()
                for query in search_queries:
                    query in test_list
                end_time = timeit.default_timer()
                list_times.append(end_time - start_time)
            results['list'].append(sum(list_times) / len(list_times))
        
        return results
    
    def analyze_tree_properties(self, data_sizes: List[int]) -> Dict[str, List[Any]]:
        """Analyze tree properties like height and balance."""
        results = {
            'size': [],
            'height': [],
            'is_balanced': [],
            'theoretical_max_height': []
        }
        
        for size in data_sizes:
            print(f"Analyzing tree properties for size {size}...")
            
            # Generate test data
            data = list(range(size))
            random.shuffle(data)
            
            # Build AVL tree
            avl_tree = AVLTree()
            for value in data:
                avl_tree.insert(value)
            
            results['size'].append(size)
            results['height'].append(avl_tree.height())
            results['is_balanced'].append(avl_tree.is_balanced())
            results['theoretical_max_height'].append(int(1.44 * (size + 2).bit_length() - 0.328))
        
        return results
    
    def print_benchmark_results(self, results: Dict[str, List[float]], title: str):
        """Print benchmark results in a formatted table."""
        print(f"\n{title}")
        print("=" * 60)
        print(f"{'Size':<8} {'AVL Tree':<12} {'BST':<12} {'List':<12} {'Set':<12}")
        print("-" * 60)
        
        sizes = [100, 1000, 10000, 100000]
        for i, size in enumerate(sizes):
            avl_time = results['avl_tree'][i] if i < len(results['avl_tree']) else 0
            bst_time = results['bst'][i] if i < len(results['bst']) else 0
            list_time = results['list'][i] if i < len(results['list']) else 0
            set_time = results['set'][i] if i < len(results['set']) else 0
            
            print(f"{size:<8} {avl_time:<12.6f} {bst_time:<12.6f} {list_time:<12.6f} {set_time:<12.6f}")
    
    def print_tree_analysis(self, results: Dict[str, List[Any]]):
        """Print tree analysis results."""
        print("\nAVL Tree Properties Analysis")
        print("=" * 50)
        print(f"{'Size':<8} {'Height':<8} {'Balanced':<10} {'Max Height':<12}")
        print("-" * 50)
        
        for i in range(len(results['size'])):
            size = results['size'][i]
            height = results['height'][i]
            balanced = results['is_balanced'][i]
            max_height = results['theoretical_max_height'][i]
            
            print(f"{size:<8} {height:<8} {str(balanced):<10} {max_height:<12}")
    
    def benchmark_rotation_scenarios(self, num_trials: int = 10) -> Dict[str, float]:
        """Benchmark specific rotation scenarios."""
        results = {}
        
        # Left-Left rotation scenario
        print("Benchmarking Left-Left rotation scenario...")
        ll_times = []
        for _ in range(num_trials):
            avl_tree = AVLTree()
            # Insert in order that triggers LL rotation
            values = [30, 20, 10]  # This will trigger LL rotation
            start_time = timeit.default_timer()
            for value in values:
                avl_tree.insert(value)
            end_time = timeit.default_timer()
            ll_times.append(end_time - start_time)
        results['left_left'] = sum(ll_times) / len(ll_times)
        
        # Right-Right rotation scenario
        print("Benchmarking Right-Right rotation scenario...")
        rr_times = []
        for _ in range(num_trials):
            avl_tree = AVLTree()
            # Insert in order that triggers RR rotation
            values = [10, 20, 30]  # This will trigger RR rotation
            start_time = timeit.default_timer()
            for value in values:
                avl_tree.insert(value)
            end_time = timeit.default_timer()
            rr_times.append(end_time - start_time)
        results['right_right'] = sum(rr_times) / len(rr_times)
        
        # Left-Right rotation scenario
        print("Benchmarking Left-Right rotation scenario...")
        lr_times = []
        for _ in range(num_trials):
            avl_tree = AVLTree()
            # Insert in order that triggers LR rotation
            values = [30, 10, 20]  # This will trigger LR rotation
            start_time = timeit.default_timer()
            for value in values:
                avl_tree.insert(value)
            end_time = timeit.default_timer()
            lr_times.append(end_time - start_time)
        results['left_right'] = sum(lr_times) / len(lr_times)
        
        # Right-Left rotation scenario
        print("Benchmarking Right-Left rotation scenario...")
        rl_times = []
        for _ in range(num_trials):
            avl_tree = AVLTree()
            # Insert in order that triggers RL rotation
            values = [10, 30, 20]  # This will trigger RL rotation
            start_time = timeit.default_timer()
            for value in values:
                avl_tree.insert(value)
            end_time = timeit.default_timer()
            rl_times.append(end_time - start_time)
        results['right_left'] = sum(rl_times) / len(rl_times)
        
        return results
    
    def print_rotation_benchmarks(self, results: Dict[str, float]):
        """Print rotation benchmark results."""
        print("\nRotation Performance Analysis")
        print("=" * 40)
        print(f"{'Rotation Type':<15} {'Time (seconds)':<15}")
        print("-" * 40)
        
        for rotation_type, time_taken in results.items():
            print(f"{rotation_type:<15} {time_taken:<15.6f}")
    
    def analyze_memory_usage(self, tree: AVLTree) -> Dict[str, int]:
        """Analyze memory usage of AVL tree vs alternatives."""
        def calculate_total_memory(node):
            """Recursively calculate total memory usage of tree nodes."""
            if node is None:
                return 0
            node_size = sys.getsizeof(node)
            left_size = calculate_total_memory(node.left)
            right_size = calculate_total_memory(node.right)
            return node_size + left_size + right_size
        
        tree_size = sys.getsizeof(tree)
        node_size = sys.getsizeof(tree._root) if tree._root else 0
        total_memory = calculate_total_memory(tree._root)
        
        return {
            'tree_size': tree_size,
            'node_size': node_size,
            'total_memory': total_memory,
            'nodes_count': len(tree)
        }
    
    def benchmark_memory_usage(self, data_sizes: List[int]) -> Dict[str, List[int]]:
        """Benchmark memory usage for different data structures."""
        results = {
            'avl_tree': [],
            'set': [],
            'list': [],
            'dict': []
        }
        
        for size in data_sizes:
            print(f"Benchmarking memory usage for size {size}...")
            
            # Generate test data
            data = list(range(size))
            random.shuffle(data)
            
            # AVL Tree memory usage
            avl_tree = AVLTree()
            for value in data:
                avl_tree.insert(value)
            avl_memory = self.analyze_memory_usage(avl_tree)['total_memory']
            results['avl_tree'].append(avl_memory)
            
            # Set memory usage
            test_set = set(data)
            set_memory = sys.getsizeof(test_set)
            results['set'].append(set_memory)
            
            # List memory usage
            test_list = data.copy()
            list_memory = sys.getsizeof(test_list)
            results['list'].append(list_memory)
            
            # Dict memory usage (simulating key-value storage)
            test_dict = {i: i for i in data}
            dict_memory = sys.getsizeof(test_dict)
            results['dict'].append(dict_memory)
        
        return results
    
    def print_memory_analysis(self, results: Dict[str, List[int]]):
        """Print memory analysis results."""
        print("\nMemory Usage Analysis (bytes)")
        print("=" * 60)
        print(f"{'Size':<8} {'AVL Tree':<12} {'Set':<12} {'List':<12} {'Dict':<12}")
        print("-" * 60)
        
        sizes = [100, 1000, 10000, 100000]
        for i, size in enumerate(sizes):
            avl_memory = results['avl_tree'][i] if i < len(results['avl_tree']) else 0
            set_memory = results['set'][i] if i < len(results['set']) else 0
            list_memory = results['list'][i] if i < len(results['list']) else 0
            dict_memory = results['dict'][i] if i < len(results['dict']) else 0
            
            print(f"{size:<8} {avl_memory:<12} {set_memory:<12} {list_memory:<12} {dict_memory:<12}")
    
    def fibonacci_avl_height_analysis(self, n: int) -> Dict[str, float]:
        """Analyze AVL height bounds using Fibonacci relationship."""
        def fibonacci(n: int) -> int:
            """Calculate the nth Fibonacci number."""
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b
        
        # Find minimum height for n nodes
        h = 0
        while fibonacci(h + 3) - 1 <= n:
            h += 1
        h -= 1  # Adjust for the last increment
        
        # Calculate theoretical bounds
        min_nodes = fibonacci(h + 3) - 1
        max_nodes = 2**(h + 1) - 1  # Perfect binary tree
        
        # AVL height bound
        avl_height_bound = int(1.44 * (n + 2).bit_length() - 0.328)
        
        return {
            'nodes': n,
            'min_height': h,
            'avl_height_bound': avl_height_bound,
            'min_nodes_for_height': min_nodes,
            'max_nodes_for_height': max_nodes,
            'height_efficiency': h / avl_height_bound if avl_height_bound > 0 else 0
        } 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running analyzer demonstration...")
    print("=" * 50)

    # Create instance of AVLTreeAnalyzer
    try:
        instance = AVLTreeAnalyzer()
        print(f"✓ Created AVLTreeAnalyzer instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.insert(5)
        instance.insert(3)
        instance.insert(7)
        print(f"  After inserting elements: {instance}")
    except Exception as e:
        print(f"✗ Error creating AVLTreeAnalyzer instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
