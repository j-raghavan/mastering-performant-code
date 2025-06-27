"""
Test runner for Chapter 12: Disjoint-Set (Union-Find) with Path Compression.

This script runs all tests for Chapter 12 and generates coverage reports.
"""

import pytest
import os
import subprocess
from pathlib import Path


def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    print("Running Chapter 12 tests with coverage...")
    print("=" * 60)
    
    # Get the chapter directory
    chapter_dir = Path(__file__).parent
    src_dir = chapter_dir.parent.parent / "src" / "chapter_12"
    
    # Run pytest with coverage
    cmd = [
        "python", "-m", "pytest",
        str(chapter_dir),
        "--cov=" + str(src_dir),
        "--cov-report=term-missing",
        "--cov-report=html:tests/chapter_12/coverage_html",
        "--cov-report=xml:tests/chapter_12/coverage.xml",
        "-v",
        "--tb=short"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    return result.returncode == 0


def run_individual_test_files():
    """Run individual test files separately."""
    print("\nRunning individual test files...")
    print("=" * 60)
    
    test_files = [
        "test_disjoint_set.py",
        "test_optimized_disjoint_set.py",
        "test_memory_tracked_disjoint_set.py",
        "test_graph_union_find.py",
        "test_network_connectivity.py",
        "test_image_segmentation.py",
        "test_analyzer.py"
    ]
    
    chapter_dir = Path(__file__).parent
    all_passed = True
    
    for test_file in test_files:
        test_path = chapter_dir / test_file
        if test_path.exists():
            print(f"\nRunning {test_file}...")
            print("-" * 40)
            
            cmd = ["python", "-m", "pytest", str(test_path), "-v"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            
            if result.returncode != 0:
                all_passed = False
                print(f"❌ {test_file} failed")
            else:
                print(f"✅ {test_file} passed")
        else:
            print(f"⚠️  {test_file} not found")
    
    return all_passed


def run_demo_tests():
    """Run demo functionality tests."""
    print("\nRunning demo tests...")
    print("=" * 60)
    
    try:
        # Import and run demo functions
        from chapter_12.demo import (
            benchmark_comparison,
            memory_usage_comparison,
            real_world_application_demo,
            tree_structure_analysis_demo,
            memory_tracking_demo,
            stress_test_demo,
            scalability_analysis_demo
        )
        
        # Test that demo functions can be called without errors
        print("Testing benchmark_comparison...")
        benchmark_comparison()
        
        print("Testing memory_usage_comparison...")
        memory_usage_comparison()
        
        print("Testing real_world_application_demo...")
        real_world_application_demo()
        
        print("Testing tree_structure_analysis_demo...")
        tree_structure_analysis_demo()
        
        print("Testing memory_tracking_demo...")
        memory_tracking_demo()
        
        print("Testing stress_test_demo...")
        stress_test_demo()
        
        print("Testing scalability_analysis_demo...")
        scalability_analysis_demo()
        
        print("✅ All demo tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Demo tests failed: {e}")
        return False


def run_performance_tests():
    """Run performance tests."""
    print("\nRunning performance tests...")
    print("=" * 60)
    
    try:
        from chapter_12.analyzer import UnionFindAnalyzer
        from chapter_12.disjoint_set import DisjointSet
        from chapter_12.optimized_disjoint_set import OptimizedDisjointSet
        
        # Test basic operations
        print("Testing basic operations...")
        ds = OptimizedDisjointSet()
        for i in range(100):
            ds.make_set(i)
        
        for i in range(50):
            ds.union(i, i + 1)
        
        assert ds.connected(0, 99)
        print("✅ Basic operations test passed")
        
        # Test tree structure analysis
        print("Testing tree structure analysis...")
        analysis = UnionFindAnalyzer.analyze_tree_structure(ds)
        assert 'avg_path_length' in analysis
        assert 'compression_efficiency' in analysis
        print("✅ Tree structure analysis test passed")
        
        # Test stress test
        print("Testing stress test...")
        stress_results = UnionFindAnalyzer.stress_test(OptimizedDisjointSet, 1000)
        assert 'total_time' in stress_results
        assert 'operations_per_second' in stress_results
        print("✅ Stress test passed")
        
        print("✅ All performance tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Performance tests failed: {e}")
        return False


def run_memory_tests():
    """Run memory usage tests."""
    print("\nRunning memory tests...")
    print("=" * 60)
    
    try:
        from chapter_12.memory_tracked_disjoint_set import MemoryTrackedDisjointSet
        
        # Test memory tracking
        print("Testing memory tracking...")
        ds = MemoryTrackedDisjointSet()
        
        for i in range(100):
            ds.make_set(i)
        
        memory_info = ds.get_memory_info()
        assert memory_info.elements == 100
        assert memory_info.total_size > 0
        print("✅ Memory tracking test passed")
        
        # Test memory efficiency report
        print("Testing memory efficiency report...")
        report = ds.memory_efficiency_report()
        assert "Memory Efficiency Report" in report
        print("✅ Memory efficiency report test passed")
        
        # Test memory breakdown
        print("Testing memory breakdown...")
        breakdown = ds.get_memory_breakdown()
        assert 'total' in breakdown
        print("✅ Memory breakdown test passed")
        
        print("✅ All memory tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Memory tests failed: {e}")
        return False


def run_application_tests():
    """Run real-world application tests."""
    print("\nRunning application tests...")
    print("=" * 60)
    
    try:
        from chapter_12.network_connectivity import NetworkConnectivity
        from chapter_12.image_segmentation import ImageSegmentation
        
        # Test network connectivity
        print("Testing network connectivity...")
        network = NetworkConnectivity()
        network.add_connection(1, 2)
        network.add_connection(2, 3)
        network.add_connection(4, 5)
        
        assert network.are_connected(1, 3)
        assert not network.are_connected(1, 4)
        assert len(network.get_all_networks()) == 2
        print("✅ Network connectivity test passed")
        
        # Test image segmentation
        print("Testing image segmentation...")
        img = ImageSegmentation(5, 5)
        img.set_pixel(0, 0, 1)
        img.set_pixel(0, 1, 1)
        img.set_pixel(1, 0, 1)
        
        assert img.get_segment_size(0, 0) == 3
        assert img.count_segments() == 1
        print("✅ Image segmentation test passed")
        
        print("✅ All application tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Application tests failed: {e}")
        return False


def main():
    """Main test runner function."""
    print("Chapter 12: Disjoint-Set (Union-Find) with Path Compression")
    print("Test Runner")
    print("=" * 80)
    
    # Run different types of tests
    tests = [
        ("Individual Test Files", run_individual_test_files),
        ("Demo Tests", run_demo_tests),
        ("Performance Tests", run_performance_tests),
        ("Memory Tests", run_memory_tests),
        ("Application Tests", run_application_tests),
        ("Coverage Tests", run_tests_with_coverage)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED!")
    print("="*80)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    main() 