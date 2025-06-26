"""
Profiling utilities for analyzing Python code performance.

This module provides tools for measuring execution time, memory usage,
and algorithmic complexity of Python functions and algorithms.
"""

import time
import timeit
import sys
import cProfile
import pstats
import io
import dis
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from contextlib import contextmanager
import statistics

# Try to import psutil, but don't fail if it's not available
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False


@dataclass
class ProfilingResult:
    """Result of a profiling operation."""
    function_name: str
    execution_time: float
    memory_usage: int
    call_count: int
    complexity_estimate: str
    details: Dict[str, Any]


class PerformanceProfiler:
    """
    A comprehensive profiler for measuring Python code performance.
    
    This class provides methods to measure execution time, analyze
    performance characteristics, and compare different implementations.
    """
    
    def __init__(self, number_of_runs: int = 1000):
        self.number_of_runs = number_of_runs
        self.results: Dict[str, ProfilingResult] = {}
    
    def time_function(self, func: Callable, *args, **kwargs) -> float:
        """
        Measure the execution time of a function.
        
        Args:
            func: The function to measure
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Average execution time in seconds
        """
        # Use timeit for accurate timing, but handle functions that might not be importable
        try:
            # Try the original approach first for functions that can be imported
            if hasattr(func, '__module__') and func.__module__ != '__main__':
                setup = f"from {func.__module__} import {func.__name__}"
                stmt = f"{func.__name__}(*{args}, **{kwargs})"
                return timeit.timeit(stmt, setup=setup, number=self.number_of_runs) / self.number_of_runs
            else:
                # For local functions or functions without proper module, use globals approach
                stmt = f"func(*{args}, **{kwargs})"
                return timeit.timeit(stmt, globals={'func': func}, number=self.number_of_runs) / self.number_of_runs
        except (ImportError, AttributeError, NameError):
            # Final fallback: use globals approach
            stmt = f"func(*{args}, **{kwargs})"
            return timeit.timeit(stmt, globals={'func': func}, number=self.number_of_runs) / self.number_of_runs
    
    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Profile a function using cProfile.
        
        Args:
            func: The function to profile
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Dictionary containing profiling statistics
        """
        profiler = cProfile.Profile()
        profiler.enable()
        
        try:
            result = func(*args, **kwargs)
        finally:
            profiler.disable()
        
        # Get profiling stats
        s = io.StringIO()
        stats = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        stats.print_stats(10)  # Top 10 functions
        
        return {
            'result': result,
            'stats': s.getvalue(),
            'total_calls': stats.total_calls,
            'total_time': stats.total_tt
        }
    
    def compare_functions(self, functions: Dict[str, Callable], 
                         *args, **kwargs) -> Dict[str, float]:
        """
        Compare the performance of multiple functions.
        
        Args:
            functions: Dictionary mapping function names to callables
            *args: Arguments to pass to all functions
            **kwargs: Keyword arguments to pass to all functions
            
        Returns:
            Dictionary mapping function names to execution times
        """
        results = {}
        
        for name, func in functions.items():
            try:
                execution_time = self.time_function(func, *args, **kwargs)
                results[name] = execution_time
            except Exception as e:
                results[name] = f"Error: {e}"
        
        return results
    
    def analyze_complexity(self, func: Callable, 
                          input_sizes: List[int]) -> Dict[str, Any]:
        """
        Analyze the time complexity of a function by measuring
        execution time across different input sizes.
        
        Args:
            func: The function to analyze
            input_sizes: List of input sizes to test
            
        Returns:
            Dictionary containing complexity analysis
        """
        times = []
        
        for size in input_sizes:
            try:
                execution_time = self.time_function(func, size)
                times.append((size, execution_time))
            except Exception as e:
                print(f"Error testing size {size}: {e}")
                continue
        
        if len(times) < 2:
            return {"error": "Insufficient data for complexity analysis"}
        
        # Calculate growth rate
        growth_rates = []
        for i in range(1, len(times)):
            size_ratio = times[i][0] / times[i-1][0]
            time_ratio = times[i][1] / times[i-1][1]
            growth_rates.append(time_ratio / size_ratio)
        
        avg_growth_rate = statistics.mean(growth_rates)
        
        # Estimate complexity
        if avg_growth_rate < 1.1:
            complexity = "O(1) - Constant"
        elif avg_growth_rate < 1.5:
            complexity = "O(log n) - Logarithmic"
        elif avg_growth_rate < 2.5:
            complexity = "O(n) - Linear"
        elif avg_growth_rate < 4.0:
            complexity = "O(n log n) - Linearithmic"
        elif avg_growth_rate < 8.0:
            complexity = "O(n²) - Quadratic"
        else:
            complexity = "O(n³) or higher - Polynomial"
        
        return {
            'input_sizes': [t[0] for t in times],
            'execution_times': [t[1] for t in times],
            'growth_rates': growth_rates,
            'average_growth_rate': avg_growth_rate,
            'estimated_complexity': complexity
        }


class MemoryProfiler:
    """
    A profiler for analyzing memory usage of Python objects and functions.
    """
    
    def __init__(self):
        self.baseline_memory = self._get_memory_usage()
    
    def _get_memory_usage(self) -> int:
        """Get current memory usage of the process."""
        try:
            # Check if psutil is available at runtime
            if 'psutil' in globals() and psutil is not None:
                process = psutil.Process()
                return process.memory_info().rss
            else:
                # Fallback to a simple approximation
                return 0
        except Exception:
            # Fallback to a simple approximation
            return 0
    
    def measure_object_memory(self, obj: Any) -> int:
        """
        Measure the memory usage of a Python object.
        
        Args:
            obj: The object to measure
            
        Returns:
            Memory usage in bytes
        """
        return sys.getsizeof(obj)
    
    def measure_function_memory(self, func: Callable, *args, **kwargs) -> Dict[str, int]:
        """
        Measure memory usage before and after function execution.
        
        Args:
            func: The function to measure
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Dictionary containing memory usage information
        """
        # Force garbage collection
        import gc
        gc.collect()
        
        memory_before = self._get_memory_usage()
        
        try:
            result = func(*args, **kwargs)
            memory_after = self._get_memory_usage()
            
            return {
                'memory_before': memory_before,
                'memory_after': memory_after,
                'memory_used': memory_after - memory_before,
                'result_size': sys.getsizeof(result) if result is not None else 0
            }
        except Exception as e:
            return {
                'error': str(e),
                'memory_before': memory_before,
                'memory_after': self._get_memory_usage()
            }
    
    def compare_data_structures(self, data_structures: Dict[str, Any]) -> Dict[str, int]:
        """
        Compare memory usage of different data structures.
        
        Args:
            data_structures: Dictionary mapping names to data structures
            
        Returns:
            Dictionary mapping names to memory usage
        """
        results = {}
        
        for name, data_structure in data_structures.items():
            results[name] = self.measure_object_memory(data_structure)
        
        return results


class ComplexityAnalyzer:
    """
    Analyzer for understanding algorithmic complexity and Big-O notation.
    """
    
    @staticmethod
    def analyze_loop_complexity(code: str) -> str:
        """
        Analyze the complexity of a simple loop structure.
        
        Args:
            code: String representation of the code
            
        Returns:
            Estimated complexity as a string
        """
        lines = code.split('\n')
        nested_loops = 0
        
        for line in lines:
            if any(keyword in line for keyword in ['for ', 'while ']):
                nested_loops += 1
        
        if nested_loops == 0:
            return "O(1) - Constant"
        elif nested_loops == 1:
            return "O(n) - Linear"
        elif nested_loops == 2:
            return "O(n²) - Quadratic"
        else:
            return f"O(n^{nested_loops}) - Polynomial"
    
    @staticmethod
    def disassemble_function(func: Callable) -> str:
        """
        Disassemble a function to show its bytecode.
        
        Args:
            func: The function to disassemble
            
        Returns:
            String representation of the bytecode
        """
        output = io.StringIO()
        dis.dis(func, file=output)
        return output.getvalue()
    
    @staticmethod
    def count_operations(func: Callable, *args, **kwargs) -> Dict[str, int]:
        """
        Count basic operations in a function (simplified analysis).
        
        Args:
            func: The function to analyze
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Dictionary containing operation counts
        """
        # This is a simplified approach - in practice, you'd need
        # more sophisticated static analysis
        operations = {
            'arithmetic': 0,
            'comparisons': 0,
            'function_calls': 0,
            'loops': 0
        }
        
        # Get bytecode
        bytecode = dis.Bytecode(func)
        
        for instruction in bytecode:
            if instruction.opname in ['BINARY_ADD', 'BINARY_SUBTRACT', 'BINARY_MULTIPLY', 'BINARY_DIVIDE']:
                operations['arithmetic'] += 1
            elif instruction.opname in ['COMPARE_OP']:
                operations['comparisons'] += 1
            elif instruction.opname in ['CALL_FUNCTION', 'CALL_METHOD']:
                operations['function_calls'] += 1
            elif instruction.opname in ['GET_ITER', 'FOR_ITER']:
                operations['loops'] += 1
        
        return operations


class BenchmarkSuite:
    """
    A comprehensive benchmark suite for comparing different implementations.
    """
    
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations
        self.performance_profiler = PerformanceProfiler(iterations)
        self.memory_profiler = MemoryProfiler()
        self.complexity_analyzer = ComplexityAnalyzer()
    
    def run_benchmark(self, name: str, functions: Dict[str, Callable], 
                     *args, **kwargs) -> Dict[str, Any]:
        """
        Run a comprehensive benchmark on multiple functions.
        
        Args:
            name: Name of the benchmark
            functions: Dictionary mapping function names to callables
            *args: Arguments to pass to all functions
            **kwargs: Keyword arguments to pass to all functions
            
        Returns:
            Dictionary containing benchmark results
        """
        results = {
            'name': name,
            'performance': {},
            'memory': {},
            'complexity': {}
        }
        
        # Performance benchmark
        results['performance'] = self.performance_profiler.compare_functions(
            functions, *args, **kwargs
        )
        
        # Memory benchmark (for first function only)
        if functions:
            first_func = next(iter(functions.values()))
            results['memory'] = self.memory_profiler.measure_function_memory(
                first_func, *args, **kwargs
            )
        
        # Complexity analysis (for first function only)
        if functions:
            first_func = next(iter(functions.values()))
            results['complexity'] = self.complexity_analyzer.count_operations(
                first_func, *args, **kwargs
            )
        
        return results
    
    def print_results(self, results: Dict[str, Any]) -> None:
        """
        Print benchmark results in a formatted way.
        
        Args:
            results: Results from run_benchmark
        """
        print(f"\n=== {results['name']} Benchmark Results ===")
        
        print("\nPerformance (execution time):")
        for func_name, time_result in results['performance'].items():
            if isinstance(time_result, float):
                print(f"  {func_name}: {time_result:.6f} seconds")
            else:
                print(f"  {func_name}: {time_result}")
        
        if 'memory' in results and 'memory_used' in results['memory']:
            print(f"\nMemory Usage: {results['memory']['memory_used']} bytes")
        
        if 'complexity' in results:
            print("\nOperation Counts:")
            for op_type, count in results['complexity'].items():
                print(f"  {op_type}: {count}")
        
        print("=" * 50)


@contextmanager
def timer(name: str = "Operation"):
    """
    Context manager for timing code blocks.
    
    Args:
        name: Name of the operation being timed
    """
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{name} took {end_time - start_time:.6f} seconds")


def quick_benchmark(func: Callable, *args, iterations: int = 1000, **kwargs) -> float:
    """
    Quick benchmark of a single function.
    
    Args:
        func: Function to benchmark
        *args: Arguments to pass to the function
        iterations: Number of iterations to run
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Average execution time in seconds
    """
    return timeit.timeit(lambda: func(*args, **kwargs), number=iterations) / iterations 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running profiler demonstration...")
    print("=" * 50)

    # Create instance of PerformanceProfiler
    try:
        instance = PerformanceProfiler()
        print(f"✓ Created PerformanceProfiler instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating PerformanceProfiler instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
