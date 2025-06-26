"""
Test runner for Chapter 2: Algorithmic Complexity & Profiling Techniques.

This script runs all tests for Chapter 2 and provides coverage information.
"""

import sys
import os
import subprocess
import pytest
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    print("Running Chapter 2 Tests with Coverage...")
    print("=" * 50)
    
    # Get the directory containing this script
    test_dir = Path(__file__).parent
    src_dir = test_dir.parent.parent / 'src' / 'chapter_02'
    
    # Run pytest with coverage
    cmd = [
        'python', '-m', 'pytest',
        str(test_dir),
        '--cov=' + str(src_dir),
        '--cov-report=term-missing',
        '--cov-report=html:tests/chapter_02/coverage_html',
        '--cov-report=xml:tests/chapter_02/coverage.xml',
        '-v',
        '--tb=short'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Return code: {result.returncode}")
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Some tests failed!")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


def run_individual_test_files():
    """Run individual test files separately."""
    print("\nRunning Individual Test Files...")
    print("=" * 50)
    
    test_files = [
        'test_profiler.py',
        'test_algorithms.py', 
        'test_benchmarks.py',
        'test_demo.py'
    ]
    
    test_dir = Path(__file__).parent
    
    for test_file in test_files:
        test_path = test_dir / test_file
        if test_path.exists():
            print(f"\nRunning {test_file}...")
            print("-" * 30)
            
            cmd = ['python', '-m', 'pytest', str(test_path), '-v']
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.stdout:
                    print(result.stdout)
                
                if result.stderr:
                    print(result.stderr)
                
                if result.returncode == 0:
                    print(f"✅ {test_file} passed!")
                else:
                    print(f"❌ {test_file} failed!")
                    
            except Exception as e:
                print(f"Error running {test_file}: {e}")
        else:
            print(f"⚠️  {test_file} not found")


def run_demo_tests():
    """Run demo tests to ensure they work correctly."""
    print("\nRunning Demo Tests...")
    print("=" * 50)
    
    try:
        # Import and run demo
        from src.chapter_02.demo import run_comprehensive_demo
        
        print("Running comprehensive demo...")
        run_comprehensive_demo()
        print("✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False
    
    return True


def check_code_quality():
    """Check code quality using basic linting."""
    print("\nChecking Code Quality...")
    print("=" * 50)
    
    src_dir = Path(__file__).parent.parent.parent / 'src' / 'chapter_02'
    
    # Check for basic Python syntax errors
    python_files = list(src_dir.glob('*.py'))
    
    for py_file in python_files:
        print(f"Checking {py_file.name}...")
        
        try:
            with open(py_file, 'r') as f:
                compile(f.read(), py_file, 'exec')
            print(f"✅ {py_file.name} - Syntax OK")
        except SyntaxError as e:
            print(f"❌ {py_file.name} - Syntax Error: {e}")
        except Exception as e:
            print(f"⚠️  {py_file.name} - Error: {e}")


def generate_test_report():
    """Generate a test report."""
    print("\nGenerating Test Report...")
    print("=" * 50)
    
    report = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'coverage': 0,
        'modules_tested': [
            'profiler',
            'algorithms', 
            'benchmarks',
            'demo'
        ]
    }
    
    # This would be populated by actual test results
    print("Test Report:")
    print(f"  Modules tested: {len(report['modules_tested'])}")
    print(f"  Modules: {', '.join(report['modules_tested'])}")
    print("  Coverage: Check coverage_html/index.html for detailed report")


def main():
    """Main function to run all tests and checks."""
    print("Chapter 2: Algorithmic Complexity & Profiling Techniques")
    print("Test Suite Runner")
    print("=" * 60)
    
    # Check code quality first
    check_code_quality()
    
    # Run individual test files
    run_individual_test_files()
    
    # Run tests with coverage
    tests_passed = run_tests_with_coverage()
    
    # Run demo tests
    demo_passed = run_demo_tests()
    
    # Generate report
    generate_test_report()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    
    if tests_passed and demo_passed:
        print("✅ All tests and demos passed successfully!")
        print("📊 Coverage report generated in tests/chapter_02/coverage_html/")
        print("📋 Chapter 2 is ready for review!")
        return 0
    else:
        print("❌ Some tests or demos failed!")
        print("🔧 Please fix the issues before proceeding.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 