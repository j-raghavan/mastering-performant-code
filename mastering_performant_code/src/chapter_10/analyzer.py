"""
Trie Analyzer Implementation

This module provides tools to analyze the memory usage, performance,
and characteristics of trie implementations.
"""

import timeit
from typing import List, Dict, Any
from dataclasses import dataclass
from chapter_10.trie import Trie, TrieNode
from chapter_10.compressed_trie import CompressedTrie, CompressedTrieNode

@dataclass
class TrieStats:
    """Statistics about a trie's performance and memory usage."""
    num_nodes: int
    num_strings: int
    total_chars: int
    memory_bytes: int
    avg_string_length: float
    compression_ratio: float
    height: int

class TrieAnalyzer:
    """
    Analyzer for trie data structures.
    
    This class provides tools to analyze the memory usage, performance,
    and characteristics of trie implementations.
    """
    
    @staticmethod
    def analyze_trie(trie: Trie) -> TrieStats:
        """Analyze a standard trie."""
        def count_nodes(node: TrieNode) -> int:
            count = 1
            for child in node.children.values():
                count += count_nodes(child)
            return count
        
        def get_height(node: TrieNode) -> int:
            if not node.children:
                return 0
            return 1 + max(get_height(child) for child in node.children.values())
        
        num_nodes = count_nodes(trie._root)
        strings = trie.get_all_strings()
        total_chars = sum(len(s) for s, _ in strings)
        memory_bytes = num_nodes * 100  # Rough estimate
        
        return TrieStats(
            num_nodes=num_nodes,
            num_strings=len(strings),
            total_chars=total_chars,
            memory_bytes=memory_bytes,
            avg_string_length=total_chars / len(strings) if strings else 0,
            compression_ratio=1.0,  # No compression
            height=get_height(trie._root)
        )
    
    @staticmethod
    def analyze_compressed_trie(trie: CompressedTrie) -> TrieStats:
        """Analyze a compressed trie."""
        def count_nodes(node: CompressedTrieNode) -> int:
            count = 1
            for child in node.children.values():
                count += count_nodes(child)
            return count
        
        def get_height(node: CompressedTrieNode) -> int:
            if not node.children:
                return 0
            return 1 + max(get_height(child) for child in node.children.values())
        
        num_nodes = count_nodes(trie._root)
        strings = trie.get_all_strings()
        
        # Handle both tuple and string formats
        if strings and isinstance(strings[0], tuple):
            total_chars = sum(len(s) for s, _ in strings)
            num_strings = len(strings)
        else:
            total_chars = sum(len(s) for s in strings)
            num_strings = len(strings)
        
        memory_bytes = num_nodes * 30  # Rough estimate for compressed trie
        
        # Calculate compression ratio
        std_trie_nodes = total_chars  # Worst case for standard trie
        compression_ratio = num_nodes / std_trie_nodes if std_trie_nodes > 0 else 1.0
        
        return TrieStats(
            num_nodes=num_nodes,
            num_strings=num_strings,
            total_chars=total_chars,
            memory_bytes=memory_bytes,
            avg_string_length=total_chars / num_strings if num_strings > 0 else 0,
            compression_ratio=compression_ratio,
            height=get_height(trie._root)
        )
    
    @staticmethod
    def benchmark_operations(trie: Trie, operations: List[str], 
                           test_data: List[str], iterations: int = 1000) -> Dict[str, float]:
        """Benchmark common operations on a trie."""
        results = {}
        
        for operation in operations:
            if operation == "insert":
                # Create a fresh trie for each test
                test_trie = type(trie)()
                setup = ""
                stmt = "test_trie.insert('test_string')"
                globals_dict = {'test_trie': test_trie}
            elif operation == "search":
                # Create a trie with test data
                test_trie = type(trie)()
                for s in test_data:
                    test_trie.insert(s)
                setup = ""
                stmt = "test_trie.search('test_string')"
                globals_dict = {'test_trie': test_trie}
            elif operation == "prefix_search":
                # Create a trie with test data
                test_trie = type(trie)()
                for s in test_data:
                    test_trie.insert(s)
                setup = ""
                stmt = "test_trie.starts_with('test')"
                globals_dict = {'test_trie': test_trie}
            elif operation == "autocomplete":
                # Create a trie with test data
                test_trie = type(trie)()
                for s in test_data:
                    test_trie.insert(s)
                setup = ""
                stmt = "test_trie.autocomplete('test', 5)"
                globals_dict = {'test_trie': test_trie}
            else:
                continue
            
            try:
                time = timeit.timeit(stmt, setup=setup, number=iterations, globals=globals_dict)
                results[operation] = time
            except Exception:
                # Skip operations that fail
                continue
        
        return results
    
    @staticmethod
    def trie_memory_analysis(strings: List[str], alphabet_size: int = 256) -> Dict[str, float]:
        """
        Analyze trie memory usage for a given set of strings.
        
        Args:
            strings: List of strings to analyze
            alphabet_size: Size of the alphabet (256 for ASCII, 1,114,112 for Unicode)
            
        Returns:
            Dictionary containing memory analysis
        """
        if not strings:
            return {
                'num_strings': 0,
                'avg_length': 0,
                'total_chars': 0,
                'std_trie_nodes': 0,
                'compressed_trie_nodes': 0,
                'memory_savings': 0
            }
        
        n = len(strings)
        avg_length = sum(len(s) for s in strings) / n
        total_chars = sum(len(s) for s in strings)
        
        # Estimate standard trie nodes (worst case)
        std_trie_nodes = total_chars
        
        # Estimate compressed trie nodes (much fewer)
        # In practice, compression reduces nodes by 70-90%
        compressed_trie_nodes = int(std_trie_nodes * 0.2)  # 80% reduction
        
        # Memory savings
        memory_savings = (std_trie_nodes - compressed_trie_nodes) / std_trie_nodes * 100
        
        return {
            'num_strings': n,
            'avg_length': avg_length,
            'total_chars': total_chars,
            'std_trie_nodes': std_trie_nodes,
            'compressed_trie_nodes': compressed_trie_nodes,
            'memory_savings': memory_savings,
            'alphabet_size': alphabet_size,
            'std_memory_bytes': std_trie_nodes * 100,  # Rough estimate
            'compressed_memory_bytes': compressed_trie_nodes * 30  # Rough estimate
        } 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running analyzer demonstration...")
    print("=" * 50)

    # Create instance of TrieStats
    try:
        instance = TrieStats()
        print(f"✓ Created TrieStats instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating TrieStats instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
