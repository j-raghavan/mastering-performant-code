"""
File System Tree implementation for Chapter 6.

This module demonstrates how BST principles can be applied to real-world
hierarchical data structures like file systems.
"""

import os
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class FileNode:
    """Represents a file or directory in the file system."""
    name: str
    path: str
    is_directory: bool
    size: int
    modified_time: datetime
    children: Optional[List['FileNode']] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    def get_total_size(self) -> int:
        """Get the total size including all children."""
        total = self.size
        for child in self.children:
            total += child.get_total_size()
        return total
    
    def get_file_count(self) -> int:
        """Get the number of files (not directories) in this subtree."""
        if not self.is_directory:
            return 1
        
        count = 0
        for child in self.children:
            count += child.get_file_count()
        return count
    
    def get_directory_count(self) -> int:
        """Get the number of directories in this subtree."""
        if not self.is_directory:
            return 0
        
        count = 1  # Count this directory
        for child in self.children:
            count += child.get_directory_count()
        return count
    
    def find_files_by_extension(self, extension: str) -> List['FileNode']:
        """Find all files with the given extension in this subtree."""
        result = []
        
        if not self.is_directory:
            if self.name.endswith(extension):
                result.append(self)
        else:
            for child in self.children:
                result.extend(child.find_files_by_extension(extension))
        
        return result
    
    def get_largest_files(self, count: int = 10) -> List['FileNode']:
        """Get the largest files in this subtree."""
        all_files = []
        self._collect_files(all_files)
        
        # Sort by size in descending order
        all_files.sort(key=lambda x: x.size, reverse=True)
        return all_files[:count]
    
    def _collect_files(self, files: List['FileNode']) -> None:
        """Collect all files in this subtree."""
        if not self.is_directory:
            files.append(self)
        else:
            for child in self.children:
                child._collect_files(files)
    
    def __repr__(self) -> str:
        node_type = "DIR" if self.is_directory else "FILE"
        return f"FileNode({self.name}, {node_type}, {self.size} bytes)"

class FileSystemTree:
    """
    A file system tree implementation using BST concepts.
    
    This demonstrates how BST principles can be applied to real-world
    hierarchical data structures.
    """
    
    def __init__(self, root_path: str):
        self.root_path = root_path
        self.root = self._build_tree(root_path)
    
    def _build_tree(self, path: str) -> Optional[FileNode]:
        """Build a tree representation of the file system."""
        if not os.path.exists(path):
            return None
        
        try:
            stat = os.stat(path)
            name = os.path.basename(path)
            is_directory = os.path.isdir(path)
            
            node = FileNode(
                name=name,
                path=path,
                is_directory=is_directory,
                size=stat.st_size,
                modified_time=datetime.fromtimestamp(stat.st_mtime)
            )
            
            if is_directory:
                try:
                    children = []
                    for child_name in sorted(os.listdir(path)):
                        child_path = os.path.join(path, child_name)
                        child_node = self._build_tree(child_path)
                        if child_node:
                            children.append(child_node)
                    node.children = children
                except PermissionError:
                    pass  # Skip directories we can't access
            
            return node
        except (PermissionError, OSError):
            return None
    
    def search_file(self, filename: str) -> List[FileNode]:
        """Search for files with a given name."""
        results = []
        self._search_recursive(self.root, filename, results)
        return results
    
    def _search_recursive(self, node: Optional[FileNode], filename: str, results: List[FileNode]) -> None:
        """Recursively search for files."""
        if node is None:
            return
        
        if node.name == filename:
            results.append(node)
        
        if node.children:
            for child in node.children:
                self._search_recursive(child, filename, results)
    
    def get_directory_size(self, path: str) -> int:
        """Calculate the total size of a directory."""
        node = self._find_node_by_path(path)
        if node is None:
            return 0
        return node.get_total_size()
    
    def _find_node_by_path(self, path: str) -> Optional[FileNode]:
        """Find a node by its path."""
        if self.root and self.root.path == path:
            return self.root
        
        def find_recursive(node: Optional[FileNode], target_path: str) -> Optional[FileNode]:
            if node is None:
                return None
            
            if node.path == target_path:
                return node
            
            if node.children:
                for child in node.children:
                    result = find_recursive(child, target_path)
                    if result:
                        return result
            
            return None
        
        return find_recursive(self.root, path)
    
    def list_files_by_extension(self, extension: str) -> List[FileNode]:
        """List all files with a given extension."""
        if self.root is None:
            return []
        return self.root.find_files_by_extension(extension)
    
    def get_largest_files(self, count: int = 10) -> List[FileNode]:
        """Get the largest files in the tree."""
        if self.root is None:
            return []
        return self.root.get_largest_files(count)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the file system tree."""
        if self.root is None:
            return {
                "total_size": 0,
                "file_count": 0,
                "directory_count": 0,
                "total_items": 0,
                "average_file_size": 0,
                "largest_file": None,
                "smallest_file": None
            }
        
        total_size = self.root.get_total_size()
        file_count = self.root.get_file_count()
        directory_count = self.root.get_directory_count()
        total_items = file_count + directory_count
        
        # Find largest and smallest files
        all_files = []
        self.root._collect_files(all_files)
        
        largest_file = max(all_files, key=lambda x: x.size) if all_files else None
        smallest_file = min(all_files, key=lambda x: x.size) if all_files else None
        
        average_file_size = total_size / file_count if file_count > 0 else 0
        
        return {
            "total_size": total_size,
            "file_count": file_count,
            "directory_count": directory_count,
            "total_items": total_items,
            "average_file_size": average_file_size,
            "largest_file": largest_file,
            "smallest_file": smallest_file
        }
    
    def print_tree(self, node: Optional[FileNode] = None, prefix: str = "", is_last: bool = True) -> None:
        """Print a tree representation of the file system."""
        if node is None:
            node = self.root
            if node is None:
                print("Empty tree")
                return
        
        # Print current node
        connector = "└── " if is_last else "├── "
        size_str = f" ({self._format_size(node.size)})" if not node.is_directory else "/"
        print(f"{prefix}{connector}{node.name}{size_str}")
        
        # Print children
        if node.children:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(node.children):
                is_last_child = i == len(node.children) - 1
                self.print_tree(child, new_prefix, is_last_child)
    
    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_directory_structure(self, max_depth: int = 3) -> Dict[str, Any]:
        """Get a structured representation of the directory hierarchy."""
        if self.root is None:
            return {}
        
        def build_structure(node: FileNode, depth: int) -> Dict[str, Any]:
            if depth > max_depth:
                return {"type": "truncated", "name": node.name}
            
            structure = {
                "name": node.name,
                "type": "directory" if node.is_directory else "file",
                "size": node.size,
                "modified_time": node.modified_time.isoformat()
            }
            
            if node.is_directory and node.children:
                structure["children"] = [
                    build_structure(child, depth + 1) 
                    for child in node.children
                ]
            
            return structure
        
        return build_structure(self.root, 0)
    
    def find_duplicate_files(self) -> Dict[str, List[FileNode]]:
        """Find files with the same size (potential duplicates)."""
        if self.root is None:
            return {}
        
        all_files = []
        self.root._collect_files(all_files)
        
        # Group files by size
        size_groups = {}
        for file_node in all_files:
            size = file_node.size
            if size not in size_groups:
                size_groups[size] = []
            size_groups[size].append(file_node)
        
        # Return only groups with multiple files
        return {size: files for size, files in size_groups.items() if len(files) > 1}
    
    def get_oldest_files(self, count: int = 10) -> List[FileNode]:
        """Get the oldest files in the tree."""
        if self.root is None:
            return []
        
        all_files = []
        self.root._collect_files(all_files)
        
        # Sort by modification time (oldest first)
        all_files.sort(key=lambda x: x.modified_time)
        return all_files[:count]
    
    def get_newest_files(self, count: int = 10) -> List[FileNode]:
        """Get the newest files in the tree."""
        if self.root is None:
            return []
        
        all_files = []
        self.root._collect_files(all_files)
        
        # Sort by modification time (newest first)
        all_files.sort(key=lambda x: x.modified_time, reverse=True)
        return all_files[:count]
    
    def search_by_pattern(self, pattern: str, case_sensitive: bool = True) -> List[FileNode]:
        """Search for files matching a pattern."""
        if self.root is None:
            return []
        
        results = []
        self._search_pattern_recursive(self.root, pattern, case_sensitive, results)
        return results
    
    def _search_pattern_recursive(self, node: FileNode, pattern: str, case_sensitive: bool, results: List[FileNode]) -> None:
        """Recursively search for files matching a pattern."""
        if not node.is_directory:
            name = node.name if case_sensitive else node.name.lower()
            pattern = pattern if case_sensitive else pattern.lower()
            
            if pattern in name:
                results.append(node)
        
        if node.children:
            for child in node.children:
                self._search_pattern_recursive(child, pattern, case_sensitive, results)
    
    def get_memory_usage(self) -> int:
        """Calculate the memory usage of this tree structure."""
        if self.root is None:
            return 0
        
        def calculate_node_memory(node: FileNode) -> int:
            # Approximate memory usage for a FileNode
            node_memory = (
                sys.getsizeof(node.name) +
                sys.getsizeof(node.path) +
                sys.getsizeof(node.size) +
                sys.getsizeof(node.modified_time) +
                sys.getsizeof(node.children)
            )
            
            # Add memory for children
            for child in node.children:
                node_memory += calculate_node_memory(child)
            
            return node_memory
        
        return calculate_node_memory(self.root) 