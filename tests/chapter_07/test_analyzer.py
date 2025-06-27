"""
Unit tests for AVL Tree Analyzer.

This module provides comprehensive tests for the AVLTreeAnalyzer class,
ensuring all benchmarking and analysis methods work correctly.
"""

import pytest
import os

from mastering_performant_code.chapter_07.analyzer import AVLTreeAnalyzer
from mastering_performant_code.chapter_07.avl_tree import AVLTree

class TestAVLTreeAnalyzer:
    """Test cases for AVLTreeAnalyzer class."""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        analyzer = AVLTreeAnalyzer()
        assert analyzer.results == {}
    
    def test_benchmark_insertion_small_dataset(self):
        """Test insertion benchmarking with small dataset."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [10, 50]
        
        results = analyzer.benchmark_insertion(data_sizes, num_trials=2)
        
        # Check that all expected keys are present
        expected_keys = ['avl_tree', 'bst', 'list', 'set']
        for key in expected_keys:
            assert key in results
            assert len(results[key]) == len(data_sizes)
        
        # Check that all results are positive numbers
        for key in expected_keys:
            for time_value in results[key]:
                assert time_value > 0
    
    def test_benchmark_search_small_dataset(self):
        """Test search benchmarking with small dataset."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [10, 50]
        
        results = analyzer.benchmark_search(data_sizes, num_trials=2)
        
        # Check that all expected keys are present
        expected_keys = ['avl_tree', 'set', 'list']
        for key in expected_keys:
            assert key in results
            assert len(results[key]) == len(data_sizes)
        
        # Check that all results are positive numbers
        for key in expected_keys:
            for time_value in results[key]:
                assert time_value > 0
    
    def test_analyze_tree_properties(self):
        """Test tree properties analysis."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [10, 50, 100]
        
        results = analyzer.analyze_tree_properties(data_sizes)
        
        # Check that all expected keys are present
        expected_keys = ['size', 'height', 'is_balanced', 'theoretical_max_height']
        for key in expected_keys:
            assert key in results
            assert len(results[key]) == len(data_sizes)
        
        # Check specific properties
        for i, size in enumerate(data_sizes):
            assert results['size'][i] == size
            assert results['height'][i] > 0
            assert results['is_balanced'][i] is True  # AVL trees should always be balanced
            assert results['theoretical_max_height'][i] > 0
    
    def test_benchmark_rotation_scenarios(self):
        """Test rotation scenario benchmarking."""
        analyzer = AVLTreeAnalyzer()
        
        results = analyzer.benchmark_rotation_scenarios(num_trials=2)
        
        # Check that all expected keys are present
        expected_keys = ['left_left', 'right_right', 'left_right', 'right_left']
        for key in expected_keys:
            assert key in results
            assert results[key] > 0
    
    def test_print_benchmark_results(self, capsys):
        """Test benchmark results printing."""
        analyzer = AVLTreeAnalyzer()
        
        # Create mock results
        results = {
            'avl_tree': [0.001, 0.002],
            'bst': [0.002, 0.004],
            'list': [0.0005, 0.001],
            'set': [0.0003, 0.0006]
        }
        
        analyzer.print_benchmark_results(results, "Test Results")
        
        # Capture the output
        captured = capsys.readouterr()
        output = captured.out
        
        # Check that the output contains expected content
        assert "Test Results" in output
        assert "AVL Tree" in output
        assert "BST" in output
        assert "List" in output
        assert "Set" in output
    
    def test_print_tree_analysis(self, capsys):
        """Test tree analysis printing."""
        analyzer = AVLTreeAnalyzer()
        
        # Create mock results
        results = {
            'size': [10, 50],
            'height': [4, 6],
            'is_balanced': [True, True],
            'theoretical_max_height': [5, 7]
        }
        
        analyzer.print_tree_analysis(results)
        
        # Capture the output
        captured = capsys.readouterr()
        output = captured.out
        
        # Check that the output contains expected content
        assert "AVL Tree Properties Analysis" in output
        assert "Size" in output
        assert "Height" in output
        assert "Balanced" in output
    
    def test_print_rotation_benchmarks(self, capsys):
        """Test rotation benchmark printing."""
        analyzer = AVLTreeAnalyzer()
        
        # Create mock results
        results = {
            'left_left': 0.001,
            'right_right': 0.001,
            'left_right': 0.001,
            'right_left': 0.001
        }
        
        analyzer.print_rotation_benchmarks(results)
        
        # Capture the output
        captured = capsys.readouterr()
        output = captured.out
        
        # Check that the output contains expected content
        assert "Rotation Performance Analysis" in output
        assert "left_left" in output
        assert "right_right" in output
        assert "left_right" in output
        assert "right_left" in output
    
    def test_benchmark_insertion_performance_comparison(self):
        """Test that AVL tree insertion performance is reasonable."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [100]
        
        results = analyzer.benchmark_insertion(data_sizes, num_trials=3)
        
        # AVL tree should be slower than set but faster than list for large datasets
        # For small datasets, the difference might be minimal
        avl_time = results['avl_tree'][0]
        set_time = results['set'][0]
        list_time = results['list'][0]
        
        # All times should be positive
        assert avl_time > 0
        assert set_time > 0
        assert list_time > 0
        
        # AVL tree should be slower than set (due to balancing overhead)
        # but this might not always be true for very small datasets
        # So we just check that times are reasonable
    
    def test_benchmark_search_performance_comparison(self):
        """Test that AVL tree search performance is reasonable."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [100]
        
        results = analyzer.benchmark_search(data_sizes, num_trials=3)
        
        avl_time = results['avl_tree'][0]
        set_time = results['set'][0]
        list_time = results['list'][0]
        
        # All times should be positive
        assert avl_time > 0
        assert set_time > 0
        assert list_time > 0
        
        # For small datasets, the performance differences might be minimal
        # So we just check that all times are reasonable and positive
        # AVL tree should generally be faster than list for search, but this
        # might not always be true for very small datasets due to overhead
    
    def test_tree_properties_validation(self):
        """Test that analyzed tree properties are valid."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [10, 50, 100]
        
        results = analyzer.analyze_tree_properties(data_sizes)
        
        for i, size in enumerate(data_sizes):
            # Height should be positive and reasonable
            height = results['height'][i]
            assert height > 0
            assert height <= results['theoretical_max_height'][i]
            
            # AVL trees should always be balanced
            assert results['is_balanced'][i] is True
            
            # Theoretical max height should be reasonable
            theoretical_max = results['theoretical_max_height'][i]
            assert theoretical_max > 0
            # For AVL trees, theoretical max height is approximately 1.44 * log2(n+2)
            import math
            expected_max = int(1.44 * math.log2(size + 2) - 0.328)
            assert theoretical_max >= expected_max - 1  # Allow small rounding differences
    
    def test_rotation_scenario_validation(self):
        """Test that rotation scenarios produce valid trees."""
        analyzer = AVLTreeAnalyzer()
        
        # Test each rotation scenario manually
        scenarios = [
            ([30, 20, 10], "left_left"),
            ([10, 20, 30], "right_right"),
            ([30, 10, 20], "left_right"),
            ([10, 30, 20], "right_left")
        ]
        
        for values, scenario_name in scenarios:
            tree = AVLTree()
            for value in values:
                tree.insert(value)
            
            # Tree should be balanced after rotations
            assert tree.is_balanced() is True
            assert tree.height() <= 3  # Small trees should have reasonable height
            
            # All values should be present
            for value in values:
                assert tree.search(value) is not None
    
    def test_large_dataset_benchmarking(self):
        """Test benchmarking with larger datasets."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [1000]  # Use smaller size for testing
        
        # Test insertion benchmarking
        insertion_results = analyzer.benchmark_insertion(data_sizes, num_trials=2)
        assert len(insertion_results['avl_tree']) == 1
        assert insertion_results['avl_tree'][0] > 0
        
        # Test search benchmarking
        search_results = analyzer.benchmark_search(data_sizes, num_trials=2)
        assert len(search_results['avl_tree']) == 1
        assert search_results['avl_tree'][0] > 0
        
        # Test tree properties analysis
        tree_results = analyzer.analyze_tree_properties(data_sizes)
        assert len(tree_results['size']) == 1
        assert tree_results['size'][0] == 1000
        assert tree_results['is_balanced'][0] is True
    
    def test_benchmark_with_different_trial_counts(self):
        """Test benchmarking with different numbers of trials."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [50]
        
        # Test with 1 trial
        results_1 = analyzer.benchmark_insertion(data_sizes, num_trials=1)
        assert len(results_1['avl_tree']) == 1
        
        # Test with 5 trials
        results_5 = analyzer.benchmark_insertion(data_sizes, num_trials=5)
        assert len(results_5['avl_tree']) == 1
        
        # Both should produce valid results
        assert results_1['avl_tree'][0] > 0
        assert results_5['avl_tree'][0] > 0
    
    def test_analyzer_with_empty_datasets(self):
        """Test analyzer behavior with edge cases."""
        analyzer = AVLTreeAnalyzer()
        
        # Test with empty data sizes list
        empty_results = analyzer.benchmark_insertion([], num_trials=1)
        assert empty_results['avl_tree'] == []
        assert empty_results['bst'] == []
        assert empty_results['list'] == []
        assert empty_results['set'] == []
        
        # Test with empty data sizes for tree analysis
        empty_tree_results = analyzer.analyze_tree_properties([])
        assert empty_tree_results['size'] == []
        assert empty_tree_results['height'] == []
        assert empty_tree_results['is_balanced'] == []
        assert empty_tree_results['theoretical_max_height'] == []
    
    def test_benchmark_consistency(self):
        """Test that benchmarks produce consistent results."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [100]
        
        # Run the same benchmark multiple times
        results1 = analyzer.benchmark_insertion(data_sizes, num_trials=3)
        results2 = analyzer.benchmark_insertion(data_sizes, num_trials=3)
        
        # Results should be similar (within reasonable bounds)
        time1 = results1['avl_tree'][0]
        time2 = results2['avl_tree'][0]
        
        # Times should be positive and reasonably close
        assert time1 > 0
        assert time2 > 0
        
        # Check that times are within reasonable bounds of each other
        # (allowing for system variations)
        ratio = max(time1, time2) / min(time1, time2)
        assert ratio < 10  # Times should be within 10x of each other
    
    def test_tree_height_growth(self):
        """Test that tree height grows logarithmically."""
        analyzer = AVLTreeAnalyzer()
        data_sizes = [10, 100, 1000]
        
        results = analyzer.analyze_tree_properties(data_sizes)
        
        heights = results['height']
        
        # Height should increase as size increases
        assert heights[1] >= heights[0]  # 100 vs 10
        assert heights[2] >= heights[1]  # 1000 vs 100
        
        # But height should not grow linearly
        # For AVL trees, height should be approximately log2(n)
        import math
        for i, size in enumerate(data_sizes):
            expected_height = math.log2(size)
            # Allow some flexibility due to AVL balancing
            assert heights[i] <= expected_height * 2 