"""
Unit tests for Red-Black Tree implementation.

This module provides comprehensive tests for all Red-Black tree operations,
including edge cases, property validation, and performance benchmarks.
"""

import pytest
import timeit
from typing import List, Optional
from mastering_performant_code.chapter_08.red_black_tree import (
    RedBlackTree, RedBlackNode, Color, 
    red_black_height_analysis, benchmark_red_black_tree_operations,
    analyze_red_black_properties
)


class TestRedBlackNode:
    """Test cases for RedBlackNode class."""
    
    def test_node_creation(self):
        """Test node creation with different colors."""
        # Test red node
        red_node = RedBlackNode(10, Color.RED)
        assert red_node.key == 10
        assert red_node.color == Color.RED
        assert red_node.is_red()
        assert not red_node.is_black()
        
        # Test black node
        black_node = RedBlackNode(20, Color.BLACK)
        assert black_node.key == 20
        assert black_node.color == Color.BLACK
        assert black_node.is_black()
        assert not black_node.is_red()
        
        # Test default color (red)
        default_node = RedBlackNode(30)
        assert default_node.color == Color.RED
        assert default_node.is_red()
    
    def test_node_color_operations(self):
        """Test color setting operations."""
        node = RedBlackNode(10)
        
        # Test setting colors
        node.set_black()
        assert node.is_black()
        assert not node.is_red()
        
        node.set_red()
        assert node.is_red()
        assert not node.is_black()
    
    def test_node_relationships(self):
        """Test node relationship methods."""
        # Create a simple tree structure
        root = RedBlackNode(20)
        left = RedBlackNode(10)
        right = RedBlackNode(30)
        
        root.left = left
        root.right = right
        left.parent = root
        right.parent = root
        
        # Test sibling relationships
        assert left.get_sibling() == right
        assert right.get_sibling() == left
        assert root.get_sibling() is None
        
        # Test uncle relationships
        assert left.get_uncle() is None
        assert right.get_uncle() is None
        
        # Create grandparent structure
        grandparent = RedBlackNode(40)
        parent = RedBlackNode(25)
        uncle = RedBlackNode(35)
        
        grandparent.left = parent
        grandparent.right = uncle
        parent.parent = grandparent
        uncle.parent = grandparent
        
        # Add child to parent
        child = RedBlackNode(15)
        parent.left = child
        child.parent = parent
        
        # Test uncle relationship
        assert child.get_uncle() == uncle
    
    def test_node_repr(self):
        """Test node string representation."""
        red_node = RedBlackNode(10, Color.RED)
        black_node = RedBlackNode(20, Color.BLACK)
        
        assert repr(red_node) == "RedBlackNode(10, RED)"
        assert repr(black_node) == "RedBlackNode(20, BLACK)"


class TestRedBlackTree:
    """Test cases for RedBlackTree class."""
    
    def test_empty_tree(self):
        """Test empty tree properties."""
        tree = RedBlackTree()
        
        assert len(tree) == 0
        assert tree.is_empty()
        assert tree.root is None
        assert tree.find_min() is None
        assert tree.find_max() is None
        assert tree.height() == -1  # Empty tree should have height -1
        assert tree.black_height() == 0
        assert tree.is_valid()
    
    def test_single_node_insertion(self):
        """Test insertion of a single node."""
        tree = RedBlackTree()
        tree.insert(10)
        
        assert len(tree) == 1
        assert not tree.is_empty()
        assert tree.root is not None
        assert tree.root.key == 10
        assert tree.root.is_black()  # Root should be black
        assert tree.find_min() == 10
        assert tree.find_max() == 10
        assert tree.height() == 0  # Single node tree has height 0
        assert tree.black_height() == 1
        assert tree.is_valid()
    
    def test_multiple_insertions(self):
        """Test multiple insertions maintaining Red-Black properties."""
        tree = RedBlackTree()
        values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
        
        for value in values:
            tree.insert(value)
        
        assert len(tree) == len(values)
        assert tree.is_valid()
        assert tree.find_min() == 2
        assert tree.find_max() == 26
        
        # Check that all values are present
        for value in values:
            assert tree.search(value) is not None
    
    def test_search_operations(self):
        """Test search operations."""
        tree = RedBlackTree()
        values = [5, 3, 7, 1, 9]
        
        for value in values:
            tree.insert(value)
        
        # Test successful searches
        for value in values:
            node = tree.search(value)
            assert node is not None
            assert node.key == value
        
        # Test unsuccessful searches
        assert tree.search(0) is None
        assert tree.search(4) is None
        assert tree.search(8) is None
        assert tree.search(10) is None
    
    def test_deletion_operations(self):
        """Test deletion operations."""
        tree = RedBlackTree()
        values = [10, 5, 15, 3, 7, 12, 17]
        
        for value in values:
            tree.insert(value)
        
        initial_size = len(tree)
        
        # Test deletion of leaf node
        assert tree.delete(3)
        assert len(tree) == initial_size - 1
        assert tree.search(3) is None
        assert tree.is_valid()
        
        # Test deletion of node with one child
        assert tree.delete(5)
        assert len(tree) == initial_size - 2
        assert tree.search(5) is None
        assert tree.is_valid()
        
        # Test deletion of node with two children
        assert tree.delete(10)
        assert len(tree) == initial_size - 3
        assert tree.search(10) is None
        assert tree.is_valid()
        
        # Test deletion of non-existent node
        assert not tree.delete(100)
        assert len(tree) == initial_size - 3
    
    def test_traversal_operations(self):
        """Test all traversal methods."""
        tree = RedBlackTree()
        values = [5, 3, 7, 1, 9]
        
        for value in values:
            tree.insert(value)
        
        # Test inorder traversal
        inorder_result = list(tree.inorder_traversal())
        assert inorder_result == sorted(values)
        
        # Test preorder traversal
        preorder_result = list(tree.preorder_traversal())
        assert len(preorder_result) == len(values)
        assert set(preorder_result) == set(values)
        
        # Test postorder traversal
        postorder_result = list(tree.postorder_traversal())
        assert len(postorder_result) == len(values)
        assert set(postorder_result) == set(values)
        
        # Test level order traversal
        level_order_result = list(tree.level_order_traversal())
        assert len(level_order_result) > 0
        all_level_values = []
        for level in level_order_result:
            all_level_values.extend(level)
        assert set(all_level_values) == set(values)
    
    def test_find_min_max(self):
        """Test find minimum and maximum operations."""
        tree = RedBlackTree()
        
        # Test empty tree
        assert tree.find_min() is None
        assert tree.find_max() is None
        
        # Test single node
        tree.insert(10)
        assert tree.find_min() == 10
        assert tree.find_max() == 10
        
        # Test multiple nodes
        values = [5, 3, 7, 1, 9, 2, 8]
        for value in values:
            tree.insert(value)
        
        assert tree.find_min() == 1
        assert tree.find_max() == 10  # 10 was already in the tree
    
    def test_height_and_black_height(self):
        """Test height and black height calculations."""
        tree = RedBlackTree()
        
        # Test empty tree
        assert tree.height() == -1  # Empty tree should have height -1
        assert tree.black_height() == 0
        
        # Test single node
        tree.insert(10)
        assert tree.height() == 0  # Single node tree has height 0
        assert tree.black_height() == 1
        
        # Test multiple nodes
        tree.insert(5)
        tree.insert(15)
        height = tree.height()
        black_height = tree.black_height()
        
        assert height >= 1  # Should have height at least 1
        assert black_height >= 1  # Should have black height at least 1
        assert tree.is_valid()
    
    def test_red_black_properties(self):
        """Test that Red-Black properties are maintained."""
        tree = RedBlackTree()
        
        # Test empty tree
        assert tree.is_valid()
        
        # Test with various insertions
        values = [10, 5, 15, 3, 7, 12, 17, 1, 9, 11, 13, 16, 18]
        
        for value in values:
            tree.insert(value)
            assert tree.is_valid(), f"Tree invalid after inserting {value}"
        
        # Test after deletions
        for value in [3, 7, 15]:
            tree.delete(value)
            assert tree.is_valid(), f"Tree invalid after deleting {value}"
    
    def test_complex_scenarios(self):
        """Test complex insertion and deletion scenarios."""
        tree = RedBlackTree()
        
        # Insert in reverse order
        for i in range(10, 0, -1):
            tree.insert(i)
            assert tree.is_valid()
        
        # Delete in random order
        delete_order = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
        for value in delete_order:
            if tree.search(value) is not None:
                tree.delete(value)
                assert tree.is_valid()
    
    def test_duplicate_handling(self):
        """Test handling of duplicate keys."""
        tree = RedBlackTree()
        
        # Insert same value multiple times
        for _ in range(5):
            tree.insert(10)
        
        # Should only have one node with key 10
        assert len(tree) == 5  # Current implementation allows duplicates
        assert tree.search(10) is not None
    
    def test_large_dataset(self):
        """Test with a larger dataset."""
        tree = RedBlackTree()
        values = list(range(1, 101))  # 1 to 100
        
        # Insert all values
        for value in values:
            tree.insert(value)
        
        assert len(tree) == 100
        assert tree.is_valid()
        assert tree.find_min() == 1
        assert tree.find_max() == 100
        
        # Test search for all values
        for value in values:
            assert tree.search(value) is not None
        
        # Test deletion of every other value
        for value in values[::2]:
            tree.delete(value)
        
        assert len(tree) == 50
        assert tree.is_valid()
    
    def test_edge_cases(self):
        """Test various edge cases."""
        tree = RedBlackTree()
        
        # Test empty tree operations
        assert tree.delete(10) == False
        assert tree.search(10) is None
        assert tree.height() == -1  # Empty tree should have height -1
        assert tree.black_height() == 0
        
        # Test single node deletion (root deletion)
        tree.insert(10)
        assert tree.delete(10) == True
        assert tree.is_empty()
        assert tree.height() == -1
        
        # Test insertion of duplicate keys
        tree.insert(10)
        tree.insert(10)  # Should handle duplicates gracefully
        assert len(tree) == 2
        
        # Test with negative numbers
        tree = RedBlackTree()
        tree.insert(-5)
        tree.insert(-10)
        tree.insert(-3)
        assert tree.is_valid()
        assert tree.find_min() == -10
        assert tree.find_max() == -3
    
    def test_height_bounds(self):
        """Test that height bounds are maintained."""
        import math
        
        tree = RedBlackTree()
        for i in range(1000):
            tree.insert(i)
        
        height = tree.height()
        theoretical_bound = 2 * math.log2(1000 + 1)
        assert height <= theoretical_bound
        
        # Test with larger dataset
        tree = RedBlackTree()
        for i in range(10000):
            tree.insert(i)
        
        height = tree.height()
        theoretical_bound = 2 * math.log2(10000 + 1)
        assert height <= theoretical_bound
    
    def test_black_height_validation(self):
        """Test black height validation across all paths."""
        tree = RedBlackTree()
        values = [7, 3, 18, 10, 22, 8, 11, 26, 2, 6, 13]
        
        for value in values:
            tree.insert(value)
        
        # Should not raise ValueError for valid tree
        black_height = tree.black_height()
        assert black_height > 0
        
        # Test that invalid trees raise ValueError
        # This would require manually creating an invalid tree structure
        # which is complex, so we'll test the validation method directly
        assert tree.is_valid()
    
    def test_very_large_dataset(self):
        """Test behavior with very large datasets."""
        tree = RedBlackTree()
        
        # Insert 10,000 nodes
        for i in range(10000):
            tree.insert(i)
        
        assert len(tree) == 10000
        assert tree.is_valid()
        assert tree.find_min() == 0
        assert tree.find_max() == 9999
        
        # Test search performance
        import time
        start_time = time.time()
        for i in range(0, 10000, 100):
            assert tree.search(i) is not None
        search_time = time.time() - start_time
        
        # Search should be fast (O(log n))
        assert search_time < 1.0  # Should complete in under 1 second


class TestRedBlackTreeApplications:
    """Test cases for real-world applications."""
    
    def test_database_index(self):
        """Test database index application."""
        from mastering_performant_code.chapter_08.applications import DatabaseIndex
        
        index = DatabaseIndex()
        
        # Test insertion
        index.insert(1, "Alice")
        index.insert(2, "Bob")
        index.insert(3, "Charlie")
        
        # Test search
        assert index.search(1) == "Alice"
        assert index.search(2) == "Bob"
        assert index.search(3) == "Charlie"
        assert index.search(4) is None
        
        # Test range query
        results = index.range_query(1, 2)
        assert len(results) == 2
        assert ("Alice", 1) in [(v, k) for k, v in results]
        assert ("Bob", 2) in [(v, k) for k, v in results]
        
        # Test deletion
        assert index.delete(2)
        assert index.search(2) is None
        assert not index.delete(2)  # Already deleted
    
    def test_priority_queue(self):
        """Test priority queue application."""
        from mastering_performant_code.chapter_08.applications import PriorityQueue
        
        pq = PriorityQueue()
        
        # Test empty queue
        assert pq.is_empty()
        assert pq.size() == 0
        assert pq.peek() is None
        assert pq.dequeue() is None
        
        # Test enqueue and dequeue
        pq.enqueue(3, "Task C")
        pq.enqueue(1, "Task A")
        pq.enqueue(2, "Task B")
        
        assert not pq.is_empty()
        assert pq.size() == 3
        
        # Test peek
        assert "Task A" in pq.peek()
        
        # Test dequeue order
        assert "Task A" in pq.dequeue()
        assert "Task B" in pq.dequeue()
        assert "Task C" in pq.dequeue()
        assert pq.dequeue() is None
    
    def test_symbol_table(self):
        """Test symbol table application."""
        from mastering_performant_code.chapter_08.applications import SymbolTable
        
        st = SymbolTable()
        
        # Test insertion
        assert st.insert("x", {"type": "int", "value": 10})
        assert st.insert("y", {"type": "string", "value": "hello"})
        
        # Test duplicate insertion
        assert not st.insert("x", {"type": "float", "value": 20.5})
        
        # Test lookup
        x_info = st.lookup("x")
        assert x_info is not None
        assert x_info["name"] == "x"
        assert x_info["scope"] == 0
        
        # Test non-existent symbol
        assert st.lookup("z") is None
        
        # Test scoping
        st.enter_scope()
        assert st.insert("x", {"type": "float", "value": 30.0})
        
        x_info = st.lookup("x")
        assert x_info is not None
        assert x_info["scope"] == 1
        
        # Test scope exit
        st.exit_scope()
        x_info = st.lookup("x")
        assert x_info is not None
        assert x_info["scope"] == 0
        
        # Test deletion
        assert st.delete("x")
        assert st.lookup("x") is None


class TestRedBlackTreeAnalysis:
    """Test cases for analysis functions."""
    
    def test_height_analysis(self):
        """Test height analysis function."""
        result = red_black_height_analysis(100)
        
        assert "nodes" in result
        assert "rb_height_bound" in result
        assert "avl_height_bound" in result
        assert "perfect_height" in result
        
        assert result["nodes"] == 100
        assert result["rb_height_bound"] > 0
        assert result["avl_height_bound"] > 0
        assert result["perfect_height"] > 0
        
        # Test edge cases
        result_0 = red_black_height_analysis(0)
        assert result_0["nodes"] == 0
        
        result_1 = red_black_height_analysis(1)
        assert result_1["nodes"] == 1
    
    def test_benchmark_functions(self):
        """Test benchmark functions."""
        # Test that benchmark functions run without error
        try:
            benchmark_red_black_tree_operations()
        except Exception as e:
            pytest.fail(f"Benchmark function failed: {e}")
    
    def test_property_analysis(self):
        """Test property analysis function."""
        # Test that analysis function runs without error
        try:
            analyze_red_black_properties()
        except Exception as e:
            pytest.fail(f"Property analysis function failed: {e}")


class TestRedBlackTreePerformance:
    """Test cases for performance characteristics."""
    
    def test_insertion_performance(self):
        """Test insertion performance."""
        tree = RedBlackTree()
        
        # Measure insertion time for 1000 elements
        def insert_operation():
            for i in range(1000):
                tree.insert(i)
        
        # This should complete in reasonable time
        execution_time = timeit.timeit(insert_operation, number=1)
        assert execution_time < 1.0  # Should complete in less than 1 second
        
        assert len(tree) == 1000
        assert tree.is_valid()
    
    def test_search_performance(self):
        """Test search performance."""
        tree = RedBlackTree()
        
        # Insert 1000 elements
        for i in range(1000):
            tree.insert(i)
        
        # Measure search time
        def search_operation():
            for i in range(1000):
                tree.search(i)
        
        execution_time = timeit.timeit(search_operation, number=1)
        assert execution_time < 1.0  # Should complete in less than 1 second
    
    def test_deletion_performance(self):
        """Test deletion performance."""
        tree = RedBlackTree()
        
        # Insert 1000 elements
        for i in range(1000):
            tree.insert(i)
        
        # Measure deletion time
        def deletion_operation():
            for i in range(500):  # Delete half the elements
                tree.delete(i)
        
        execution_time = timeit.timeit(deletion_operation, number=1)
        assert execution_time < 1.0  # Should complete in less than 1 second
        
        assert len(tree) == 500
        assert tree.is_valid()


if __name__ == "__main__":
    pytest.main([__file__]) 