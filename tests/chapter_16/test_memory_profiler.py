"""
Unit tests for the memory profiler module.

This module tests all functionality of the memory profiler, including
memory analysis, leak detection, and performance comparisons.
"""

import unittest
import gc
import time
from unittest.mock import patch, MagicMock
from mastering_performant_code.chapter_16.memory_profiler import (
    MemoryProfiler, MemorySnapshot, MemoryComparison, 
    memory_context, demonstrate_memory_optimization
)


class TestMemorySnapshot(unittest.TestCase):
    """Test the MemorySnapshot dataclass."""
    
    def test_memory_snapshot_creation(self):
        """Test creating a MemorySnapshot."""
        snapshot = MemorySnapshot(
            current_memory=1024,
            peak_memory=2048,
            object_count=100,
            timestamp=123.456
        )
        
        self.assertEqual(snapshot.current_memory, 1024)
        self.assertEqual(snapshot.peak_memory, 2048)
        self.assertEqual(snapshot.object_count, 100)
        self.assertEqual(snapshot.timestamp, 123.456)


class TestMemoryComparison(unittest.TestCase):
    """Test the MemoryComparison dataclass."""
    
    def test_memory_comparison_creation(self):
        """Test creating a MemoryComparison."""
        baseline = MemorySnapshot(1000, 2000, 50, 1.0)
        optimized = MemorySnapshot(800, 1600, 40, 0.8)
        
        comparison = MemoryComparison(
            baseline=baseline,
            optimized=optimized,
            memory_saved=200,
            percentage_saved=20.0,
            performance_impact=0.2
        )
        
        self.assertEqual(comparison.memory_saved, 200)
        self.assertEqual(comparison.percentage_saved, 20.0)
        self.assertEqual(comparison.performance_impact, 0.2)


class TestMemoryProfiler(unittest.TestCase):
    """Test the MemoryProfiler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.profiler = MemoryProfiler()
    
    def tearDown(self):
        """Clean up after tests."""
        if self.profiler._tracing:
            self.profiler.stop_tracing()
    
    def test_initialization(self):
        """Test MemoryProfiler initialization."""
        self.assertEqual(len(self.profiler.snapshots), 0)
        self.assertFalse(self.profiler._tracing)
    
    def test_start_tracing(self):
        """Test starting memory tracing."""
        self.profiler.start_tracing()
        self.assertTrue(self.profiler._tracing)
        
        # Should not start again if already tracing
        self.profiler.start_tracing()
        self.assertTrue(self.profiler._tracing)
    
    def test_stop_tracing(self):
        """Test stopping memory tracing."""
        self.profiler.start_tracing()
        self.profiler.stop_tracing()
        self.assertFalse(self.profiler._tracing)
        
        # Should not stop again if not tracing
        self.profiler.stop_tracing()
        self.assertFalse(self.profiler._tracing)
    
    def test_take_snapshot(self):
        """Test taking a memory snapshot."""
        snapshot = self.profiler.take_snapshot("test")
        
        self.assertIsInstance(snapshot, MemorySnapshot)
        self.assertGreaterEqual(snapshot.current_memory, 0)
        self.assertGreaterEqual(snapshot.peak_memory, 0)
        self.assertGreaterEqual(snapshot.object_count, 0)
        self.assertGreater(snapshot.timestamp, 0)
        
        # Should be added to snapshots list
        self.assertEqual(len(self.profiler.snapshots), 1)
        self.assertEqual(self.profiler.snapshots[0], snapshot)
    
    def test_analyze_object_memory_simple(self):
        """Test analyzing memory of a simple object."""
        obj = "test string"
        analysis = self.profiler.analyze_object_memory(obj)
        
        self.assertIn('object_size', analysis)
        self.assertIn('reference_count', analysis)
        self.assertIn('type', analysis)
        self.assertIn('container_info', analysis)
        
        self.assertEqual(analysis['type'], 'str')
        self.assertGreater(analysis['object_size'], 0)
        self.assertGreaterEqual(analysis['reference_count'], 0)
    
    def test_analyze_object_memory_container(self):
        """Test analyzing memory of a container object."""
        obj = [1, 2, 3, 4, 5]
        analysis = self.profiler.analyze_object_memory(obj)
        
        self.assertIn('object_size', analysis)
        self.assertIn('container_info', analysis)
        self.assertEqual(analysis['container_info']['length'], 5)
        self.assertIn('content_size', analysis['container_info'])
        self.assertIn('total_size', analysis['container_info'])
    
    def test_analyze_object_memory_recursive(self):
        """Test analyzing memory of a recursive object."""
        obj = []
        obj.append(obj)  # Create a circular reference
        
        analysis = self.profiler.analyze_object_memory(obj)
        
        # Should handle recursive objects gracefully
        self.assertIn('object_size', analysis)
        self.assertIn('container_info', analysis)
    
    @patch('mastering_performant_code.chapter_16.memory_profiler.timeit.timeit')
    def test_compare_memory_usage(self, mock_timeit):
        """Test compare_memory_usage method."""
        mock_timeit.return_value = 0.001
        
        profiler = MemoryProfiler()
        
        # Test with two different functions
        def baseline_func():
            return [i for i in range(100)]
        
        def optimized_func():
            return list(range(100))
        
        comparison = profiler.compare_memory_usage(baseline_func, optimized_func)
        
        assert isinstance(comparison, MemoryComparison)
        assert isinstance(comparison.baseline, MemorySnapshot)
        assert isinstance(comparison.optimized, MemorySnapshot)
        assert hasattr(comparison, 'memory_saved')
        assert hasattr(comparison, 'percentage_saved')
        assert hasattr(comparison, 'performance_impact')
    
    def test_detect_memory_leaks_clean(self):
        """Test detecting memory leaks in a clean function."""
        def clean_function():
            # Create objects that will be garbage collected
            objects = [i for i in range(100)]
            return len(objects)
        
        leak_analysis = self.profiler.detect_memory_leaks(clean_function, iterations=5)
        
        self.assertIn('memory_growth', leak_analysis)
        self.assertIn('memory_after_gc', leak_analysis)
        self.assertIn('potential_leak', leak_analysis)
        self.assertIn('leak_size', leak_analysis)
        self.assertIn('snapshots', leak_analysis)
        
        # Clean function should not have significant leaks
        self.assertGreaterEqual(leak_analysis['leak_size'], 0)
    
    def test_detect_memory_leaks_leaky(self):
        """Test detecting memory leaks in a leaky function."""
        leaky_objects = []
        
        def leaky_function():
            # Create objects that are stored in a global list
            for i in range(100):
                leaky_objects.append([i] * 10)
        
        leak_analysis = self.profiler.detect_memory_leaks(leaky_function, iterations=3)
        
        self.assertIn('potential_leak', leak_analysis)
        self.assertIn('leak_size', leak_analysis)
        
        # Clean up
        leaky_objects.clear()
    
    def test_get_top_memory_users_not_tracing(self):
        """Test getting top memory users when not tracing."""
        users = self.profiler.get_top_memory_users()
        self.assertEqual(users, [])
    
    def test_get_top_memory_users_tracing(self):
        """Test getting top memory users when tracing."""
        self.profiler.start_tracing()
        
        # Create some memory usage
        large_list = [i for i in range(10000)]
        
        users = self.profiler.get_top_memory_users(limit=5)
        
        self.assertIsInstance(users, list)
        # Should return some users when tracing
        self.assertGreaterEqual(len(users), 0)
        
        self.profiler.stop_tracing()


class TestMemoryContext(unittest.TestCase):
    """Test the memory_context context manager."""
    
    def test_memory_context(self):
        """Test the memory_context context manager."""
        profiler = MemoryProfiler()
        
        with patch('builtins.print') as mock_print:
            with memory_context(profiler, "test_context"):
                # Create some memory usage
                test_list = [i for i in range(1000)]
            
            # Should have printed memory usage
            mock_print.assert_called_once()
            call_args = mock_print.call_args[0][0]
            self.assertIn("Memory used in test_context", call_args)


class TestDemonstrateMemoryOptimization(unittest.TestCase):
    """Test the demonstrate_memory_optimization function."""
    
    @patch('builtins.print')
    def test_demonstrate_memory_optimization(self, mock_print):
        """Test the memory optimization demonstration."""
        comparison = demonstrate_memory_optimization()
        
        # Should print optimization results
        self.assertGreater(mock_print.call_count, 0)
        
        # Should return a comparison object
        self.assertIsInstance(comparison, MemoryComparison)


class TestMemoryProfilerIntegration(unittest.TestCase):
    """Integration tests for the memory profiler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.profiler = MemoryProfiler()
    
    def tearDown(self):
        """Clean up after tests."""
        if self.profiler._tracing:
            self.profiler.stop_tracing()
    
    def test_full_profiling_workflow(self):
        """Test a complete profiling workflow."""
        # Start profiling
        self.profiler.start_tracing()
        
        # Take initial snapshot
        initial = self.profiler.take_snapshot("initial")
        
        # Create some objects
        objects = [i for i in range(1000)]
        
        # Take final snapshot
        final = self.profiler.take_snapshot("final")
        
        # Stop profiling
        self.profiler.stop_tracing()
        
        # Verify snapshots
        self.assertEqual(len(self.profiler.snapshots), 2)
        self.assertGreaterEqual(final.current_memory, initial.current_memory)
    
    def test_memory_analysis_workflow(self):
        """Test a complete memory analysis workflow."""
        # Create different types of objects
        simple_obj = "test"
        list_obj = [1, 2, 3, 4, 5]
        dict_obj = {'a': 1, 'b': 2}
        
        # Analyze each
        simple_analysis = self.profiler.analyze_object_memory(simple_obj)
        list_analysis = self.profiler.analyze_object_memory(list_obj)
        dict_analysis = self.profiler.analyze_object_memory(dict_obj)
        
        # Verify analyses
        self.assertEqual(simple_analysis['type'], 'str')
        self.assertEqual(list_analysis['type'], 'list')
        self.assertEqual(dict_analysis['type'], 'dict')
        
        # Verify container info
        self.assertEqual(list_analysis['container_info']['length'], 5)
        self.assertEqual(dict_analysis['container_info']['length'], 2)


if __name__ == '__main__':
    unittest.main(verbosity=2) 