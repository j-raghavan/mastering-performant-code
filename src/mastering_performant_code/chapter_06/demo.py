"""
Demo script for Chapter 6: Binary Search Tree implementations.

This script demonstrates the functionality of both recursive and iterative
BST implementations with performance comparisons and real-world examples.
"""

import timeit
from typing import List, Dict, Any

from .recursive_bst import RecursiveBST
from .iterative_bst import IterativeBST
from .analyzer import BSTAnalyzer, TreeInfo
from .file_system_tree import FileSystemTree

def benchmark_comparison():
    """Compare performance of recursive vs iterative BST implementations."""
    print("=== BST Performance Comparison ===\n")
    
    # Test with different data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"Performance with {size} elements:")
        print("-" * 40)
        
        # Insert operations
        recursive_insert = timeit.timeit(
            f"bst.insert(i) for i in range({size})",
            setup="from code.chapter_06 import RecursiveBST; bst = RecursiveBST()",
            number=1
        )
        
        iterative_insert = timeit.timeit(
            f"bst.insert(i) for i in range({size})",
            setup="from code.chapter_06 import IterativeBST; bst = IterativeBST()",
            number=1
        )
        
        print(f"Insert {size} items:")
        print(f"  Recursive: {recursive_insert:.6f} seconds")
        print(f"  Iterative: {iterative_insert:.6f} seconds")
        print(f"  Ratio: {recursive_insert/iterative_insert:.2f}x")
        
        # Search operations
        recursive_search = timeit.timeit(
            f"bst.search(i) for i in range({size})",
            setup=f"from code.chapter_06 import RecursiveBST; bst = RecursiveBST(); [bst.insert(i) for i in range({size})]",
            number=1
        )
        
        iterative_search = timeit.timeit(
            f"bst.search(i) for i in range({size})",
            setup=f"from code.chapter_06 import IterativeBST; bst = IterativeBST(); [bst.insert(i) for i in range({size})]",
            number=1
        )
        
        print(f"Search {size} items:")
        print(f"  Recursive: {recursive_search:.6f} seconds")
        print(f"  Iterative: {iterative_search:.6f} seconds")
        print(f"  Ratio: {recursive_search/iterative_search:.2f}x")
        
        # Traversal operations
        recursive_traversal = timeit.timeit(
            "list(bst.inorder_traversal())",
            setup=f"from code.chapter_06 import RecursiveBST; bst = RecursiveBST(); [bst.insert(i) for i in range({size})]",
            number=10
        )
        
        iterative_traversal = timeit.timeit(
            "list(bst.inorder_traversal())",
            setup=f"from code.chapter_06 import IterativeBST; bst = IterativeBST(); [bst.insert(i) for i in range({size})]",
            number=10
        )
        
        print(f"Traversal {size} items:")
        print(f"  Recursive: {recursive_traversal:.6f} seconds")
        print(f"  Iterative: {iterative_traversal:.6f} seconds")
        print(f"  Ratio: {recursive_traversal/iterative_traversal:.2f}x")
        
        print()

def memory_usage_comparison():
    """Compare memory usage of BST implementations."""
    print("=== BST Memory Usage Comparison ===\n")
    
    # Test with different data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"Memory usage with {size} elements:")
        print("-" * 40)
        
        # Recursive BST
        recursive_bst = RecursiveBST()
        for i in range(size):
            recursive_bst.insert(i)
        
        recursive_memory = sys.getsizeof(recursive_bst)
        
        # Iterative BST
        iterative_bst = IterativeBST()
        for i in range(size):
            iterative_bst.insert(i)
        
        iterative_memory = sys.getsizeof(iterative_bst)
        
        print(f"Recursive BST: {recursive_memory} bytes")
        print(f"Iterative BST: {iterative_memory} bytes")
        print(f"Ratio: {recursive_memory/iterative_memory:.2f}x")
        print()

def tree_analysis_demo():
    """Demonstrate tree analysis capabilities."""
    print("=== Tree Analysis Demo ===\n")
    
    # Create a sample tree
    bst = RecursiveBST()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    
    for value in values:
        bst.insert(value)
    
    # Analyze the tree
    analyzer = BSTAnalyzer()
    tree_info = analyzer.analyze_tree(bst._root)
    
    print(f"Tree Analysis:")
    print(f"  Height: {tree_info.height}")
    print(f"  Size: {tree_info.size}")
    print(f"  Is Balanced: {tree_info.is_balanced}")
    print(f"  Memory Usage: {tree_info.memory_usage} bytes")
    print(f"  Average Depth: {tree_info.average_depth:.2f}")
    print(f"  Leaf Count: {tree_info.leaf_count}")
    print(f"  Internal Node Count: {tree_info.internal_node_count}")
    print(f"  Min Value: {tree_info.min_value}")
    print(f"  Max Value: {tree_info.max_value}")
    
    print(f"\nTraversal Results:")
    print(f"  Inorder: {list(bst.inorder_traversal())}")
    print(f"  Preorder: {list(bst.preorder_traversal())}")
    print(f"  Postorder: {list(bst.postorder_traversal())}")
    print(f"  Level-order: {list(bst.level_order_traversal())}")
    
    print(f"\nMin/Max Values:")
    print(f"  Minimum: {bst.find_minimum()}")
    print(f"  Maximum: {bst.find_maximum()}")
    
    print(f"\nSuccessor/Predecessor:")
    print(f"  Successor of 30: {bst.get_successor(30)}")
    print(f"  Predecessor of 70: {bst.get_predecessor(70)}")
    
    print(f"\nRange Search (25-65): {bst.range_search(25, 65)}")

def traversal_comparison_demo():
    """Demonstrate different traversal methods."""
    print("=== Traversal Comparison Demo ===\n")
    
    # Create a tree
    bst = RecursiveBST()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    
    for value in values:
        bst.insert(value)
    
    print("Tree Structure:")
    print("       50")
    print("      /  \\")
    print("     30   70")
    print("    /  \\ /  \\")
    print("   20  40 60  80")
    print("  /  \\/  \\/  \\/  \\")
    print(" 10  25 35 45 55 65 75 85")
    print()
    
    print("Traversal Results:")
    print(f"Inorder (Left → Root → Right): {list(bst.inorder_traversal())}")
    print(f"Preorder (Root → Left → Right): {list(bst.preorder_traversal())}")
    print(f"Postorder (Left → Right → Root): {list(bst.postorder_traversal())}")
    print(f"Level-order (Breadth-first): {list(bst.level_order_traversal())}")

def deletion_demo():
    """Demonstrate BST deletion operations."""
    print("=== BST Deletion Demo ===\n")
    
    # Create a tree
    bst = RecursiveBST()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    
    for value in values:
        bst.insert(value)
    
    print(f"Original tree (inorder): {list(bst.inorder_traversal())}")
    print(f"Size: {len(bst)}")
    
    # Delete a leaf node
    print(f"\nDeleting leaf node 10:")
    bst.delete(10)
    print(f"After deletion: {list(bst.inorder_traversal())}")
    print(f"Size: {len(bst)}")
    
    # Delete a node with one child
    print(f"\nDeleting node with one child 20:")
    bst.delete(20)
    print(f"After deletion: {list(bst.inorder_traversal())}")
    print(f"Size: {len(bst)}")
    
    # Delete a node with two children
    print(f"\nDeleting node with two children 30:")
    bst.delete(30)
    print(f"After deletion: {list(bst.inorder_traversal())}")
    print(f"Size: {len(bst)}")
    
    # Delete root
    print(f"\nDeleting root node 50:")
    bst.delete(50)
    print(f"After deletion: {list(bst.inorder_traversal())}")
    print(f"Size: {len(bst)}")

def range_search_demo():
    """Demonstrate range search functionality."""
    print("=== Range Search Demo ===\n")
    
    # Create a tree
    bst = RecursiveBST()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    
    for value in values:
        bst.insert(value)
    
    print(f"All values: {list(bst.inorder_traversal())}")
    
    ranges = [
        (10, 30),
        (25, 60),
        (40, 80),
        (0, 100),
        (15, 25)
    ]
    
    for min_val, max_val in ranges:
        result = bst.range_search(min_val, max_val)
        print(f"Range [{min_val}, {max_val}]: {result}")

def tree_structure_analysis_demo():
    """Demonstrate tree structure analysis."""
    print("=== Tree Structure Analysis Demo ===\n")
    
    # Create different tree structures
    trees = {
        "Balanced": [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85],
        "Linear (Right)": [10, 20, 30, 40, 50, 60, 70, 80, 90],
        "Linear (Left)": [90, 80, 70, 60, 50, 40, 30, 20, 10],
        "Unbalanced": [50, 40, 30, 20, 10, 60, 70, 80, 90]
    }
    
    analyzer = BSTAnalyzer()
    
    for name, values in trees.items():
        print(f"{name} Tree:")
        print("-" * 30)
        
        bst = RecursiveBST()
        for value in values:
            bst.insert(value)
        
        tree_info = analyzer.analyze_tree(bst._root)
        structure_info = analyzer.analyze_tree_structure(bst._root)
        
        print(f"  Height: {tree_info.height}")
        print(f"  Size: {tree_info.size}")
        print(f"  Is Balanced: {tree_info.is_balanced}")
        print(f"  Structure Type: {structure_info['structure']}")
        print(f"  Balance Factor: {structure_info['balance_factor']}")
        print(f"  Efficiency Ratio: {structure_info['efficiency_ratio']:.2f}")
        print()

def memory_efficiency_demo():
    """Demonstrate memory efficiency analysis."""
    print("=== Memory Efficiency Analysis Demo ===\n")
    
    # Create trees of different sizes
    sizes = [100, 1000, 10000]
    
    analyzer = BSTAnalyzer()
    
    for size in sizes:
        print(f"Tree with {size} elements:")
        print("-" * 30)
        
        bst = RecursiveBST()
        for i in range(size):
            bst.insert(i)
        
        memory_info = analyzer.memory_efficiency_analysis(bst._root)
        
        print(f"  Total Memory: {memory_info['total_memory']} bytes")
        print(f"  Node Memory: {memory_info['node_memory']} bytes")
        print(f"  Value Memory: {memory_info['value_memory']} bytes")
        print(f"  Overhead Memory: {memory_info['overhead_memory']} bytes")
        print(f"  Memory per Node: {memory_info['memory_per_node']:.1f} bytes")
        print(f"  Efficiency Score: {memory_info['efficiency_score']:.3f}")
        print()

def file_system_demo():
    """Demonstrate file system tree application."""
    print("=== File System Tree Demo ===\n")
    
    # Create a simple file system tree (using current directory)
    try:
        fs_tree = FileSystemTree(".")
        
        print("File System Statistics:")
        stats = fs_tree.get_statistics()
        print(f"  Total Size: {fs_tree._format_size(stats['total_size'])}")
        print(f"  File Count: {stats['file_count']}")
        print(f"  Directory Count: {stats['directory_count']}")
        print(f"  Total Items: {stats['total_items']}")
        print(f"  Average File Size: {fs_tree._format_size(stats['average_file_size'])}")
        
        if stats['largest_file']:
            print(f"  Largest File: {stats['largest_file'].name} ({fs_tree._format_size(stats['largest_file'].size)})")
        
        print(f"\nLargest Files:")
        largest_files = fs_tree.get_largest_files(5)
        for i, file_node in enumerate(largest_files, 1):
            print(f"  {i}. {file_node.name} ({fs_tree._format_size(file_node.size)})")
        
        print(f"\nPython Files:")
        python_files = fs_tree.list_files_by_extension(".py")
        for file_node in python_files[:5]:  # Show first 5
            print(f"  {file_node.name} ({fs_tree._format_size(file_node.size)})")
        
        if len(python_files) > 5:
            print(f"  ... and {len(python_files) - 5} more")
        
    except Exception as e:
        print(f"Error creating file system tree: {e}")
        print("This demo requires access to the file system.")

def performance_analysis_demo():
    """Demonstrate comprehensive performance analysis."""
    print("=== Performance Analysis Demo ===\n")
    
    # Test different tree shapes
    test_cases = {
        "Balanced": list(range(100)),
        "Unbalanced (Right)": list(range(100)),  # Will create a right-heavy tree
        "Random": [50, 25, 75, 12, 37, 62, 87, 6, 18, 31, 43, 56, 68, 81, 93]
    }
    
    operations = ["insert", "search", "delete", "traversal"]
    
    for tree_type, values in test_cases.items():
        print(f"{tree_type} Tree Performance:")
        print("-" * 40)
        
        # Test recursive implementation
        recursive_bst = RecursiveBST()
        recursive_times = {}
        
        for operation in operations:
            if operation == "insert":
                start_time = timeit.default_timer()
                for value in values:
                    recursive_bst.insert(value)
                end_time = timeit.default_timer()
                recursive_times[operation] = end_time - start_time
            elif operation == "search":
                start_time = timeit.default_timer()
                for value in values[:10]:  # Search first 10 values
                    recursive_bst.search(value)
                end_time = timeit.default_timer()
                recursive_times[operation] = end_time - start_time
            elif operation == "delete":
                start_time = timeit.default_timer()
                for value in values[:10]:  # Delete first 10 values
                    recursive_bst.delete(value)
                end_time = timeit.default_timer()
                recursive_times[operation] = end_time - start_time
            elif operation == "traversal":
                start_time = timeit.default_timer()
                list(recursive_bst.inorder_traversal())
                end_time = timeit.default_timer()
                recursive_times[operation] = end_time - start_time
        
        # Test iterative implementation
        iterative_bst = IterativeBST()
        iterative_times = {}
        
        for operation in operations:
            if operation == "insert":
                start_time = timeit.default_timer()
                for value in values:
                    iterative_bst.insert(value)
                end_time = timeit.default_timer()
                iterative_times[operation] = end_time - start_time
            elif operation == "search":
                start_time = timeit.default_timer()
                for value in values[:10]:  # Search first 10 values
                    iterative_bst.search(value)
                end_time = timeit.default_timer()
                iterative_times[operation] = end_time - start_time
            elif operation == "delete":
                start_time = timeit.default_timer()
                for value in values[:10]:  # Delete first 10 values
                    iterative_bst.delete(value)
                end_time = timeit.default_timer()
                iterative_times[operation] = end_time - start_time
            elif operation == "traversal":
                start_time = timeit.default_timer()
                list(iterative_bst.inorder_traversal())
                end_time = timeit.default_timer()
                iterative_times[operation] = end_time - start_time
        
        # Print results
        for operation in operations:
            recursive_time = recursive_times[operation]
            iterative_time = iterative_times[operation]
            ratio = recursive_time / iterative_time if iterative_time > 0 else float('inf')
            
            print(f"  {operation.capitalize()}:")
            print(f"    Recursive: {recursive_time:.6f}s")
            print(f"    Iterative: {iterative_time:.6f}s")
            print(f"    Ratio: {ratio:.2f}x")
        
        print()

def main():
    """Run all demos."""
    print("Chapter 6: Binary Search Tree - Recursive & Iterative Approaches")
    print("=" * 70)
    print()
    
    # Run all demos
    tree_analysis_demo()
    print()
    
    traversal_comparison_demo()
    print()
    
    deletion_demo()
    print()
    
    range_search_demo()
    print()
    
    tree_structure_analysis_demo()
    print()
    
    memory_efficiency_demo()
    print()
    
    performance_analysis_demo()
    print()
    
    file_system_demo()
    print()
    
    benchmark_comparison()
    print()
    
    memory_usage_comparison()
    print()
    
    print("Demo completed successfully!")

if __name__ == "__main__":
    main() 