"""
Unit tests for Red-Black Tree applications.

This module provides comprehensive tests for all real-world applications
of Red-Black trees, including database indexing, priority queues,
symbol tables, file systems, and network routing.
"""

import pytest
from typing import List, Tuple, Optional, Dict
from mastering_performant_code.chapter_08.applications import (
    DatabaseIndex, PriorityQueue, SymbolTable, 
    FileSystemTree, NetworkRoutingTable
)
import shutil
import os


class TestDatabaseIndex:
    """Test cases for DatabaseIndex application."""
    
    def test_empty_index(self):
        """Test empty database index."""
        index = DatabaseIndex()
        
        assert index.search(1) is None
        assert index.range_query(1, 10) == []
        assert not index.delete(1)
    
    def test_basic_operations(self):
        """Test basic database index operations."""
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
    
    def test_range_queries(self):
        """Test range query functionality."""
        index = DatabaseIndex()
        
        # Insert data
        data = [(1, "A"), (2, "B"), (3, "C"), (4, "D"), (5, "E")]
        for key, value in data:
            index.insert(key, value)
        
        # Test various range queries
        assert index.range_query(1, 3) == [(1, "A"), (2, "B"), (3, "C")]
        assert index.range_query(2, 4) == [(2, "B"), (3, "C"), (4, "D")]
        assert index.range_query(1, 1) == [(1, "A")]
        assert index.range_query(10, 20) == []
        assert index.range_query(0, 0) == []
    
    def test_deletion(self):
        """Test deletion operations."""
        index = DatabaseIndex()
        
        # Insert data
        index.insert(1, "Alice")
        index.insert(2, "Bob")
        index.insert(3, "Charlie")
        
        # Test deletion
        assert index.delete(2)
        assert index.search(2) is None
        assert index.search(1) == "Alice"  # Other data should remain
        assert index.search(3) == "Charlie"
        
        # Test deletion of non-existent key
        assert not index.delete(2)  # Already deleted
        assert not index.delete(4)  # Never existed
    
    def test_large_dataset(self):
        """Test with larger dataset."""
        index = DatabaseIndex()
        
        # Insert 100 records
        for i in range(1, 101):
            index.insert(i, f"Record_{i}")
        
        # Test search
        assert index.search(1) == "Record_1"
        assert index.search(50) == "Record_50"
        assert index.search(100) == "Record_100"
        assert index.search(101) is None
        
        # Test range query
        results = index.range_query(25, 75)
        assert len(results) == 51
        assert results[0] == (25, "Record_25")
        assert results[-1] == (75, "Record_75")
        
        # Test deletion of multiple records
        for i in range(1, 51):
            assert index.delete(i)
        
        # Verify remaining records
        assert index.search(1) is None
        assert index.search(50) is None
        assert index.search(51) == "Record_51"
        assert index.search(100) == "Record_100"


class TestPriorityQueue:
    """Test cases for PriorityQueue application."""
    
    def test_empty_queue(self):
        """Test empty priority queue."""
        pq = PriorityQueue()
        
        assert pq.is_empty()
        assert pq.size() == 0
        assert pq.peek() is None
        assert pq.dequeue() is None
    
    def test_basic_operations(self):
        """Test basic priority queue operations."""
        pq = PriorityQueue()
        
        # Test enqueue
        pq.enqueue(3, "Task C")
        pq.enqueue(1, "Task A")
        pq.enqueue(2, "Task B")
        
        assert not pq.is_empty()
        assert pq.size() == 3
        
        # Test peek
        peek_result = pq.peek()
        assert peek_result is not None
        assert "Task A" in peek_result  # Lowest priority number should be highest priority
    
    def test_dequeue_order(self):
        """Test that dequeue returns items in correct priority order."""
        pq = PriorityQueue()
        
        # Insert items with different priorities
        pq.enqueue(5, "Low Priority")
        pq.enqueue(1, "High Priority")
        pq.enqueue(3, "Medium Priority")
        pq.enqueue(2, "Medium-High Priority")
        
        # Dequeue should return in priority order (lowest number = highest priority)
        assert "High Priority" in pq.dequeue()
        assert "Medium-High Priority" in pq.dequeue()
        assert "Medium Priority" in pq.dequeue()
        assert "Low Priority" in pq.dequeue()
        assert pq.dequeue() is None
    
    def test_duplicate_priorities(self):
        """Test handling of duplicate priorities."""
        pq = PriorityQueue()
        
        # Insert items with same priority
        pq.enqueue(1, "Task A")
        pq.enqueue(1, "Task B")
        pq.enqueue(1, "Task C")
        
        assert pq.size() == 3
        
        # All should be dequeued (order may vary due to count tiebreaker)
        results = []
        while not pq.is_empty():
            results.append(pq.dequeue())
        
        assert len(results) == 3
        assert all("Task" in result for result in results)
    
    def test_large_queue(self):
        """Test with larger priority queue."""
        pq = PriorityQueue()
        
        # Insert 100 items with random priorities
        for i in range(100):
            priority = (i * 7) % 10  # Create some duplicate priorities
            pq.enqueue(priority, f"Task_{i}")
        
        assert pq.size() == 100
        
        # Dequeue all items
        results = []
        while not pq.is_empty():
            results.append(pq.dequeue())
        
        assert len(results) == 100
        assert pq.is_empty()
        assert pq.size() == 0
    
    def test_edge_cases(self):
        """Test edge cases for priority queue."""
        pq = PriorityQueue()
        
        # Test with negative priorities
        pq.enqueue(-5, "Negative Priority")
        pq.enqueue(0, "Zero Priority")
        pq.enqueue(10, "Positive Priority")
        
        # Negative should be highest priority (lowest number)
        result = pq.dequeue()
        assert "Negative Priority" in result
        
        # Test with very large priorities
        pq.enqueue(1000000, "Very High Number")
        pq.enqueue(1, "Low Number")
        
        # Next highest priority should be "Zero Priority" (priority 0)
        result = pq.dequeue()
        assert "Zero Priority" in result

    def test_actual_item_storage_and_retrieval(self):
        pq = PriorityQueue()
        pq.enqueue(3, "Task C")
        pq.enqueue(1, "Task A")
        pq.enqueue(2, "Task B")
        assert pq.dequeue() == "Task A"
        assert pq.dequeue() == "Task B"
        assert pq.dequeue() == "Task C"
        assert pq.dequeue() is None


class TestSymbolTable:
    """Test cases for SymbolTable application."""
    
    def test_empty_symbol_table(self):
        """Test empty symbol table."""
        st = SymbolTable()
        
        assert st.lookup("x") is None
        assert st.get_all_symbols() == []
        assert not st.delete("x")
    
    def test_basic_operations(self):
        """Test basic symbol table operations."""
        st = SymbolTable()
        
        # Test insertion
        assert st.insert("x", {"type": "int", "value": 10})
        assert st.insert("y", {"type": "string", "value": "hello"})
        
        # Test lookup
        x_info = st.lookup("x")
        assert x_info is not None
        assert x_info["name"] == "x"
        assert x_info["scope"] == 0
        
        y_info = st.lookup("y")
        assert y_info is not None
        assert y_info["name"] == "y"
        assert y_info["scope"] == 0
        
        # Test non-existent symbol
        assert st.lookup("z") is None
    
    def test_duplicate_insertion(self):
        """Test duplicate symbol insertion."""
        st = SymbolTable()
        
        # First insertion should succeed
        assert st.insert("x", {"type": "int", "value": 10})
        
        # Second insertion with same name should fail
        assert not st.insert("x", {"type": "float", "value": 20.5})
        
        # Lookup should still return original scope
        x_info = st.lookup("x")
        assert x_info is not None
        assert x_info["scope"] == 0
    
    def test_scoping(self):
        """Test symbol table scoping."""
        st = SymbolTable()
        
        # Insert in global scope
        st.insert("global_var", {"type": "int", "value": 100})
        
        # Enter new scope
        st.enter_scope()
        st.insert("local_var", {"type": "string", "value": "local"})
        
        # Lookup should find local variable first
        local_info = st.lookup("local_var")
        assert local_info is not None
        assert local_info["scope"] == 1
        
        # Global variable should still be accessible
        global_info = st.lookup("global_var")
        assert global_info is not None
        assert global_info["scope"] == 0
        
        # Exit scope
        st.exit_scope()
        
        # Local variable should no longer be accessible
        assert st.lookup("local_var") is None
        
        # Global variable should still be accessible
        assert st.lookup("global_var") is not None
    
    def test_nested_scopes(self):
        """Test deeply nested scopes."""
        st = SymbolTable()
        
        # Global scope
        st.insert("global", {"type": "int", "value": 0})
        
        # Scope 1
        st.enter_scope()
        st.insert("level1", {"type": "int", "value": 1})
        
        # Scope 2
        st.enter_scope()
        st.insert("level2", {"type": "int", "value": 2})
        
        # Scope 3
        st.enter_scope()
        st.insert("level3", {"type": "int", "value": 3})
        
        # Test lookup in different scopes
        assert st.lookup("level3")["scope"] == 3
        assert st.lookup("level2")["scope"] == 2
        assert st.lookup("level1")["scope"] == 1
        assert st.lookup("global")["scope"] == 0
        
        # Exit scopes
        st.exit_scope()
        assert st.lookup("level3") is None
        assert st.lookup("level2") is not None
        
        st.exit_scope()
        assert st.lookup("level2") is None
        assert st.lookup("level1") is not None
        
        st.exit_scope()
        assert st.lookup("level1") is None
        assert st.lookup("global") is not None
    
    def test_deletion(self):
        """Test symbol deletion."""
        st = SymbolTable()
        
        # Insert symbols
        st.insert("x", {"type": "int", "value": 10})
        st.insert("y", {"type": "string", "value": "hello"})
        
        # Test deletion
        assert st.delete("x")
        assert st.lookup("x") is None
        assert st.lookup("y") is not None  # Other symbol should remain
        
        # Test deletion of non-existent symbol
        assert not st.delete("x")  # Already deleted
        assert not st.delete("z")  # Never existed
    
    def test_get_all_symbols(self):
        """Test getting all symbols in current scope."""
        st = SymbolTable()
        
        # Insert symbols in global scope
        st.insert("a", {"type": "int"})
        st.insert("b", {"type": "string"})
        st.insert("c", {"type": "float"})
        
        symbols = st.get_all_symbols()
        assert len(symbols) == 3
        assert "a" in symbols
        assert "b" in symbols
        assert "c" in symbols
        
        # Enter new scope and insert more symbols
        st.enter_scope()
        st.insert("d", {"type": "int"})
        st.insert("e", {"type": "string"})
        
        symbols = st.get_all_symbols()
        assert len(symbols) == 2
        assert "d" in symbols
        assert "e" in symbols
        assert "a" not in symbols  # Should not include symbols from parent scope
    
    def test_scope_boundaries(self):
        """Test scope boundary conditions."""
        st = SymbolTable()
        
        # Try to exit scope when already at global scope
        st.exit_scope()  # Should not raise error
        
        # Should still be able to insert in global scope
        assert st.insert("x", {"type": "int", "value": 10})
        assert st.lookup("x") is not None
    
    def test_large_symbol_table(self):
        """Test with larger symbol table."""
        st = SymbolTable()
        
        # Insert many symbols
        for i in range(100):
            st.insert(f"var_{i}", {"type": "int", "value": i})
        
        # Test lookup for all symbols
        for i in range(100):
            info = st.lookup(f"var_{i}")
            assert info is not None
            assert info["name"] == f"var_{i}"
            assert info["scope"] == 0
        
        # Test get_all_symbols
        symbols = st.get_all_symbols()
        assert len(symbols) == 100
        assert all(f"var_{i}" in symbols for i in range(100))

    def test_symbol_table_scope_operations(self):
        """Test symbol table scope operations."""
        symbol_table = SymbolTable()
        
        # Insert symbols in global scope
        symbol_table.insert("global_var", {"type": "int", "value": 42})
        symbol_table.insert("global_func", {"type": "function", "params": ["x", "y"]})
        
        # Enter new scope
        symbol_table.enter_scope()
        symbol_table.insert("local_var", {"type": "string", "value": "hello"})
        
        # Test lookup in current scope
        local_symbol = symbol_table.lookup("local_var")
        assert local_symbol is not None
        assert local_symbol["type"] == "string"
        
        # Test lookup of global symbol from local scope
        global_symbol = symbol_table.lookup("global_var")
        assert global_symbol is not None
        assert global_symbol["type"] == "int"
        
        # Exit scope
        symbol_table.exit_scope()
        
        # Test that local symbol is no longer accessible
        assert symbol_table.lookup("local_var") is None
        assert symbol_table.lookup("global_var") is not None

    def test_symbol_table_data_storage(self):
        st = SymbolTable()
        st.insert("x", {"type": "int", "value": 42})
        result = st.lookup("x")
        assert result["type"] == "int"
        assert result["value"] == 42
        assert result["name"] == "x"
        assert "scope" in result


class TestFileSystemTree:
    """Test cases for FileSystemTree application."""
    
    def setup_method(self):
        self.test_root = "tmp_test_fs"
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)
        os.mkdir(self.test_root)
        self.fs = FileSystemTree()
        self.fs.create_directory(self.test_root)
    
    def teardown_method(self):
        if os.path.exists(self.test_root):
            shutil.rmtree(self.test_root)
    
    def test_file_system_creation(self):
        fs = self.fs
        root = self.test_root
        # Create directories
        assert fs.create_directory(f"{root}/home")
        assert fs.create_directory(f"{root}/home/user")
        assert fs.create_directory(f"{root}/var")
        assert fs.create_directory(f"{root}/var/log")
        # Create files
        assert fs.create_file(f"{root}/home/user/file1.txt", 1024, {"owner": "user"})
        assert fs.create_file(f"{root}/home/user/file2.txt", 2048, {"owner": "user"})
        assert fs.create_file(f"{root}/var/log/system.log", 5120, {"owner": "root"})
        # Test directory listing
        home_contents = fs.list_directory(f"{root}/home")
        assert "user" in home_contents
        user_contents = fs.list_directory(f"{root}/home/user")
        assert len(user_contents) == 2
        assert f"{root}/home/user/file1.txt" in user_contents
        assert f"{root}/home/user/file2.txt" in user_contents
    
    def test_file_operations(self):
        """Test file operations."""
        fs = self.fs
        fs.create_directory("/test")
        
        # Create file
        assert fs.create_file("/test/file.txt", 1024, {"type": "text"})
        
        # Get file info
        file_info = fs.get_file_info("/test/file.txt")
        assert file_info is not None
        assert file_info["size"] == 1024
        assert file_info["metadata"]["type"] == "text"
        assert file_info["parent"] == "/test"
        
        # Delete file
        assert fs.delete_file("/test/file.txt")
        assert fs.get_file_info("/test/file.txt") is None
    
    def test_directory_operations(self):
        fs = self.fs
        root = self.test_root
        # Create nested directory structure
        assert fs.create_directory(f"{root}/root")
        assert fs.create_directory(f"{root}/root/subdir1")
        assert fs.create_directory(f"{root}/root/subdir2")
        assert fs.create_file(f"{root}/root/file1.txt", 100)
        assert fs.create_file(f"{root}/root/subdir1/file2.txt", 200)
        assert fs.create_file(f"{root}/root/subdir2/file3.txt", 300)
        # Delete directory with contents
        assert fs.delete_directory(f"{root}/root")
        # Verify all contents are deleted
        assert fs.get_file_info(f"{root}/root/file1.txt") is None
        assert fs.get_file_info(f"{root}/root/subdir1/file2.txt") is None
        assert fs.get_file_info(f"{root}/root/subdir2/file3.txt") is None
    
    def test_file_system_validation(self):
        fs = self.fs
        root = self.test_root
        # Try to create file without parent directory
        assert not fs.create_file(f"{root}/nonexistent/file.txt", 100)
        # Try to create duplicate directory
        fs.create_directory(f"{root}/test")
        assert not fs.create_directory(f"{root}/test")
        # Try to create duplicate file
        fs.create_directory(f"{root}/test2")
        fs.create_file(f"{root}/test2/file.txt", 100)
        assert not fs.create_file(f"{root}/test2/file.txt", 200)
        # Try to delete non-existent file/directory
        assert not fs.delete_file(f"{root}/nonexistent.txt")
        assert not fs.delete_directory(f"{root}/nonexistent")


class TestNetworkRoutingTable:
    """Test cases for NetworkRoutingTable application."""
    
    def test_routing_table_operations(self):
        """Test basic routing table operations."""
        routing_table = NetworkRoutingTable()
        
        # Add routes
        assert routing_table.add_route("192.168.1", "192.168.1.1", "eth0", 1)
        assert routing_table.add_route("10.0.0", "10.0.0.1", "eth1", 2)
        assert routing_table.add_route("172.16.0", "172.16.0.1", "eth2", 3)
        
        # Look up routes (use matching prefixes)
        route1 = routing_table.lookup_route("192.168.1.5")
        assert route1 is not None
        assert route1["next_hop"] == "192.168.1.1"
        assert route1["interface"] == "eth0"
        
        route2 = routing_table.lookup_route("10.0.0.10")
        assert route2 is not None
        assert route2["next_hop"] == "10.0.0.1"
        assert route2["interface"] == "eth1"
    
    def test_prefix_matching(self):
        """Test prefix matching functionality."""
        routing_table = NetworkRoutingTable()
        
        # Add routes with different prefix lengths
        routing_table.add_route("192.168.1", "192.168.1.1", "eth0")
        routing_table.add_route("192.168", "192.168.0.1", "eth1")
        routing_table.add_route("192", "192.0.0.1", "eth2")
        
        # Test longest prefix matching
        route = routing_table.lookup_route("192.168.1.100")
        assert route is not None
        assert route["next_hop"] == "192.168.1.1"  # Should match 192.168.1
        
        route = routing_table.lookup_route("192.168.2.100")
        assert route is not None
        assert route["next_hop"] == "192.168.0.1"  # Should match 192.168
        
        route = routing_table.lookup_route("192.200.1.100")
        assert route is not None
        assert route["next_hop"] == "192.0.0.1"  # Should match 192
    
    def test_route_management(self):
        """Test route management operations."""
        routing_table = NetworkRoutingTable()
        
        # Add route
        routing_table.add_route("192.168.1", "192.168.1.1", "eth0", 1)
        
        # Update metric
        assert routing_table.update_metric("192.168.1", 5)
        
        # Verify update
        route = routing_table.lookup_route("192.168.1.5")
        assert route is not None
        assert route["metric"] == 5
        
        # Remove route
        assert routing_table.remove_route("192.168.1")
        
        # Verify removal
        assert routing_table.lookup_route("192.168.1.5") is None
    
    def test_routing_table_validation(self):
        """Test routing table validation and error handling."""
        routing_table = NetworkRoutingTable()
        
        # Try to add duplicate route
        routing_table.add_route("192.168.1.0", "192.168.1.1", "eth0")
        assert not routing_table.add_route("192.168.1.0", "192.168.1.2", "eth1")
        
        # Try to update non-existent route
        assert not routing_table.update_metric("192.168.2.0", 5)
        
        # Try to remove non-existent route
        assert not routing_table.remove_route("192.168.2.0")
        
        # Test lookup with no matching routes
        assert routing_table.lookup_route("192.168.2.5") is None
    
    def test_get_all_routes(self):
        """Test getting all routing entries."""
        routing_table = NetworkRoutingTable()
        
        # Add multiple routes
        routing_table.add_route("192.168.1.0", "192.168.1.1", "eth0", 1)
        routing_table.add_route("10.0.0.0", "10.0.0.1", "eth1", 2)
        routing_table.add_route("172.16.0.0", "172.16.0.1", "eth2", 3)
        
        # Get all routes
        all_routes = routing_table.get_all_routes()
        assert len(all_routes) == 3
        
        # Verify route data
        route_dict = dict(all_routes)
        assert "192.168.1.0" in route_dict
        assert "10.0.0.0" in route_dict
        assert "172.16.0.0" in route_dict
        
        assert route_dict["192.168.1.0"]["next_hop"] == "192.168.1.1"
        assert route_dict["10.0.0.0"]["metric"] == 2
        assert route_dict["172.16.0.0"]["interface"] == "eth2"


if __name__ == "__main__":
    pytest.main([__file__]) 