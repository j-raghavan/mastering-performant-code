"""
Union-Find analyzer for performance analysis and benchmarking.

This module provides tools to analyze the performance and behavior
of Union-Find implementations.
"""

import timeit
from typing import Dict, List, Optional, Tuple, Type
from .optimized_disjoint_set import OptimizedDisjointSet


class UnionFindAnalyzer:
    """
    Analyzer for Union-Find data structures.
    
    This class provides tools to analyze the performance and behavior
    of Union-Find implementations.
    
    Features:
    - Benchmark operations across different sizes
    - Analyze tree structure and efficiency
    - Compare different implementations
    - Generate performance reports
    """
    
    @staticmethod
    def benchmark_operations(implementation_class: Type, operations: List[str], sizes: List[int]) -> Dict[str, Dict[int, float]]:
        """
        Benchmark Union-Find operations across different sizes.
        
        Args:
            implementation_class: Class of the Union-Find implementation to test
            operations: List of operations to benchmark ('make_set', 'find', 'union', 'connected')
            sizes: List of sizes to test
            
        Returns:
            Dictionary mapping operation names to dictionaries of size -> time
            
        Time Complexity: O(s * n * o) where s is number of sizes, n is size, o is number of operations
        """
        results = {}
        
        for operation in operations:
            results[operation] = {}
            
            for size in sizes:
                if operation == "make_set":
                    setup = f"from chapter_12 import {implementation_class.__name__}; ds = {implementation_class.__name__}()"
                    stmt = f"ds.make_set(i) for i in range({size})"
                elif operation == "find":
                    setup = f"from chapter_12 import {implementation_class.__name__}; ds = {implementation_class.__name__}(); [ds.make_set(i) for i in range({size})]"
                    stmt = f"ds.find(i) for i in range({size})"
                elif operation == "union":
                    setup = f"from chapter_12 import {implementation_class.__name__}; ds = {implementation_class.__name__}(); [ds.make_set(i) for i in range({size})]"
                    stmt = f"ds.union(i, (i+1)%{size}) for i in range({size})"
                elif operation == "connected":
                    setup = f"from chapter_12 import {implementation_class.__name__}; ds = {implementation_class.__name__}(); [ds.make_set(i) for i in range({size})]; [ds.union(i, (i+1)%{size}) for i in range({size})]"
                    stmt = f"ds.connected(i, (i+1)%{size}) for i in range({size})"
                else:
                    continue
                
                time = timeit.timeit(stmt, setup=setup, number=1)
                results[operation][size] = time
        
        return results
    
    @staticmethod
    def analyze_tree_structure(ds: OptimizedDisjointSet) -> Dict[str, float]:
        """
        Analyze the tree structure of the Union-Find data structure.
        
        Args:
            ds: OptimizedDisjointSet instance to analyze
            
        Returns:
            Dictionary containing tree structure metrics
            
        Time Complexity: O(n * α(n)) amortized
        """
        if not ds.parents:
            return {
                'avg_path_length': 0.0,
                'max_path_length': 0,
                'avg_set_size': 0.0,
                'max_set_size': 0,
                'num_sets': 0,
                'compression_efficiency': 1.0,
                'balance_factor': 1.0
            }
        
        # Calculate path lengths
        total_path_length = 0
        path_lengths = []
        
        for element in ds.parents:
            path_length = 0
            current = element
            while ds.parents[current] != current:
                current = ds.parents[current]
                path_length += 1
            total_path_length += path_length
            path_lengths.append(path_length)
        
        avg_path_length = total_path_length / len(ds.parents)
        max_path_length = max(path_lengths) if path_lengths else 0
        
        # Calculate tree balance
        sets = ds.get_sets()
        set_sizes = [len(s) for s in sets.values()]
        avg_set_size = sum(set_sizes) / len(set_sizes) if set_sizes else 0
        max_set_size = max(set_sizes) if set_sizes else 0
        
        # Calculate compression efficiency
        compression_efficiency = 1.0 - (avg_path_length / max_path_length) if max_path_length > 0 else 1.0
        
        # Calculate balance factor (ratio of largest to smallest set)
        balance_factor = max_set_size / min(set_sizes) if set_sizes and min(set_sizes) > 0 else 1.0
        
        return {
            'avg_path_length': avg_path_length,
            'max_path_length': max_path_length,
            'avg_set_size': avg_set_size,
            'max_set_size': max_set_size,
            'num_sets': len(sets),
            'compression_efficiency': compression_efficiency,
            'balance_factor': balance_factor
        }
    
    @staticmethod
    def compare_implementations(implementations: List[Type], operations: List[str], sizes: List[int]) -> Dict[str, Dict[str, Dict[int, float]]]:
        """
        Compare multiple Union-Find implementations.
        
        Args:
            implementations: List of Union-Find implementation classes
            operations: List of operations to benchmark
            sizes: List of sizes to test
            
        Returns:
            Dictionary mapping implementation names to operation results
            
        Time Complexity: O(i * s * n * o) where i is number of implementations
        """
        results = {}
        
        for impl_class in implementations:
            impl_name = impl_class.__name__
            results[impl_name] = UnionFindAnalyzer.benchmark_operations(impl_class, operations, sizes)
        
        return results
    
    @staticmethod
    def generate_performance_report(comparison_results: Dict[str, Dict[str, Dict[int, float]]]) -> str:
        """
        Generate a comprehensive performance report.
        
        Args:
            comparison_results: Results from compare_implementations
            
        Returns:
            Formatted performance report string
        """
        report = "Union-Find Performance Report\n"
        report += "=" * 50 + "\n\n"
        
        implementations = list(comparison_results.keys())
        operations = list(comparison_results[implementations[0]].keys()) if implementations else []
        sizes = list(comparison_results[implementations[0]][operations[0]].keys()) if operations else []
        
        for operation in operations:
            report += f"Operation: {operation}\n"
            report += "-" * 30 + "\n"
            
            for size in sizes:
                report += f"Size {size}:\n"
                times = []
                for impl in implementations:
                    time = comparison_results[impl][operation][size]
                    times.append((impl, time))
                    report += f"  {impl}: {time:.6f} seconds\n"
                
                # Find fastest implementation
                fastest = min(times, key=lambda x: x[1])
                report += f"  Fastest: {fastest[0]} ({fastest[1]:.6f}s)\n"
                
                # Calculate speedup ratios
                for impl, time in times:
                    if time > 0:
                        speedup = fastest[1] / time
                        report += f"  {impl} speedup: {speedup:.2f}x\n"
                
                report += "\n"
        
        return report
    
    @staticmethod
    def analyze_scalability(implementation_class: Type, max_size: int = 10000, step: int = 1000) -> Dict[str, List[float]]:
        """
        Analyze how performance scales with size.
        
        Args:
            implementation_class: Union-Find implementation class to test
            max_size: Maximum size to test
            step: Step size between tests
            
        Returns:
            Dictionary containing size and time data for plotting
            
        Time Complexity: O(max_size * max_size / step)
        """
        sizes = list(range(step, max_size + 1, step))
        operations = ['make_set', 'find', 'union']
        
        results = UnionFindAnalyzer.benchmark_operations(implementation_class, operations, sizes)
        
        scalability_data = {
            'sizes': sizes,
            'make_set_times': [results['make_set'][size] for size in sizes],
            'find_times': [results['find'][size] for size in sizes],
            'union_times': [results['union'][size] for size in sizes]
        }
        
        return scalability_data
    
    @staticmethod
    def calculate_complexity_ratios(implementation_class: Type, sizes: List[int]) -> Dict[str, List[float]]:
        """
        Calculate empirical complexity ratios to verify theoretical bounds.
        
        Args:
            implementation_class: Union-Find implementation class to test
            sizes: List of sizes to test
            
        Returns:
            Dictionary containing complexity ratios
            
        Time Complexity: O(len(sizes) * max(sizes))
        """
        operations = ['make_set', 'find', 'union']
        results = UnionFindAnalyzer.benchmark_operations(implementation_class, operations, sizes)
        
        ratios = {}
        
        for operation in operations:
            times = [results[operation][size] for size in sizes]
            ratios[operation] = []
            
            # Calculate ratios between consecutive sizes
            for i in range(1, len(times)):
                if times[i-1] > 0:
                    ratio = times[i] / times[i-1]
                    ratios[operation].append(ratio)
        
        return ratios
    
    @staticmethod
    def stress_test(implementation_class: Type, num_operations: int = 10000) -> Dict[str, float]:
        """
        Perform a stress test with random operations.
        
        Args:
            implementation_class: Union-Find implementation class to test
            num_operations: Number of random operations to perform
            
        Returns:
            Dictionary containing stress test results
            
        Time Complexity: O(num_operations * α(n)) amortized
        """
        import random
        
        ds = implementation_class()
        operations = []
        
        # Generate random operations
        for _ in range(num_operations):
            op_type = random.choice(['make_set', 'find', 'union'])
            if op_type == 'make_set':
                element = random.randint(0, num_operations // 10)
                operations.append(('make_set', element))
            elif op_type == 'find':
                if ds.parents:
                    element = random.choice(list(ds.parents.keys()))
                    operations.append(('find', element))
            elif op_type == 'union':
                if len(ds.parents) >= 2:
                    elements = random.sample(list(ds.parents.keys()), 2)
                    operations.append(('union', elements[0], elements[1]))
        
        # Execute operations and measure time
        start_time = timeit.default_timer()
        
        for op in operations:
            if op[0] == 'make_set':
                ds.make_set(op[1])
            elif op[0] == 'find':
                try:
                    ds.find(op[1])
                except ValueError:
                    pass  # Element not found
            elif op[0] == 'union':
                ds.union(op[1], op[2])
        
        end_time = timeit.default_timer()
        
        return {
            'total_time': end_time - start_time,
            'operations_per_second': num_operations / (end_time - start_time),
            'final_sets': ds.count_sets(),
            'final_elements': len(ds.parents)
        }
    
    @staticmethod
    def memory_efficiency_analysis(implementation_class: Type, sizes: List[int]) -> Dict[str, List[int]]:
        """
        Analyze memory efficiency across different sizes.
        
        Args:
            implementation_class: Union-Find implementation class to test
            sizes: List of sizes to test
            
        Returns:
            Dictionary containing memory usage data
            
        Time Complexity: O(len(sizes) * max(sizes))
        """
        memory_data = {
            'sizes': sizes,
            'memory_usage': []
        }
        
        for size in sizes:
            ds = implementation_class()
            
            # Add elements
            for i in range(size):
                ds.make_set(i)
            
            # Perform some unions
            for i in range(size - 1):
                ds.union(i, i + 1)
            
            # Measure memory usage
            if hasattr(ds, 'get_memory_info'):
                memory_info = ds.get_memory_info()
                memory_data['memory_usage'].append(memory_info.total_size)
            else:
                # Fallback to basic memory measurement
                memory_data['memory_usage'].append(sys.getsizeof(ds))
        
        return memory_data



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running analyzer demonstration...")
    print("=" * 50)

    # Create instance of UnionFindAnalyzer
    try:
        instance = UnionFindAnalyzer()
        print(f"✓ Created UnionFindAnalyzer instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating UnionFindAnalyzer instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
