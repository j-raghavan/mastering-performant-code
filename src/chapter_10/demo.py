"""
Trie Demo and Benchmarking

This module provides demonstrations and benchmarking tools for trie implementations,
including performance comparisons and real-world application examples.
"""

import timeit
import random
import string
from typing import List, Dict, Any

# Try relative imports for local execution
try:
    from .trie import Trie
    from .compressed_trie import CompressedTrie
    from .unicode_trie import UnicodeTrie
    from .autocomplete import AutocompleteSystem
    from .spell_checker import SpellChecker
    from .analyzer import TrieAnalyzer
except ImportError:
    # Fallback for running from project root
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from chapter_10.trie import Trie
    from chapter_10.compressed_trie import CompressedTrie
    from chapter_10.unicode_trie import UnicodeTrie
    from chapter_10.autocomplete import AutocompleteSystem
    from chapter_10.spell_checker import SpellChecker
    from chapter_10.analyzer import TrieAnalyzer

def generate_words(num_words: int, min_length: int = 3, max_length: int = 10) -> List[str]:
    """Generate random words for testing."""
    words = []
    for _ in range(num_words):
        length = random.randint(min_length, max_length)
        word = ''.join(random.choices(string.ascii_lowercase, k=length))
        words.append(word)
    return words

def benchmark_trie_performance():
    """Benchmark trie performance against other data structures."""
    test_words = generate_words(1000)
    test_prefixes = [word[:3] for word in test_words[:100]]
    
    # Test data structures
    structures = {
        'Standard Trie': Trie(),
        'Compressed Trie': CompressedTrie(),
        'Unicode Trie': UnicodeTrie(),
        'Python Set': set(),
        'Python Dict': {}
    }
    
    print("Performance Benchmark Results:")
    print("=" * 50)
    
    for name, structure in structures.items():
        print(f"\n{name}:")
        
        # Insert benchmark
        if hasattr(structure, 'insert'):
            insert_time = timeit.timeit(
                lambda: [structure.insert(word) for word in test_words[:100]],
                number=1
            )
            print(f"  Insert 100 words: {insert_time:.6f} seconds")
        
        # Search benchmark
        if hasattr(structure, 'search'):
            search_time = timeit.timeit(
                lambda: [structure.search(word) for word in test_words[:100]],
                number=1
            )
            print(f"  Search 100 words: {search_time:.6f} seconds")
        
        # Prefix search benchmark
        if hasattr(structure, 'starts_with'):
            prefix_time = timeit.timeit(
                lambda: [structure.starts_with(prefix) for prefix in test_prefixes],
                number=1
            )
            print(f"  Prefix search 100 prefixes: {prefix_time:.6f} seconds")
        
        # Memory usage
        if hasattr(structure, '_root'):
            memory = sys.getsizeof(structure)
            print(f"  Memory usage: {memory} bytes")

def demonstrate_real_world_applications():
    """Demonstrate real-world applications of tries."""
    print("\nReal-World Applications:")
    print("=" * 30)
    
    # 1. Autocomplete System
    print("\n1. Autocomplete System:")
    autocomplete = AutocompleteSystem()
    
    # Add some words with frequencies
    words_with_freq = [
        ("python", 100), ("programming", 80), ("data", 90),
        ("structure", 70), ("algorithm", 85), ("computer", 75),
        ("science", 95), ("software", 88), ("development", 92),
        ("database", 78), ("network", 82), ("system", 87)
    ]
    
    for word, freq in words_with_freq:
        autocomplete.add_word(word, freq)
    
    suggestions = autocomplete.get_suggestions("pro", 5)
    print(f"  Suggestions for 'pro': {suggestions}")
    
    # 2. Spell Checker
    print("\n2. Spell Checker:")
    dictionary = [
        "python", "programming", "data", "structure", "algorithm",
        "computer", "science", "software", "development", "database"
    ]
    
    spell_checker = SpellChecker(dictionary)
    
    test_words = ["pythn", "progrmming", "dta", "structre"]
    for word in test_words:
        is_correct = spell_checker.is_correct(word)
        suggestions = spell_checker.get_suggestions(word)
        print(f"  '{word}': {'✓' if is_correct else '✗'} -> {suggestions}")
    
    # 3. Unicode Handling
    print("\n3. Unicode Handling:")
    unicode_trie = UnicodeTrie(normalize=True, case_sensitive=False)
    
    unicode_words = ["café", "CAFÉ", "naïve", "naive", "résumé", "resume"]
    for word in unicode_words:
        unicode_trie.insert(word)
    
    print(f"  'cafe' in trie: {unicode_trie.search('cafe')}")
    print(f"  'CAFE' in trie: {unicode_trie.search('CAFE')}")
    print(f"  'naive' in trie: {unicode_trie.search('naive')}")

def analyze_memory_usage():
    """Analyze memory usage of different trie implementations."""
    # Test data
    words = [
        "python", "programming", "data", "structure", "algorithm",
        "computer", "science", "software", "development", "database",
        "network", "system", "application", "interface", "database",
        "query", "optimization", "performance", "memory", "efficiency"
    ]
    
    # Create tries
    standard_trie = Trie()
    compressed_trie = CompressedTrie()
    unicode_trie = UnicodeTrie()
    
    # Insert words
    for word in words:
        standard_trie.insert(word)
        compressed_trie.insert(word)
        unicode_trie.insert(word)
    
    # Analyze memory usage
    analyzer = TrieAnalyzer()
    
    std_stats = analyzer.analyze_trie(standard_trie)
    comp_stats = analyzer.analyze_compressed_trie(compressed_trie)
    
    print("Memory Usage Analysis:")
    print("=" * 30)
    print(f"Standard Trie:")
    print(f"  Nodes: {std_stats.num_nodes}")
    print(f"  Memory: {std_stats.memory_bytes} bytes")
    print(f"  Compression ratio: {std_stats.compression_ratio:.2f}")
    
    print(f"\nCompressed Trie:")
    print(f"  Nodes: {comp_stats.num_nodes}")
    print(f"  Memory: {comp_stats.memory_bytes} bytes")
    print(f"  Compression ratio: {comp_stats.compression_ratio:.2f}")
    print(f"  Memory savings: {(1 - comp_stats.compression_ratio) * 100:.1f}%")

def demonstrate_ip_routing():
    """Demonstrate IP routing using trie."""
    print("\n4. IP Routing Example:")
    
    class IPRouter:
        """Simple IP router using trie for longest prefix matching."""
        
        def __init__(self):
            self._trie = Trie[str]()  # Store next-hop information
        
        def add_route(self, prefix: str, next_hop: str):
            """Add a routing entry."""
            self._trie.insert(prefix, next_hop)
        
        def route_packet(self, ip_address: str) -> str:
            """Find the best matching route for an IP address."""
            # Find the longest matching prefix
            best_match = None
            best_length = 0
            
            for i in range(1, len(ip_address) + 1):
                prefix = ip_address[:i]
                if self._trie.starts_with(prefix):
                    if len(prefix) > best_length:
                        best_length = len(prefix)
                        best_match = self._trie.search(prefix)
            
            return best_match or "default"
    
    # Example usage
    router = IPRouter()
    router.add_route("192.168.1.0/24", "eth0")
    router.add_route("192.168.0.0/16", "eth1")
    router.add_route("0.0.0.0/0", "default")
    
    test_ips = ["192.168.1.100", "192.168.2.50", "10.0.0.1"]
    for ip in test_ips:
        next_hop = router.route_packet(ip)
        print(f"  {ip} -> {next_hop}")

def demonstrate_dna_analysis():
    """Demonstrate DNA sequence analysis using trie."""
    print("\n5. DNA Sequence Analysis:")
    
    class DNAAnalyzer:
        """DNA sequence analyzer using trie."""
        
        def __init__(self):
            self._trie = Trie[int]()  # Store sequence frequency
        
        def add_sequence(self, sequence: str):
            """Add a DNA sequence to the analyzer."""
            # Add all possible k-mers
            k = 3  # k-mer length
            for i in range(len(sequence) - k + 1):
                kmer = sequence[i:i+k]
                current_freq = self._trie.search(kmer) or 0
                self._trie.insert(kmer, current_freq + 1)
        
        def find_common_patterns(self, min_frequency: int = 2) -> List[tuple]:
            """Find common DNA patterns."""
            all_kmers = self._trie.get_all_strings()
            return [(kmer, freq) for kmer, freq in all_kmers if freq >= min_frequency]
    
    # Example usage
    dna_analyzer = DNAAnalyzer()
    sequences = ["ATCGATCG", "GCTAGCTA", "ATCGATCG"]
    for seq in sequences:
        dna_analyzer.add_sequence(seq)
    
    common_patterns = dna_analyzer.find_common_patterns(min_frequency=2)
    print(f"  Common DNA patterns: {common_patterns}")

if __name__ == "__main__":
    # Run benchmarks
    benchmark_trie_performance()
    
    # Demonstrate applications
    demonstrate_real_world_applications()
    
    # Analyze memory usage
    analyze_memory_usage()
    
    # Demonstrate IP routing
    demonstrate_ip_routing()
    
    # Demonstrate DNA analysis
    demonstrate_dna_analysis() 