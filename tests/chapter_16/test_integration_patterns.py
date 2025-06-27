"""
Unit tests for the integration patterns module.

This module tests all functionality of the integration patterns, including
plugin systems, subprocess optimization, thread-safe caching, and performance monitoring.
"""

import unittest
import tempfile
import shutil
import time
import threading
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from chapter_16.integration_patterns import (
    PluginManager, PluginInfo, SubprocessOptimizer, 
    ThreadSafeCache, PerformanceMonitor, demonstrate_integration_patterns
)


class TestPluginInfo(unittest.TestCase):
    """Test the PluginInfo dataclass."""
    
    def test_plugin_info_creation(self):
        """Test creating a PluginInfo."""
        info = PluginInfo(
            name="test_plugin",
            version="1.0.0",
            description="Test plugin",
            functions=["func1", "func2"],
            load_time=0.1
        )
        
        self.assertEqual(info.name, "test_plugin")
        self.assertEqual(info.version, "1.0.0")
        self.assertEqual(info.description, "Test plugin")
        self.assertEqual(info.functions, ["func1", "func2"])
        self.assertEqual(info.load_time, 0.1)


class TestPluginManager(unittest.TestCase):
    """Test the PluginManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.plugin_manager = PluginManager(plugin_directory=self.temp_dir)
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test PluginManager initialization."""
        self.assertEqual(len(self.plugin_manager.plugins), 0)
        self.assertEqual(len(self.plugin_manager.plugin_info), 0)
        self.assertTrue(self.plugin_manager.plugin_directory.exists())
    
    def test_register_plugin(self):
        """Test registering a plugin."""
        # Create a mock module
        mock_module = MagicMock()
        mock_module.func1 = lambda x: x * 2
        mock_module.func2 = lambda x: x + 1
        
        self.plugin_manager.register_plugin(
            "test_plugin", mock_module, "1.0.0", "Test plugin"
        )
        
        self.assertIn("test_plugin", self.plugin_manager.plugins)
        self.assertIn("test_plugin", self.plugin_manager.plugin_info)
        
        info = self.plugin_manager.plugin_info["test_plugin"]
        self.assertEqual(info.name, "test_plugin")
        self.assertEqual(info.version, "1.0.0")
        self.assertEqual(info.description, "Test plugin")
        self.assertIn("func1", info.functions)
        self.assertIn("func2", info.functions)
    
    def test_load_plugin_from_file_success(self):
        """Test loading a plugin from file successfully."""
        # Create a test plugin file
        plugin_content = """
def test_function(x):
    return x * 2

def another_function(y):
    return y + 1
"""
        plugin_file = Path(self.temp_dir) / "test_plugin.py"
        plugin_file.write_text(plugin_content)
        
        plugin_name = self.plugin_manager.load_plugin_from_file(str(plugin_file))
        
        self.assertEqual(plugin_name, "test_plugin")
        self.assertIn("test_plugin", self.plugin_manager.plugins)
        
        # Test calling the plugin function
        result = self.plugin_manager.call_plugin_function("test_plugin", "test_function", 5)
        self.assertEqual(result, 10)
    
    def test_load_plugin_from_file_not_found(self):
        """Test loading a plugin from non-existent file."""
        plugin_name = self.plugin_manager.load_plugin_from_file("nonexistent.py")
        self.assertIsNone(plugin_name)
    
    def test_load_plugin_from_file_invalid(self):
        """Test loading a plugin with invalid syntax."""
        # Create a plugin file with invalid syntax
        plugin_content = "def test_function(x):\n    return x * 2\ninvalid syntax here"
        plugin_file = Path(self.temp_dir) / "invalid_plugin.py"
        plugin_file.write_text(plugin_content)
        
        plugin_name = self.plugin_manager.load_plugin_from_file(str(plugin_file))
        self.assertIsNone(plugin_name)
    
    def test_get_plugin(self):
        """Test getting a plugin by name."""
        # Register a plugin
        mock_module = MagicMock()
        self.plugin_manager.register_plugin("test_plugin", mock_module)
        
        # Get the plugin
        plugin = self.plugin_manager.get_plugin("test_plugin")
        self.assertEqual(plugin, mock_module)
        
        # Get non-existent plugin
        plugin = self.plugin_manager.get_plugin("nonexistent")
        self.assertIsNone(plugin)
    
    def test_list_plugins(self):
        """Test listing all plugins."""
        # Register multiple plugins
        mock_module1 = MagicMock()
        mock_module2 = MagicMock()
        
        self.plugin_manager.register_plugin("plugin1", mock_module1)
        self.plugin_manager.register_plugin("plugin2", mock_module2)
        
        plugins = self.plugin_manager.list_plugins()
        self.assertEqual(len(plugins), 2)
        plugin_names = [p.name for p in plugins]
        self.assertIn("plugin1", plugin_names)
        self.assertIn("plugin2", plugin_names)
    
    def test_call_plugin_function_success(self):
        """Test calling a plugin function successfully."""
        # Register a plugin with a function
        mock_module = MagicMock()
        mock_module.test_func = lambda x, y: x + y
        self.plugin_manager.register_plugin("test_plugin", mock_module)
        
        result = self.plugin_manager.call_plugin_function("test_plugin", "test_func", 2, 3)
        self.assertEqual(result, 5)
    
    def test_call_plugin_function_plugin_not_found(self):
        """Test calling a function from non-existent plugin."""
        with self.assertRaises(ValueError) as context:
            self.plugin_manager.call_plugin_function("nonexistent", "func", 1)
        
        self.assertIn("Plugin 'nonexistent' not found", str(context.exception))
    
    def test_call_plugin_function_function_not_found(self):
        """Test calling a non-existent function from a plugin."""
        # Use a real object with no such attribute
        class DummyPlugin:
            def existing_func(self):
                return 42
        plugin = DummyPlugin()
        self.plugin_manager.register_plugin("test_plugin", plugin)
        
        with self.assertRaises(ValueError) as context:
            self.plugin_manager.call_plugin_function("test_plugin", "nonexistent", 1)
        
        self.assertIn("Function 'nonexistent' not found", str(context.exception))


class TestSubprocessOptimizer(unittest.TestCase):
    """Test the SubprocessOptimizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = SubprocessOptimizer()
    
    def test_initialization(self):
        """Test SubprocessOptimizer initialization."""
        self.assertEqual(self.optimizer.max_workers, 4)
        self.assertEqual(len(self.optimizer.processes), 0)
    
    def test_run_task_in_subprocess_success(self):
        """Test running a task in subprocess successfully."""
        script_content = """
def main(data):
    return data * 2
"""
        
        result = self.optimizer.run_task_in_subprocess(script_content, 5)
        self.assertEqual(result, 10)
    
    def test_run_task_in_subprocess_failure(self):
        """Test running a task in subprocess that fails."""
        script_content = """
def main(data):
    raise ValueError("Test error")
"""
        
        with self.assertRaises(RuntimeError) as context:
            self.optimizer.run_task_in_subprocess(script_content, 5)
        
        self.assertIn("Subprocess failed", str(context.exception))
    
    def test_run_parallel_tasks(self):
        """Test running multiple tasks in parallel."""
        tasks = [
            ("def main(data): return data * 2", 5),
            ("def main(data): return data + 10", 5),
            ("def main(data): return data ** 2", 3)
        ]
        
        results = self.optimizer.run_parallel_tasks(tasks)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], 10)  # 5 * 2
        self.assertEqual(results[1], 15)  # 5 + 10
        self.assertEqual(results[2], 9)   # 3 ** 2


class TestThreadSafeCache(unittest.TestCase):
    """Test the ThreadSafeCache class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cache = ThreadSafeCache(max_size=3)
    
    def test_initialization(self):
        """Test ThreadSafeCache initialization."""
        self.assertEqual(self.cache.max_size, 3)
        self.assertEqual(self.cache.size(), 0)
    
    def test_set_and_get(self):
        """Test setting and getting values from cache."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), None)
        self.assertEqual(self.cache.get("key3", "default"), "default")
    
    def test_cache_eviction(self):
        """Test cache eviction when max size is reached."""
        # Fill the cache
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.cache.set("key3", "value3")
        
        self.assertEqual(self.cache.size(), 3)
        
        # Add one more item, should evict least accessed
        self.cache.set("key4", "value4")
        
        # key1 should be evicted (least accessed)
        self.assertIsNone(self.cache.get("key1"))
        self.assertEqual(self.cache.get("key2"), "value2")
        self.assertEqual(self.cache.get("key3"), "value3")
        self.assertEqual(self.cache.get("key4"), "value4")
    
    def test_access_count_tracking(self):
        """Test that access counts are tracked correctly."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        # Access key1 multiple times
        self.cache.get("key1")
        self.cache.get("key1")
        self.cache.get("key1")
        # Access key2 once
        self.cache.get("key2")
        # Add a new item, should evict least accessed (key2)
        self.cache.set("key3", "value3")
        # Add another item, should evict next least accessed (key1)
        self.cache.set("key4", "value4")
        # Now, only three keys should remain in the cache
        remaining_keys = {k for k in ["key1", "key2", "key3", "key4"] if self.cache.get(k) is not None}
        self.assertEqual(len(remaining_keys), 3)
        missing_keys = {k for k in ["key1", "key2", "key3", "key4"] if self.cache.get(k) is None}
        self.assertEqual(len(missing_keys), 1)
    
    def test_clear(self):
        """Test clearing the cache."""
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        
        self.assertEqual(self.cache.size(), 2)
        
        self.cache.clear()
        
        self.assertEqual(self.cache.size(), 0)
        self.assertIsNone(self.cache.get("key1"))
        self.assertIsNone(self.cache.get("key2"))
    
    def test_thread_safety(self):
        """Test thread safety of the cache."""
        # Use a larger cache size to avoid eviction during the test
        cache = ThreadSafeCache(max_size=10000)
        
        def worker(worker_id):
            for i in range(100):
                key = f"worker_{worker_id}_key_{i}"
                value = f"value_{worker_id}_{i}"
                cache.set(key, value)
                
                # Small delay to increase chance of race conditions
                time.sleep(0.001)
                
                retrieved = cache.get(key)
                if retrieved != value:
                    raise ValueError(f"Cache inconsistency: {retrieved} != {value}")
        
        # Run multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()


class TestPerformanceMonitor(unittest.TestCase):
    """Test the PerformanceMonitor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.monitor = PerformanceMonitor()
    
    def test_initialization(self):
        """Test PerformanceMonitor initialization."""
        self.assertEqual(len(self.monitor.metrics), 0)
        self.assertEqual(len(self.monitor.start_times), 0)
    
    def test_record_metric(self):
        """Test recording a metric."""
        self.monitor.record_metric("test_metric", 1.5)
        self.monitor.record_metric("test_metric", 2.5)
        
        self.assertIn("test_metric", self.monitor.metrics)
        self.assertEqual(len(self.monitor.metrics["test_metric"]), 2)
        self.assertEqual(self.monitor.metrics["test_metric"], [1.5, 2.5])
    
    def test_measure_context_manager(self):
        """Test the measure context manager."""
        with self.monitor.measure("test_operation"):
            time.sleep(0.01)  # Small delay
        
        self.assertIn("test_operation", self.monitor.metrics)
        self.assertEqual(len(self.monitor.metrics["test_operation"]), 1)
        self.assertGreater(self.monitor.metrics["test_operation"][0], 0)
    
    def test_get_statistics(self):
        """Test getting statistics for a metric."""
        # Record some metrics
        self.monitor.record_metric("test_metric", 1.0)
        self.monitor.record_metric("test_metric", 2.0)
        self.monitor.record_metric("test_metric", 3.0)
        
        stats = self.monitor.get_statistics("test_metric")
        
        self.assertEqual(stats["count"], 3)
        self.assertEqual(stats["min"], 1.0)
        self.assertEqual(stats["max"], 3.0)
        self.assertEqual(stats["mean"], 2.0)
        self.assertEqual(stats["total"], 6.0)
    
    def test_get_statistics_empty(self):
        """Test getting statistics for non-existent metric."""
        stats = self.monitor.get_statistics("nonexistent")
        self.assertEqual(stats, {})
    
    def test_export_metrics_json(self):
        """Test exporting metrics in JSON format."""
        self.monitor.record_metric("metric1", 1.0)
        self.monitor.record_metric("metric2", 2.0)
        
        json_output = self.monitor.export_metrics("json")
        
        self.assertIn("metric1", json_output)
        self.assertIn("metric2", json_output)
        self.assertIn("1.0", json_output)
        self.assertIn("2.0", json_output)
    
    def test_export_metrics_csv(self):
        """Test exporting metrics in CSV format."""
        self.monitor.record_metric("metric1", 1.0)
        self.monitor.record_metric("metric1", 2.0)
        
        csv_output = self.monitor.export_metrics("csv")
        
        lines = csv_output.split('\n')
        self.assertEqual(lines[0], "metric,value")
        self.assertIn("metric1,1.0", lines)
        self.assertIn("metric1,2.0", lines)
    
    def test_export_metrics_invalid_format(self):
        """Test exporting metrics with invalid format."""
        with self.assertRaises(ValueError) as context:
            self.monitor.export_metrics("invalid")
        
        self.assertIn("Unsupported format", str(context.exception))


class TestDemonstrateIntegrationPatterns(unittest.TestCase):
    """Test the demonstrate_integration_patterns function."""
    
    @patch('builtins.print')
    def test_demonstrate_integration_patterns(self, mock_print):
        """Test the integration patterns demonstration."""
        demonstrate_integration_patterns()
        
        # Should print demonstration output
        self.assertGreater(mock_print.call_count, 0)


class TestIntegrationPatternsIntegration(unittest.TestCase):
    """Integration tests for the integration patterns."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_plugin_system_integration(self):
        """Test complete plugin system workflow."""
        plugin_manager = PluginManager(plugin_directory=self.temp_dir)
        
        # Create a plugin file
        plugin_content = """
def add_numbers(a, b):
    return a + b

def multiply_numbers(a, b):
    return a * b
"""
        plugin_file = Path(self.temp_dir) / "math_plugin.py"
        plugin_file.write_text(plugin_content)
        
        # Load the plugin
        plugin_name = plugin_manager.load_plugin_from_file(str(plugin_file))
        self.assertEqual(plugin_name, "math_plugin")
        
        # Use the plugin
        result1 = plugin_manager.call_plugin_function("math_plugin", "add_numbers", 3, 4)
        result2 = plugin_manager.call_plugin_function("math_plugin", "multiply_numbers", 3, 4)
        
        self.assertEqual(result1, 7)
        self.assertEqual(result2, 12)
    
    def test_cache_and_monitor_integration(self):
        """Test cache and monitor integration."""
        cache = ThreadSafeCache(max_size=10)
        monitor = PerformanceMonitor()
        
        # Use cache with monitoring
        with monitor.measure("cache_operation"):
            cache.set("key1", "value1")
            value = cache.get("key1")
        
        self.assertEqual(value, "value1")
        
        stats = monitor.get_statistics("cache_operation")
        self.assertEqual(stats["count"], 1)
        self.assertGreater(stats["total"], 0)


if __name__ == '__main__':
    unittest.main(verbosity=2) 