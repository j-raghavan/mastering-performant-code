"""
Real-World Applications of Red-Black Trees

This module demonstrates practical applications of Red-Black trees
in various domains including database indexing, priority queues,
compiler symbol tables, file system structures, and network routing.

Classes:
    - DatabaseIndex: Database indexing application
    - PriorityQueue: Priority queue implementation
    - SymbolTable: Symbol table for compilers
    - FileSystemTree: File system directory structure
    - NetworkRoutingTable: Network routing table implementation
"""

from typing import Optional, List, Tuple, Dict
from .red_black_tree import RedBlackTree

class DatabaseIndex:
    """
    A simple database index using Red-Black trees.
    
    This demonstrates how Red-Black trees can be used for efficient
    database indexing and range queries.
    """
    
    def __init__(self):
        self.index = RedBlackTree[int]()
        self.data = {}
    
    def insert(self, key: int, value: str) -> None:
        """Insert a key-value pair into the index."""
        self.index.insert(key)
        self.data[key] = value
    
    def search(self, key: int) -> Optional[str]:
        """Search for a value by key."""
        if self.index.search(key) is not None:
            return self.data.get(key)
        return None
    
    def range_query(self, start: int, end: int) -> List[Tuple[int, str]]:
        """Perform a range query."""
        result = []
        for key in self.index.inorder_traversal():
            if start <= key <= end:
                result.append((key, self.data[key]))
        return result
    
    def delete(self, key: int) -> bool:
        """Delete a key-value pair."""
        if self.index.delete(key):
            del self.data[key]
            return True
        return False

class PriorityQueue:
    """
    A priority queue implementation using Red-Black trees.
    
    This provides O(log n) insertion and deletion operations,
    making it suitable for applications requiring efficient
    priority-based scheduling.
    """
    
    def __init__(self):
        self.tree = RedBlackTree[int]()
        self.items = {}  # Store actual items
        self.count = 0
    
    def enqueue(self, priority: int, item: str) -> None:
        """Add an item with given priority."""
        # Use priority as key, with count to handle duplicates
        key = priority * 1000000 + self.count
        self.tree.insert(key)
        self.items[key] = item  # Store the actual item
        self.count += 1
    
    def dequeue(self) -> Optional[str]:
        """Remove and return the highest priority item."""
        if self.tree.is_empty():
            return None
        
        min_key = self.tree.find_min()
        if min_key is not None:
            self.tree.delete(min_key)
            item = self.items.pop(min_key, None)
            return item
        return None
    
    def peek(self) -> Optional[str]:
        """Return the highest priority item without removing it."""
        if self.tree.is_empty():
            return None
        
        min_key = self.tree.find_min()
        if min_key is not None:
            return self.items.get(min_key, None)
        return None
    
    def is_empty(self) -> bool:
        """Check if the priority queue is empty."""
        return self.tree.is_empty()
    
    def size(self) -> int:
        """Get the size of the priority queue."""
        return len(self.tree)

class SymbolTable:
    """
    A symbol table implementation using Red-Black trees.
    
    This demonstrates how Red-Black trees can be used in compiler
    design for efficient symbol lookup and scoping.
    """
    
    def __init__(self):
        self.scopes = [RedBlackTree[str]()]
        self.symbol_data = [{}]  # Store actual symbol information
        self.current_scope = 0
    
    def enter_scope(self) -> None:
        """Enter a new scope."""
        self.scopes.append(RedBlackTree[str]())
        self.symbol_data.append({})
        self.current_scope += 1
    
    def exit_scope(self) -> None:
        """Exit the current scope."""
        if self.current_scope > 0:
            self.scopes.pop()
            self.symbol_data.pop()
            self.current_scope -= 1
    
    def insert(self, name: str, symbol_info: Dict) -> bool:
        """Insert a symbol into the current scope."""
        # Check if symbol already exists in current scope
        if self.scopes[self.current_scope].search(name) is not None:
            return False
        
        self.scopes[self.current_scope].insert(name)
        self.symbol_data[self.current_scope][name] = symbol_info
        return True
    
    def lookup(self, name: str) -> Optional[Dict]:
        """Look up a symbol starting from current scope."""
        for i in range(self.current_scope, -1, -1):
            if self.scopes[i].search(name) is not None:
                symbol_info = self.symbol_data[i].get(name, {})
                return {
                    "name": name,
                    "scope": i,
                    **symbol_info
                }
        return None
    
    def delete(self, name: str) -> bool:
        """Delete a symbol from the current scope."""
        if self.scopes[self.current_scope].delete(name):
            self.symbol_data[self.current_scope].pop(name, None)
            return True
        return False
    
    def get_all_symbols(self) -> List[str]:
        """Get all symbols in the current scope."""
        return list(self.scopes[self.current_scope].inorder_traversal())

class FileSystemTree:
    """
    A file system directory structure using Red-Black trees.
    
    This demonstrates how Red-Black trees can be used to represent
    hierarchical file system structures with efficient lookup and traversal.
    """
    
    def __init__(self):
        self.directories = RedBlackTree[str]()
        self.files = {}  # Store file metadata
        self.directory_contents = {}  # Store directory contents
    
    def create_directory(self, path: str) -> bool:
        """Create a new directory."""
        if path in self.directory_contents:
            return False
        
        parent_dir = self._get_parent_directory(path)
        if parent_dir:
            if parent_dir not in self.directory_contents:
                return False  # Parent directory must exist
            self.directory_contents[parent_dir].append(path.split('/')[-1])
        self.directories.insert(path)
        self.directory_contents[path] = []
        return True
    
    def create_file(self, path: str, size: int, metadata: Dict = None) -> bool:
        """Create a new file."""
        if path in self.files:
            return False
        
        parent_dir = self._get_parent_directory(path)
        if not parent_dir or parent_dir not in self.directory_contents:
            return False  # Parent directory must exist
        self.files[path] = {
            'size': size,
            'metadata': metadata or {},
            'parent': parent_dir
        }
        self.directory_contents[parent_dir].append(path)
        return True
    
    def _get_parent_directory(self, path: str) -> Optional[str]:
        """Get the parent directory of a path."""
        if '/' not in path:
            return None
        return '/'.join(path.split('/')[:-1])
    
    def list_directory(self, path: str) -> List[str]:
        """List contents of a directory."""
        return self.directory_contents.get(path, [])
    
    def get_file_info(self, path: str) -> Optional[Dict]:
        """Get file information."""
        return self.files.get(path)
    
    def delete_file(self, path: str) -> bool:
        """Delete a file."""
        if path not in self.files:
            return False
        
        parent_dir = self.files[path]['parent']
        if parent_dir in self.directory_contents:
            self.directory_contents[parent_dir].remove(path)
        del self.files[path]
        return True
    
    def delete_directory(self, path: str) -> bool:
        """Delete a directory and all its contents."""
        if path not in self.directory_contents:
            return False
        
        # Recursively delete all contents
        for item in list(self.directory_contents[path]):
            full_path = path + '/' + item if '/' not in item and not item.startswith(path + '/') else item
            if full_path in self.files:
                del self.files[full_path]
            elif full_path in self.directory_contents:
                self.delete_directory(full_path)
        
        # Remove this directory from its parent
        parent_dir = self._get_parent_directory(path)
        if parent_dir and parent_dir in self.directory_contents:
            name = path.split('/')[-1]
            if name in self.directory_contents[parent_dir]:
                self.directory_contents[parent_dir].remove(name)
        
        self.directories.delete(path)
        del self.directory_contents[path]
        return True

class NetworkRoutingTable:
    """
    A network routing table using Red-Black trees.
    
    This demonstrates how Red-Black trees can be used for efficient
    IP address lookup and routing decisions in network infrastructure.
    """
    
    def __init__(self):
        self.routes = RedBlackTree[str]()
        self.route_data = {}  # Store routing information
    
    def add_route(self, destination: str, next_hop: str, 
                  interface: str, metric: int = 1) -> bool:
        """Add a routing entry."""
        if destination in self.route_data:
            return False
        
        self.routes.insert(destination)
        self.route_data[destination] = {
            'next_hop': next_hop,
            'interface': interface,
            'metric': metric
        }
        return True
    
    def _is_prefix_match(self, route: str, destination: str) -> int:
        """Return the number of matching octets if route is a prefix of destination, else 0."""
        route_parts = route.split('.')
        dest_parts = destination.split('.')
        match_len = 0
        for r, d in zip(route_parts, dest_parts):
            if r == d:
                match_len += 1
            else:
                break
        return match_len if match_len == len(route_parts) else 0
    
    def lookup_route(self, destination: str) -> Optional[Dict]:
        """Look up the best route for a destination."""
        best_match = None
        best_length = 0
        for route in self.routes.inorder_traversal():
            match_len = self._is_prefix_match(route, destination)
            if match_len > best_length:
                best_length = match_len
                best_match = route
        if best_match:
            return self.route_data[best_match]
        return None
    
    def remove_route(self, destination: str) -> bool:
        """Remove a routing entry."""
        if destination not in self.route_data:
            return False
        
        self.routes.delete(destination)
        del self.route_data[destination]
        return True
    
    def get_all_routes(self) -> List[Tuple[str, Dict]]:
        """Get all routing entries."""
        return [(route, self.route_data[route]) 
                for route in self.routes.inorder_traversal()]
    
    def update_metric(self, destination: str, new_metric: int) -> bool:
        """Update the metric for a route."""
        if destination not in self.route_data:
            return False
        
        self.route_data[destination]['metric'] = new_metric
        return True 