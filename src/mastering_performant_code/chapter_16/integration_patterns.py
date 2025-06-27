"""
Integration patterns for Chapter 16.

This module demonstrates various patterns for integrating optimized code
into larger systems using only built-in Python modules.

SECURITY WARNING: The plugin system in this module loads and executes arbitrary
Python code. In production environments, this can be a significant security risk.
Consider implementing proper sandboxing, code validation, and permission controls
before using this in production systems.
"""

import importlib
import importlib.util
import subprocess
import time
import threading
import queue
import json
import pickle
import ast
import warnings
import sys
from typing import Any, Dict, List, Optional, Callable, TypeVar, Generic
from dataclasses import dataclass
from pathlib import Path
from contextlib import contextmanager


T = TypeVar('T')


@dataclass
class PluginInfo:
    """Information about a loaded plugin."""
    name: str
    version: str
    description: str
    functions: List[str]
    load_time: float
    security_validated: bool = False


class PluginSecurityValidator:
    """
    Basic security validator for plugin code.
    
    This provides basic validation to check for potentially dangerous
    operations in plugin code. Note that this is not a complete security
    solution and should be enhanced for production use.
    """
    
    DANGEROUS_IMPORTS = {
        'os', 'subprocess', 'sys', 'builtins', 'eval', 'exec',
        'open', 'file', 'input', 'raw_input'
    }
    
    DANGEROUS_FUNCTIONS = {
        'eval', 'exec', 'compile', 'input', 'raw_input',
        'open', 'file', 'globals', 'locals'
    }
    
    @classmethod
    def validate_plugin_code(cls, code: str) -> Dict[str, Any]:
        """
        Validate plugin code for potentially dangerous operations.
        
        Returns a dictionary with validation results and warnings.
        """
        warnings_list = []
        is_safe = True
        
        try:
            tree = ast.parse(code)
            
            # Check for dangerous imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name in cls.DANGEROUS_IMPORTS:
                            warnings_list.append(f"Dangerous import: {alias.name}")
                            is_safe = False
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module in cls.DANGEROUS_IMPORTS:
                        warnings_list.append(f"Dangerous import from: {node.module}")
                        is_safe = False
                
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in cls.DANGEROUS_FUNCTIONS:
                            warnings_list.append(f"Dangerous function call: {node.func.id}")
                            is_safe = False
                    elif isinstance(node.func, ast.Attribute):
                        if node.func.attr in cls.DANGEROUS_FUNCTIONS:
                            warnings_list.append(f"Dangerous method call: {node.func.attr}")
                            is_safe = False
            
            return {
                'is_safe': is_safe,
                'warnings': warnings_list,
                'validation_passed': True
            }
            
        except SyntaxError as e:
            return {
                'is_safe': False,
                'warnings': [f"Syntax error: {e}"],
                'validation_passed': False
            }
        except Exception as e:
            return {
                'is_safe': False,
                'warnings': [f"Validation error: {e}"],
                'validation_passed': False
            }


class PluginManager:
    """
    A plugin system for dynamically loading optimized modules.
    
    This demonstrates how to integrate optimized code as plugins
    that can be loaded at runtime without external dependencies.
    
    SECURITY WARNING: This plugin system loads and executes arbitrary Python code.
    In production environments, this can be a significant security risk.
    Always validate plugin code and consider implementing proper sandboxing.
    """
    
    def __init__(self, plugin_directory: str = "plugins", enable_security_validation: bool = True):
        self.plugin_directory = Path(plugin_directory)
        self.plugins: Dict[str, Any] = {}
        self.plugin_info: Dict[str, PluginInfo] = {}
        self.plugin_directory.mkdir(exist_ok=True)
        self.enable_security_validation = enable_security_validation
        
        if enable_security_validation:
            warnings.warn(
                "PluginManager is loading arbitrary Python code. "
                "This can be a security risk in production environments. "
                "Consider implementing proper sandboxing and code validation.",
                UserWarning
            )
    
    def register_plugin(self, name: str, module: Any, version: str = "1.0.0", 
                       description: str = "", security_validated: bool = False) -> None:
        """Register a plugin module."""
        start_time = time.time()
        
        # Extract available functions
        functions = [attr for attr in dir(module) 
                    if callable(getattr(module, attr)) and not attr.startswith('_')]
        
        self.plugins[name] = module
        self.plugin_info[name] = PluginInfo(
            name=name,
            version=version,
            description=description,
            functions=functions,
            load_time=time.time() - start_time,
            security_validated=security_validated
        )
    
    def load_plugin_from_file(self, file_path: str) -> Optional[str]:
        """
        Load a plugin from a Python file with optional security validation.
        
        Args:
            file_path: Path to the plugin file
            
        Returns:
            Plugin name if loaded successfully, None otherwise
            
        Raises:
            SecurityWarning: If dangerous operations are detected in the plugin code
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return None
            
            # Read and validate the plugin code if security validation is enabled
            if self.enable_security_validation:
                with open(file_path, 'r') as f:
                    code = f.read()
                
                validation_result = PluginSecurityValidator.validate_plugin_code(code)
                
                if not validation_result['is_safe']:
                    warnings.warn(
                        f"Plugin {file_path} contains potentially dangerous operations: "
                        f"{validation_result['warnings']}",
                        UserWarning
                    )
                    # In production, you might want to reject the plugin entirely
                    # raise SecurityWarning(f"Dangerous plugin code: {validation_result['warnings']}")
            
            # Load the module
            spec = importlib.util.spec_from_file_location(
                file_path.stem, file_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Register the plugin
            plugin_name = file_path.stem
            self.register_plugin(
                plugin_name, 
                module, 
                security_validated=self.enable_security_validation
            )
            
            return plugin_name
            
        except Exception as e:
            print(f"Failed to load plugin {file_path}: {e}")
            return None
    
    def get_plugin(self, name: str) -> Optional[Any]:
        """Get a loaded plugin by name."""
        return self.plugins.get(name)
    
    def list_plugins(self) -> List[PluginInfo]:
        """List all loaded plugins."""
        return list(self.plugin_info.values())
    
    def call_plugin_function(self, plugin_name: str, function_name: str, 
                           *args, **kwargs) -> Any:
        """
        Call a function from a specific plugin.
        
        SECURITY WARNING: This executes arbitrary code from the plugin.
        Ensure the plugin has been properly validated before calling.
        """
        plugin = self.get_plugin(plugin_name)
        if plugin is None:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        
        if not hasattr(plugin, function_name):
            raise ValueError(f"Function '{function_name}' not found in plugin '{plugin_name}'")
        
        # Check if plugin has been security validated
        plugin_info = self.plugin_info.get(plugin_name)
        if plugin_info and not plugin_info.security_validated:
            warnings.warn(
                f"Calling function from plugin '{plugin_name}' that has not been "
                f"security validated. This may be unsafe.",
                UserWarning
            )
        
        func = getattr(plugin, function_name)
        return func(*args, **kwargs)


class SubprocessOptimizer:
    """
    A subprocess-based optimizer for CPU-intensive tasks.
    
    This demonstrates how to use subprocesses to run optimized code
    in separate processes, avoiding GIL limitations.
    """
    
    def __init__(self, max_workers: int = 4):
        self.max_workers = max_workers
        self.processes: List[subprocess.Popen] = []
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
    
    def run_task_in_subprocess(self, script_content: str, 
                              input_data: Any = None) -> Any:
        """Run a task in a separate subprocess."""
        # Create a temporary script
        script = f"""
import sys
import json
import pickle

{script_content}

if __name__ == "__main__":
    # Read input from stdin
    input_data = pickle.loads(sys.stdin.buffer.read())
    result = main(input_data)
    # Write result to stdout
    sys.stdout.buffer.write(pickle.dumps(result))
"""
        
        # Run the subprocess
        process = subprocess.Popen(
            [sys.executable, '-c', script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Send input data
        input_bytes = pickle.dumps(input_data)
        stdout, stderr = process.communicate(input=input_bytes)
        
        if process.returncode != 0:
            raise RuntimeError(f"Subprocess failed: {stderr.decode()}")
        
        # Parse result
        result = pickle.loads(stdout)
        return result
    
    def run_parallel_tasks(self, tasks: List[tuple]) -> List[Any]:
        """Run multiple tasks in parallel subprocesses."""
        results = []
        
        for script_content, input_data in tasks:
            result = self.run_task_in_subprocess(script_content, input_data)
            results.append(result)
        
        return results


class ThreadSafeCache:
    """
    A thread-safe cache implementation for shared state.
    
    This demonstrates how to create thread-safe data structures
    for use in multi-threaded applications.
    """
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self._access_count: Dict[str, int] = {}
        self._last_access: Dict[str, float] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the cache."""
        with self._lock:
            if key in self._cache:
                self._access_count[key] = self._access_count.get(key, 0) + 1
                self._last_access[key] = time.time()
                return self._cache[key]
            return default
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the cache."""
        with self._lock:
            # If key already exists, just update it
            if key in self._cache:
                self._cache[key] = value
                self._access_count[key] = self._access_count.get(key, 0) + 1
                self._last_access[key] = time.time()
                return
            
            # If cache is full, evict least recently used item
            if len(self._cache) >= self.max_size:
                self._evict_lru_item()
            
            self._cache[key] = value
            self._access_count[key] = 0
            self._last_access[key] = time.time()
    
    def _evict_lru_item(self) -> None:
        """Evict the least recently used item from the cache."""
        if not self._cache:
            return
        
        # Find the least recently used item
        lru_key = min(self._last_access.keys(), 
                     key=lambda k: self._last_access.get(k, 0))
        
        # Remove the item
        del self._cache[lru_key]
        if lru_key in self._access_count:
            del self._access_count[lru_key]
        if lru_key in self._last_access:
            del self._last_access[lru_key]
    
    def clear(self) -> None:
        """Clear the cache."""
        with self._lock:
            self._cache.clear()
            self._access_count.clear()
            self._last_access.clear()
    
    def size(self) -> int:
        """Get the current size of the cache."""
        with self._lock:
            return len(self._cache)


class PerformanceMonitor:
    """
    A performance monitoring system for production integration.
    
    This demonstrates how to monitor performance metrics
    in production systems using only built-in modules.
    """
    
    def __init__(self):
        self.metrics: Dict[str, List[float]] = {}
        self.start_times: Dict[str, float] = {}
        self._lock = threading.Lock()
    
    @contextmanager
    def measure(self, metric_name: str):
        """Context manager for measuring execution time."""
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            self.record_metric(metric_name, end_time - start_time)
    
    def record_metric(self, metric_name: str, value: float) -> None:
        """Record a performance metric."""
        with self._lock:
            if metric_name not in self.metrics:
                self.metrics[metric_name] = []
            self.metrics[metric_name].append(value)
    
    def get_statistics(self, metric_name: str) -> Dict[str, float]:
        """Get statistics for a metric."""
        with self._lock:
            if metric_name not in self.metrics:
                return {}
            
            values = self.metrics[metric_name]
            if not values:
                return {}
            
            return {
                'count': len(values),
                'min': min(values),
                'max': max(values),
                'mean': sum(values) / len(values),
                'total': sum(values)
            }
    
    def export_metrics(self, format: str = 'json') -> str:
        """Export metrics in the specified format."""
        with self._lock:
            if format == 'json':
                return json.dumps(self.metrics, indent=2)
            elif format == 'csv':
                lines = ['metric,value']
                for metric, values in self.metrics.items():
                    for value in values:
                        lines.append(f'{metric},{value}')
                return '\n'.join(lines)
            else:
                raise ValueError(f"Unsupported format: {format}")


class OptimizedDataStructures:
    """
    Demonstrates optimization of data structures from previous chapters.
    
    This class shows how to apply performance optimization techniques
    from Chapter 16 to data structures covered in earlier chapters.
    """
    
    def __init__(self):
        self.performance_monitor = PerformanceMonitor()
    
    def optimized_bst_node(self):
        """
        Optimized Binary Search Tree node using __slots__.
        
        This demonstrates how to optimize the BST implementation from Chapter 6
        by using __slots__ to reduce memory overhead for large trees.
        """
        class OptimizedBSTNode:
            __slots__ = ('key', 'value', 'left', 'right', 'parent')
            
            def __init__(self, key, value=None):
                self.key = key
                self.value = value
                self.left = None
                self.right = None
                self.parent = None
        
        return OptimizedBSTNode
    
    def optimized_heap_node(self):
        """
        Optimized Heap node using __slots__.
        
        This demonstrates how to optimize the heap implementation from Chapter 11
        by using __slots__ for better memory efficiency.
        """
        class OptimizedHeapNode:
            __slots__ = ('value', 'priority', 'index')
            
            def __init__(self, value, priority=0):
                self.value = value
                self.priority = priority
                self.index = 0
        
        return OptimizedHeapNode
    
    def optimized_cache_entry(self):
        """
        Optimized cache entry using __slots__.
        
        This demonstrates how to optimize cache implementations from Chapter 15
        by using __slots__ for better memory efficiency in large caches.
        """
        class OptimizedCacheEntry:
            __slots__ = ('key', 'value', 'access_count', 'last_access', 'size')
            
            def __init__(self, key, value, size=0):
                self.key = key
                self.value = value
                self.access_count = 0
                self.last_access = time.time()
                self.size = size
            
            def update_access(self):
                """Update access statistics."""
                self.access_count += 1
                self.last_access = time.time()
        
        return OptimizedCacheEntry
    
    def benchmark_optimization_impact(self):
        """
        Benchmark the impact of optimizations on data structures.
        
        This demonstrates the performance improvements achieved by
        applying optimization techniques to data structures.
        """
        print("=== Data Structure Optimization Benchmark ===\n")
        
        # Test BST node optimization
        with self.performance_monitor.measure("bst_node_creation"):
            # Create many BST nodes
            nodes = []
            for i in range(10000):
                node = self.optimized_bst_node()(i, f"value_{i}")
                nodes.append(node)
        
        # Test heap node optimization
        with self.performance_monitor.measure("heap_node_creation"):
            # Create many heap nodes
            nodes = []
            for i in range(10000):
                node = self.optimized_heap_node()(i, i)
                nodes.append(node)
        
        # Test cache entry optimization
        with self.performance_monitor.measure("cache_entry_creation"):
            # Create many cache entries
            entries = []
            for i in range(10000):
                entry = self.optimized_cache_entry()(f"key_{i}", f"value_{i}", 100)
                entries.append(entry)
        
        # Get performance statistics
        stats = self.performance_monitor.get_statistics()
        for metric, data in stats.items():
            print(f"{metric}: {data['mean']:.6f} seconds (avg), {data['min']:.6f} seconds (min)")
    
    def demonstrate_memory_savings(self):
        """
        Demonstrate memory savings from optimizations.
        
        This shows the memory usage differences between regular and
        optimized versions of data structure nodes.
        """
        print("\n=== Memory Usage Comparison ===\n")
        
        # Regular BST node (without __slots__)
        class RegularBSTNode:
            def __init__(self, key, value=None):
                self.key = key
                self.value = value
                self.left = None
                self.right = None
                self.parent = None
        
        # Optimized BST node (with __slots__)
        OptimizedBSTNode = self.optimized_bst_node()
        
        # Create nodes and measure memory
        regular_nodes = [RegularBSTNode(i, f"value_{i}") for i in range(1000)]
        optimized_nodes = [OptimizedBSTNode(i, f"value_{i}") for i in range(1000)]
        
        regular_size = sum(sys.getsizeof(node) for node in regular_nodes)
        optimized_size = sum(sys.getsizeof(node) for node in optimized_nodes)
        
        print(f"Regular BST nodes: {regular_size} bytes")
        print(f"Optimized BST nodes: {optimized_size} bytes")
        print(f"Memory saved: {regular_size - optimized_size} bytes ({((regular_size - optimized_size) / regular_size * 100):.1f}%)")
    
    def run_optimization_demo(self):
        """
        Run a comprehensive demonstration of data structure optimizations.
        """
        print("=== Data Structure Optimization Demonstration ===\n")
        
        # Benchmark performance impact
        self.benchmark_optimization_impact()
        
        # Demonstrate memory savings
        self.demonstrate_memory_savings()
        
        print("\n=== Optimization Summary ===")
        print("✓ __slots__ reduces memory overhead for large data structures")
        print("✓ Performance improvements in object creation and access")
        print("✓ Better cache locality due to reduced memory footprint")
        print("✓ Applicable to all data structure implementations")


def demonstrate_integration_patterns():
    """Demonstrate various integration patterns."""
    
    # 1. Plugin System
    print("=== Plugin System Demo ===")
    plugin_manager = PluginManager()
    
    # Create a sample plugin
    sample_plugin_code = """
def optimized_sort(data):
    return sorted(data)

def optimized_filter(data, predicate):
    return [x for x in data if predicate(x)]

def get_plugin_info():
    return "Sample optimization plugin"
"""
    
    # Save plugin to file
    plugin_file = Path("plugins/sample_optimizer.py")
    plugin_file.parent.mkdir(exist_ok=True)
    plugin_file.write_text(sample_plugin_code)
    
    # Load the plugin
    plugin_name = plugin_manager.load_plugin_from_file(str(plugin_file))
    if plugin_name:
        print(f"Loaded plugin: {plugin_name}")
        print(f"Available functions: {plugin_manager.plugin_info[plugin_name].functions}")
        
        # Use the plugin
        data = [3, 1, 4, 1, 5, 9, 2, 6]
        sorted_data = plugin_manager.call_plugin_function(plugin_name, 'optimized_sort', data)
        print(f"Sorted data: {sorted_data}")
    
    # 2. Subprocess Optimization
    print("\n=== Subprocess Optimization Demo ===")
    optimizer = SubprocessOptimizer()
    
    subprocess_script = """
def main(data):
    # CPU-intensive task
    result = sum(x * x for x in range(data))
    return result
"""
    
    result = optimizer.run_task_in_subprocess(subprocess_script, 10000)
    print(f"Subprocess result: {result}")
    
    # 3. Thread-Safe Cache
    print("\n=== Thread-Safe Cache Demo ===")
    cache = ThreadSafeCache(max_size=5)
    
    def worker(worker_id: int):
        for i in range(10):
            key = f"key_{i}"
            value = f"value_{worker_id}_{i}"
            cache.set(key, value)
            retrieved = cache.get(key)
            print(f"Worker {worker_id}: {key} = {retrieved}")
    
    # Run multiple threads
    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    print(f"Final cache size: {cache.size()}")
    
    # 4. Performance Monitor
    print("\n=== Performance Monitor Demo ===")
    monitor = PerformanceMonitor()
    
    with monitor.measure("data_processing"):
        # Simulate some work
        time.sleep(0.1)
    
    with monitor.measure("data_processing"):
        time.sleep(0.05)
    
    stats = monitor.get_statistics("data_processing")
    print(f"Performance stats: {stats}")
    
    # Clean up
    if plugin_file.exists():
        plugin_file.unlink()


if __name__ == "__main__":
    demonstrate_integration_patterns() 