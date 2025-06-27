"""
BST Analyzer implementation for Chapter 6.

This module provides tools to analyze the performance and memory
characteristics of BST implementations.
"""

import timeit
import sys
from typing import TypeVar, Generic, Optional, Iterator, List, Dict, Any
from dataclasses import dataclass
from collections import deque

from .bst_node import BSTNode

T = TypeVar('T')

@dataclass
class TreeInfo:
    """Information about a binary search tree."""
    height: int
    size: int
    is_balanced: bool
    memory_usage: int
    average_depth: float
    leaf_count: int
    internal_node_count: int
    min_value: Optional[Any]
    max_value: Optional[Any]

class BSTAnalyzer:
    """
    Analyzer for Binary Search Tree implementations.
    
    This class provides tools to analyze the performance and memory
    characteristics of BST implementations.
    """
    
    @staticmethod
    def analyze_tree(root: Optional[BSTNode[T]]) -> TreeInfo:
        """Analyze a binary search tree."""
        if root is None:
            return TreeInfo(0, 0, True, 0, 0.0, 0, 0, None, None)
        
        height = BSTAnalyzer._calculate_height(root)
        size = BSTAnalyzer._calculate_size(root)
        is_balanced = BSTAnalyzer._is_balanced(root)
        memory_usage = BSTAnalyzer._calculate_memory_usage(root)
        avg_depth = BSTAnalyzer._calculate_average_depth(root)
        leaf_count = BSTAnalyzer._calculate_leaf_count(root)
        internal_node_count = size - leaf_count
        min_value = BSTAnalyzer._find_minimum_value(root)
        max_value = BSTAnalyzer._find_maximum_value(root)
        
        return TreeInfo(
            height=height,
            size=size,
            is_balanced=is_balanced,
            memory_usage=memory_usage,
            average_depth=avg_depth,
            leaf_count=leaf_count,
            internal_node_count=internal_node_count,
            min_value=min_value,
            max_value=max_value
        )
    
    @staticmethod
    def _calculate_height(node: Optional[BSTNode[T]]) -> int:
        """Calculate the height of a subtree."""
        if node is None:
            return -1
        return 1 + max(
            BSTAnalyzer._calculate_height(node.left),
            BSTAnalyzer._calculate_height(node.right)
        )
    
    @staticmethod
    def _calculate_size(node: Optional[BSTNode[T]]) -> int:
        """Calculate the size of a subtree."""
        if node is None:
            return 0
        return 1 + BSTAnalyzer._calculate_size(node.left) + BSTAnalyzer._calculate_size(node.right)
    
    @staticmethod
    def _is_balanced(node: Optional[BSTNode[T]]) -> bool:
        """Check if a tree is balanced (height difference <= 1 for all nodes)."""
        def check_balance(node: Optional[BSTNode[T]]) -> tuple[bool, int]:
            if node is None:
                return True, -1
            
            left_balanced, left_height = check_balance(node.left)
            right_balanced, right_height = check_balance(node.right)
            
            if not left_balanced or not right_balanced:
                return False, 0
            
            if abs(left_height - right_height) > 1:
                return False, 0
            
            return True, 1 + max(left_height, right_height)
        
        return check_balance(node)[0]
    
    @staticmethod
    def _calculate_memory_usage(node: Optional[BSTNode[T]]) -> int:
        """Calculate memory usage of a subtree."""
        if node is None:
            return 0
        
        node_size = sys.getsizeof(node) + sys.getsizeof(node.value)
        return node_size + BSTAnalyzer._calculate_memory_usage(node.left) + BSTAnalyzer._calculate_memory_usage(node.right)
    
    @staticmethod
    def _calculate_average_depth(node: Optional[BSTNode[T]]) -> float:
        """Calculate the average depth of nodes in a tree."""
        if node is None:
            return 0.0
        
        total_depth = 0
        node_count = 0
        
        def traverse_with_depth(node: Optional[BSTNode[T]], depth: int) -> None:
            nonlocal total_depth, node_count
            if node is None:
                return
            
            total_depth += depth
            node_count += 1
            
            traverse_with_depth(node.left, depth + 1)
            traverse_with_depth(node.right, depth + 1)
        
        traverse_with_depth(node, 0)
        return total_depth / node_count if node_count > 0 else 0.0
    
    @staticmethod
    def _calculate_leaf_count(node: Optional[BSTNode[T]]) -> int:
        """Calculate the number of leaf nodes in a tree."""
        if node is None:
            return 0
        
        if node.is_leaf():
            return 1
        
        return BSTAnalyzer._calculate_leaf_count(node.left) + BSTAnalyzer._calculate_leaf_count(node.right)
    
    @staticmethod
    def _find_minimum_value(node: Optional[BSTNode[T]]) -> Optional[T]:
        """Find the minimum value in a tree."""
        if node is None:
            return None
        
        current = node
        while current.left:
            current = current.left
        return current.value
    
    @staticmethod
    def _find_maximum_value(node: Optional[BSTNode[T]]) -> Optional[T]:
        """Find the maximum value in a tree."""
        if node is None:
            return None
        
        current = node
        while current.right:
            current = current.right
        return current.value
    
    @staticmethod
    def benchmark_operations(bst_class, operations: List[str], data_sizes: List[int]) -> Dict[str, Dict[int, float]]:
        """Benchmark common operations on BST implementations."""
        results = {}
        
        for operation in operations:
            results[operation] = {}
            
            for size in data_sizes:
                if operation == "insert":
                    setup = f"from mastering_performant_code.chapter_06 import {bst_class.__name__}; bst = {bst_class.__name__}()"
                    stmt = f"[bst.insert(i) for i in range({size})]"
                elif operation == "search":
                    setup = f"from mastering_performant_code.chapter_06 import {bst_class.__name__}; bst = {bst_class.__name__}(); [bst.insert(i) for i in range({size})]"
                    stmt = f"[bst.search(i) for i in range({size})]"
                elif operation == "delete":
                    setup = f"from mastering_performant_code.chapter_06 import {bst_class.__name__}; bst = {bst_class.__name__}(); [bst.insert(i) for i in range({size})]"
                    stmt = f"[bst.delete(i) for i in range({size})]"
                elif operation == "traversal":
                    setup = f"from mastering_performant_code.chapter_06 import {bst_class.__name__}; bst = {bst_class.__name__}(); [bst.insert(i) for i in range({size})]"
                    stmt = "list(bst.inorder_traversal())"
                elif operation == "range_search":
                    setup = f"from mastering_performant_code.chapter_06 import {bst_class.__name__}; bst = {bst_class.__name__}(); [bst.insert(i) for i in range({size})]"
                    stmt = f"bst.range_search({size//4}, {3*size//4})"
                else:
                    continue
                
                time = timeit.timeit(stmt, setup=setup, number=1)
                results[operation][size] = time
        
        return results
    
    @staticmethod
    def compare_implementations(recursive_bst_class, iterative_bst_class, data_sizes: List[int]) -> Dict[str, Dict[str, float]]:
        """Compare performance between recursive and iterative BST implementations."""
        operations = ["insert", "search", "delete", "traversal", "range_search"]
        results = {}
        
        for operation in operations:
            results[operation] = {}
            
            for size in data_sizes:
                # Benchmark recursive implementation
                recursive_setup = f"from mastering_performant_code.chapter_06 import {recursive_bst_class.__name__}; bst = {recursive_bst_class.__name__}()"
                if operation in ["search", "delete", "traversal", "range_search"]:
                    recursive_setup += f"; [bst.insert(i) for i in range({size})]"
                
                recursive_stmt = BSTAnalyzer._get_operation_stmt(operation, size)
                recursive_time = timeit.timeit(recursive_stmt, setup=recursive_setup, number=1)
                
                # Benchmark iterative implementation
                iterative_setup = f"from mastering_performant_code.chapter_06 import {iterative_bst_class.__name__}; bst = {iterative_bst_class.__name__}()"
                if operation in ["search", "delete", "traversal", "range_search"]:
                    iterative_setup += f"; [bst.insert(i) for i in range({size})]"
                
                iterative_stmt = BSTAnalyzer._get_operation_stmt(operation, size)
                iterative_time = timeit.timeit(iterative_stmt, setup=iterative_setup, number=1)
                
                results[operation][size] = {
                    "recursive": recursive_time,
                    "iterative": iterative_time,
                    "ratio": recursive_time / iterative_time if iterative_time > 0 else float('inf')
                }
        
        return results
    
    @staticmethod
    def _get_operation_stmt(operation: str, size: int) -> str:
        """Get the statement for a given operation."""
        if operation == "insert":
            return f"[bst.insert(i) for i in range({size})]"
        elif operation == "search":
            return f"[bst.search(i) for i in range({size})]"
        elif operation == "delete":
            return f"[bst.delete(i) for i in range({size})]"
        elif operation == "traversal":
            return "list(bst.inorder_traversal())"
        elif operation == "range_search":
            return f"bst.range_search({size//4}, {3*size//4})"
        else:
            return ""
    
    @staticmethod
    def analyze_tree_structure(root: Optional[BSTNode[T]]) -> Dict[str, Any]:
        """Analyze the structure of a binary search tree."""
        if root is None:
            return {
                "type": "empty",
                "height": 0,
                "size": 0,
                "balance_factor": 0,
                "structure": "empty"
            }
        
        height = BSTAnalyzer._calculate_height(root)
        size = BSTAnalyzer._calculate_size(root)
        is_balanced = BSTAnalyzer._is_balanced(root)
        
        # Determine tree structure type
        if size == 1:
            structure = "single_node"
        elif height == size - 1:
            structure = "linear"  # Degenerate tree
        elif is_balanced and height <= 2 * (size ** 0.5):
            structure = "balanced"
        else:
            structure = "unbalanced"
        
        # Calculate balance factor
        left_height = BSTAnalyzer._calculate_height(root.left)
        right_height = BSTAnalyzer._calculate_height(root.right)
        balance_factor = right_height - left_height
        
        return {
            "type": "binary_search_tree",
            "height": height,
            "size": size,
            "balance_factor": balance_factor,
            "is_balanced": is_balanced,
            "structure": structure,
            "theoretical_min_height": int(size ** 0.5) if size > 0 else 0,
            "efficiency_ratio": height / (size ** 0.5) if size > 0 else 0
        }
    
    @staticmethod
    def get_tree_visualization(root: Optional[BSTNode[T]], max_depth: int = 5) -> str:
        """Generate a text-based visualization of the tree."""
        if root is None:
            return "Empty tree"
        
        def get_level_nodes(node: Optional[BSTNode[T]], level: int, max_level: int) -> List[Optional[BSTNode[T]]]:
            if level > max_level or node is None:
                return []
            
            if level == max_level:
                return [node]
            
            left_nodes = get_level_nodes(node.left, level + 1, max_level)
            right_nodes = get_level_nodes(node.right, level + 1, max_level)
            
            return left_nodes + right_nodes
        
        lines = []
        for level in range(min(max_depth, BSTAnalyzer._calculate_height(root) + 1)):
            nodes = get_level_nodes(root, 0, level)
            if not nodes:
                break
            
            # Create level line
            level_str = "  " * (2 ** (max_depth - level) - 1)
            node_strs = []
            
            for node in nodes:
                if node is None:
                    node_strs.append("  ")
                else:
                    node_strs.append(f"{node.value:2d}")
            
            level_str += " ".join(node_strs)
            lines.append(level_str)
        
        return "\n".join(lines)
    
    @staticmethod
    def memory_efficiency_analysis(root: Optional[BSTNode[T]]) -> Dict[str, Any]:
        """Analyze memory efficiency of a BST."""
        if root is None:
            return {
                "total_memory": 0,
                "node_memory": 0,
                "value_memory": 0,
                "overhead_memory": 0,
                "memory_per_node": 0,
                "efficiency_score": 0.0
            }
        
        total_memory = BSTAnalyzer._calculate_memory_usage(root)
        size = BSTAnalyzer._calculate_size(root)
        
        # Calculate memory breakdown
        node_memory = size * sys.getsizeof(BSTNode(0))  # Approximate node memory
        value_memory = BSTAnalyzer._calculate_value_memory(root)
        overhead_memory = total_memory - node_memory - value_memory
        
        memory_per_node = total_memory / size if size > 0 else 0
        
        # Calculate efficiency score (lower is better)
        theoretical_min_memory = size * (sys.getsizeof(0) + 24)  # Minimal possible memory
        efficiency_score = theoretical_min_memory / total_memory if total_memory > 0 else 0
        
        return {
            "total_memory": total_memory,
            "node_memory": node_memory,
            "value_memory": value_memory,
            "overhead_memory": overhead_memory,
            "memory_per_node": memory_per_node,
            "efficiency_score": efficiency_score,
            "theoretical_min_memory": theoretical_min_memory
        }
    
    @staticmethod
    def _calculate_value_memory(node: Optional[BSTNode[T]]) -> int:
        """Calculate memory used by values in a tree."""
        if node is None:
            return 0
        
        value_memory = sys.getsizeof(node.value)
        return value_memory + BSTAnalyzer._calculate_value_memory(node.left) + BSTAnalyzer._calculate_value_memory(node.right) 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running analyzer demonstration...")
    print("=" * 50)

    # Create instance of BSTAnalyzer
    try:
        instance = BSTAnalyzer()
        print(f"✓ Created BSTAnalyzer instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic operations
        print("Testing basic operations...")
        instance.insert(5)
        instance.insert(3)
        instance.insert(7)
        print(f"  After inserting elements: {instance}")
    except Exception as e:
        print(f"✗ Error creating BSTAnalyzer instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
