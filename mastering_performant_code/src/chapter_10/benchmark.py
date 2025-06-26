"""
Enhanced Benchmarking Module for Trie Implementations

This module provides comprehensive benchmarking capabilities including:
- Memory profiling with tracemalloc
- Scalability analysis across different data sizes
- Baseline comparisons with Python built-ins
- Visual performance charts
- Real-time performance monitoring
"""

import timeit
import tracemalloc
import random
import string
import statistics
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

from chapter_10.trie import Trie
from chapter_10.compressed_trie import CompressedTrie
from chapter_10.unicode_trie import UnicodeTrie
from chapter_10.autocomplete import AutocompleteSystem

@dataclass
class BenchmarkResult:
    """Container for benchmark results."""
    operation: str
    data_size: int
    time_seconds: float
    memory_bytes: int
    memory_peak_bytes: int
    structure_name: str

@dataclass
class PerformanceComparison:
    """Container for performance comparison results."""
    structure_name: str
    insert_times: List[float]
    search_times: List[float]
    prefix_times: List[float]
    memory_usage: List[int]
    compression_ratio: float

class TrieBenchmarker:
    """
    Comprehensive benchmarking system for trie implementations.
    
    Provides detailed performance analysis including memory profiling,
    scalability testing, and comparison with Python built-ins.
    """
    
    def __init__(self):
        """Initialize the benchmarker."""
        self.results: List[BenchmarkResult] = []
        self.comparisons: Dict[str, PerformanceComparison] = {}
    
    def generate_test_data(self, size: int, min_length: int = 3, max_length: int = 15) -> List[str]:
        """Generate test data of specified size."""
        words = []
        for _ in range(size):
            length = random.randint(min_length, max_length)
            word = ''.join(random.choices(string.ascii_lowercase, k=length))
            words.append(word)
        return words
    
    def benchmark_structure(self, structure_name: str, structure, 
                          test_data: List[str], operations: List[str]) -> List[BenchmarkResult]:
        """Benchmark a single data structure."""
        results = []
        
        for operation in operations:
            if operation == "insert":
                # Memory profiling for insert
                tracemalloc.start()
                start_time = timeit.default_timer()
                
                for word in test_data:
                    if hasattr(structure, 'insert'):
                        structure.insert(word)
                
                end_time = timeit.default_timer()
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                results.append(BenchmarkResult(
                    operation="insert",
                    data_size=len(test_data),
                    time_seconds=end_time - start_time,
                    memory_bytes=current,
                    memory_peak_bytes=peak,
                    structure_name=structure_name
                ))
            
            elif operation == "search":
                # Search benchmark
                start_time = timeit.default_timer()
                
                for word in test_data[:100]:  # Search subset for speed
                    if hasattr(structure, 'search'):
                        structure.search(word)
                
                end_time = timeit.default_timer()
                
                results.append(BenchmarkResult(
                    operation="search",
                    data_size=len(test_data),
                    time_seconds=end_time - start_time,
                    memory_bytes=0,  # No memory allocation for search
                    memory_peak_bytes=0,
                    structure_name=structure_name
                ))
            
            elif operation == "prefix":
                # Prefix search benchmark
                prefixes = [word[:3] for word in test_data[:50]]
                
                start_time = timeit.default_timer()
                
                for prefix in prefixes:
                    if hasattr(structure, 'starts_with'):
                        structure.starts_with(prefix)
                
                end_time = timeit.default_timer()
                
                results.append(BenchmarkResult(
                    operation="prefix",
                    data_size=len(test_data),
                    time_seconds=end_time - start_time,
                    memory_bytes=0,
                    memory_peak_bytes=0,
                    structure_name=structure_name
                ))
        
        return results
    
    def comprehensive_benchmark(self, data_sizes: List[int] = None) -> Dict[str, Any]:
        """
        Run comprehensive benchmarking across multiple data sizes.
        
        Args:
            data_sizes: List of data sizes to test
            
        Returns:
            Dictionary containing all benchmark results
        """
        if data_sizes is None:
            data_sizes = [100, 1000, 5000, 10000]
        
        all_results = []
        
        for size in data_sizes:
            print(f"Benchmarking with {size} words...")
            test_data = self.generate_test_data(size)
            
            # Test structures
            structures = {
                'Standard Trie': Trie(),
                'Compressed Trie': CompressedTrie(),
                'Unicode Trie': UnicodeTrie(),
                'Python Set': set(),
                'Python Dict': {}
            }
            
            for name, structure in structures.items():
                results = self.benchmark_structure(
                    name, structure, test_data, 
                    ["insert", "search", "prefix"]
                )
                all_results.extend(results)
        
        return self.analyze_results(all_results, data_sizes)
    
    def analyze_results(self, results: List[BenchmarkResult], 
                       data_sizes: List[int]) -> Dict[str, Any]:
        """Analyze and organize benchmark results."""
        analysis = {
            'summary': {},
            'by_structure': defaultdict(list),
            'by_operation': defaultdict(list),
            'scalability': {},
            'memory_analysis': {}
        }
        
        # Group results by structure
        for result in results:
            analysis['by_structure'][result.structure_name].append(result)
            analysis['by_operation'][result.operation].append(result)
        
        # Calculate scalability metrics
        for structure_name, structure_results in analysis['by_structure'].items():
            analysis['scalability'][structure_name] = self._calculate_scalability(
                structure_results, data_sizes
            )
        
        # Memory analysis
        analysis['memory_analysis'] = self._analyze_memory_usage(results)
        
        return analysis
    
    def _calculate_scalability(self, results: List[BenchmarkResult], 
                             data_sizes: List[int]) -> Dict[str, float]:
        """Calculate scalability metrics for a structure."""
        scalability = {}
        
        # Group by operation
        by_operation = defaultdict(list)
        for result in results:
            by_operation[result.operation].append(result)
        
        for operation, op_results in by_operation.items():
            if len(op_results) >= 2:
                # Calculate time complexity (approximate)
                times = [r.time_seconds for r in op_results]
                sizes = [r.data_size for r in op_results]
                
                # Simple linear regression for complexity estimation
                if len(times) >= 2:
                    # Calculate growth rate
                    growth_rates = []
                    for i in range(1, len(times)):
                        time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 0
                        size_ratio = sizes[i] / sizes[i-1] if sizes[i-1] > 0 else 0
                        if size_ratio > 0:
                            growth_rates.append(time_ratio / size_ratio)
                    
                    if growth_rates:
                        avg_growth = statistics.mean(growth_rates)
                        scalability[f'{operation}_complexity_factor'] = avg_growth
        
        return scalability
    
    def _analyze_memory_usage(self, results: List[BenchmarkResult]) -> Dict[str, Any]:
        """Analyze memory usage patterns."""
        memory_analysis = {
            'peak_usage': {},
            'compression_ratios': {},
            'memory_efficiency': {}
        }
        
        # Group by structure
        by_structure = defaultdict(list)
        for result in results:
            if result.operation == "insert":  # Only analyze insert operations
                by_structure[result.structure_name].append(result)
        
        for structure_name, structure_results in by_structure.items():
            if structure_results:
                peak_usage = [r.memory_peak_bytes for r in structure_results]
                memory_analysis['peak_usage'][structure_name] = {
                    'min': min(peak_usage),
                    'max': max(peak_usage),
                    'avg': statistics.mean(peak_usage),
                    'by_size': {r.data_size: r.memory_peak_bytes for r in structure_results}
                }
        
        # Calculate compression ratios
        if 'Standard Trie' in memory_analysis['peak_usage'] and 'Compressed Trie' in memory_analysis['peak_usage']:
            std_usage = memory_analysis['peak_usage']['Standard Trie']['avg']
            comp_usage = memory_analysis['peak_usage']['Compressed Trie']['avg']
            
            if std_usage > 0:
                compression_ratio = comp_usage / std_usage
                memory_analysis['compression_ratios']['compressed_vs_standard'] = {
                    'ratio': compression_ratio,
                    'savings_percent': (1 - compression_ratio) * 100
                }
        
        return memory_analysis
    
    def print_summary(self, analysis: Dict[str, Any]):
        """Print a comprehensive summary of benchmark results."""
        print("\n" + "="*60)
        print("COMPREHENSIVE BENCHMARK SUMMARY")
        print("="*60)
        
        # Memory analysis
        print("\n📊 MEMORY ANALYSIS:")
        print("-" * 30)
        if 'memory_analysis' in analysis:
            ma = analysis['memory_analysis']
            
            if 'peak_usage' in ma:
                print("Peak Memory Usage:")
                for structure, usage in ma['peak_usage'].items():
                    print(f"  {structure}: {usage['avg']/1024:.2f} KB avg")
            
            if 'compression_ratios' in ma:
                for ratio_name, ratio_data in ma['compression_ratios'].items():
                    print(f"\nCompression Analysis ({ratio_name}):")
                    print(f"  Compression ratio: {ratio_data['ratio']:.3f}")
                    print(f"  Memory savings: {ratio_data['savings_percent']:.1f}%")
        
        # Scalability analysis
        print("\n📈 SCALABILITY ANALYSIS:")
        print("-" * 30)
        if 'scalability' in analysis:
            for structure, metrics in analysis['scalability'].items():
                print(f"\n{structure}:")
                for metric, value in metrics.items():
                    print(f"  {metric}: {value:.4f}")
    
    def create_performance_charts(self, analysis: Dict[str, Any], 
                                save_path: Optional[str] = None):
        """Create visual performance charts."""
        try:
            import matplotlib.pyplot as plt
            
            # Memory usage chart
            if 'memory_analysis' in analysis and 'peak_usage' in analysis['memory_analysis']:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                
                # Memory usage by structure
                structures = []
                memory_usage = []
                
                for structure, usage in analysis['memory_analysis']['peak_usage'].items():
                    structures.append(structure)
                    memory_usage.append(usage['avg'] / 1024)  # Convert to KB
                
                ax1.bar(structures, memory_usage)
                ax1.set_title('Average Memory Usage by Structure')
                ax1.set_ylabel('Memory (KB)')
                ax1.tick_params(axis='x', rotation=45)
                
                # Compression ratio chart
                if 'compression_ratios' in analysis['memory_analysis']:
                    ratios = []
                    labels = []
                    
                    for ratio_name, ratio_data in analysis['memory_analysis']['compression_ratios'].items():
                        ratios.append(ratio_data['ratio'])
                        labels.append(ratio_name.replace('_', ' ').title())
                    
                    ax2.bar(labels, ratios)
                    ax2.set_title('Compression Ratios')
                    ax2.set_ylabel('Ratio (lower is better)')
                    ax2.tick_params(axis='x', rotation=45)
                
                plt.tight_layout()
                
                if save_path:
                    plt.savefig(save_path)
                else:
                    plt.show()
                
                plt.close()
                
        except ImportError:
            print("matplotlib not available. Skipping chart generation.")
    
    def benchmark_real_world_scenarios(self) -> Dict[str, Any]:
        """Benchmark real-world usage scenarios."""
        scenarios = {
            'autocomplete': self._benchmark_autocomplete(),
            'spell_checking': self._benchmark_spell_checking(),
            'dictionary_lookup': self._benchmark_dictionary_lookup()
        }
        return scenarios
    
    def _benchmark_autocomplete(self) -> Dict[str, Any]:
        """Benchmark autocomplete system performance."""
        # Load common English words
        common_words = [
            "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
            "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
            "this", "but", "his", "by", "from", "they", "we", "say", "her",
            "she", "or", "an", "will", "my", "one", "all", "would", "there",
            "their", "what", "so", "up", "out", "if", "about", "who", "get",
            "which", "go", "me", "when", "make", "can", "like", "time", "no",
            "just", "him", "know", "take", "people", "into", "year", "your",
            "good", "some", "could", "them", "see", "other", "than", "then",
            "now", "look", "only", "come", "its", "over", "think", "also",
            "back", "after", "use", "two", "how", "our", "work", "first",
            "well", "way", "even", "new", "want", "because", "any", "these",
            "give", "day", "most", "us"
        ]
        
        # Create autocomplete system
        autocomplete = AutocompleteSystem()
        for word in common_words:
            autocomplete.add_word(word, random.randint(1, 100))
        
        # Benchmark autocomplete suggestions
        prefixes = ["t", "th", "the", "a", "an", "and", "w", "wh", "what"]
        
        start_time = timeit.default_timer()
        for prefix in prefixes:
            autocomplete.get_suggestions(prefix, 10)
        end_time = timeit.default_timer()
        
        return {
            'total_time': end_time - start_time,
            'avg_time_per_prefix': (end_time - start_time) / len(prefixes),
            'words_loaded': len(common_words)
        }
    
    def _benchmark_spell_checking(self) -> Dict[str, Any]:
        """Benchmark spell checking performance."""
        # Create a simple spell checker using trie
        dictionary = [
            "python", "programming", "data", "structure", "algorithm",
            "computer", "science", "software", "development", "database",
            "network", "system", "application", "interface", "query",
            "optimization", "performance", "memory", "efficiency", "analysis"
        ]
        
        spell_checker_trie = Trie()
        for word in dictionary:
            spell_checker_trie.insert(word)
        
        # Test words (some correct, some incorrect)
        test_words = ["pythn", "progrmming", "dta", "structre", "python", 
                     "programming", "data", "structure", "algorithm"]
        
        start_time = timeit.default_timer()
        for word in test_words:
            spell_checker_trie.search(word)
        end_time = timeit.default_timer()
        
        return {
            'total_time': end_time - start_time,
            'avg_time_per_word': (end_time - start_time) / len(test_words),
            'dictionary_size': len(dictionary)
        }
    
    def _benchmark_dictionary_lookup(self) -> Dict[str, Any]:
        """Benchmark dictionary lookup performance."""
        # Compare trie vs Python dict
        words = self.generate_test_data(1000)
        
        # Build structures
        trie = Trie()
        py_dict = {}
        
        for word in words:
            trie.insert(word, word.upper())
            py_dict[word] = word.upper()
        
        # Benchmark lookups
        lookup_words = words[:100]
        
        # Trie lookup
        start_time = timeit.default_timer()
        for word in lookup_words:
            trie.search(word)
        trie_time = timeit.default_timer() - start_time
        
        # Dict lookup
        start_time = timeit.default_timer()
        for word in lookup_words:
            py_dict.get(word)
        dict_time = timeit.default_timer() - start_time
        
        return {
            'trie_lookup_time': trie_time,
            'dict_lookup_time': dict_time,
            'speedup_ratio': dict_time / trie_time if trie_time > 0 else 0,
            'words_loaded': len(words),
            'lookups_performed': len(lookup_words)
        }

def run_comprehensive_benchmark():
    """Run the complete benchmarking suite."""
    print("🚀 Starting Comprehensive Trie Benchmarking Suite")
    print("=" * 60)
    
    benchmarker = TrieBenchmarker()
    
    # Run comprehensive benchmark
    analysis = benchmarker.comprehensive_benchmark([100, 1000, 5000])
    
    # Print summary
    benchmarker.print_summary(analysis)
    
    # Create charts
    benchmarker.create_performance_charts(analysis, "trie_benchmark_results.png")
    
    # Run real-world scenarios
    print("\n🌍 REAL-WORLD SCENARIOS:")
    print("-" * 30)
    scenarios = benchmarker.benchmark_real_world_scenarios()
    
    for scenario_name, results in scenarios.items():
        print(f"\n{scenario_name.replace('_', ' ').title()}:")
        for metric, value in results.items():
            if isinstance(value, float):
                print(f"  {metric}: {value:.6f}")
            else:
                print(f"  {metric}: {value}")
    
    return analysis, scenarios

if __name__ == "__main__":
    run_comprehensive_benchmark() 