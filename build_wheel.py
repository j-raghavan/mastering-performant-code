#!/usr/bin/env python3
"""
Helper script to build and test the Python wheel package locally.
"""

import subprocess
import sys
import zipfile
import glob
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
os.chdir(PROJECT_ROOT)


def run_command(cmd, check=True):
    """Run a command and return the result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def build_wheel():
    """Build the wheel package."""
    print("Building wheel package...")
    
    # Clean previous builds
    if os.path.exists("dist"):
        run_command("rm -rf dist")
    if os.path.exists("build"):
        run_command("rm -rf build")
    if os.path.exists("*.egg-info"):
        run_command("rm -rf *.egg-info")
    
    # Install build dependencies
    run_command("pip install build wheel setuptools")
    
    # Build wheel
    run_command("python -m build --wheel")
    
    print("Wheel built successfully!")

def verify_wheel_contents():
    """Verify that the wheel contains mastering_performant_code directory."""
    print("\nVerifying wheel contents...")
    
    wheels = glob.glob("dist/*.whl")
    if not wheels:
        print("No wheel files found in dist/")
        return False
    
    wheel_path = wheels[0]
    print(f"Checking wheel: {wheel_path}")
    
    with zipfile.ZipFile(wheel_path, 'r') as wheel:
        files = wheel.namelist()
        
        # Count files in mastering_performant_code
        pkg_files = [f for f in files if f.startswith('mastering_performant_code/')]
        
        print(f"Wheel contains {len(pkg_files)} mastering_performant_code files")
        
        if pkg_files:
            print("Sample package files:")
            for f in pkg_files[:5]:
                print(f"  {f}")
        
        # Check for key files
        key_files = [
            'mastering_performant_code/__init__.py',
            'mastering_performant_code/chapter_01/__init__.py',
            'mastering_performant_code/chapter_02/__init__.py'
        ]
        
        missing_files = [f for f in key_files if f not in files]
        if missing_files:
            print(f"Warning: Missing key files: {missing_files}")
            return False
        
        print("All key files present!")
        return True

def test_wheel_installation():
    """Test that the wheel can be installed and imported."""
    print("\nTesting wheel installation...")
    
    wheels = glob.glob("dist/*.whl")
    if not wheels:
        print("No wheel files found")
        return False
    
    wheel_path = wheels[0]
    
    try:
        # Install the wheel
        run_command(f"pip install {wheel_path}")
        
        # Test imports
        test_script = """
import mastering_performant_code
print(f"Successfully imported mastering_performant_code package: {mastering_performant_code.__version__}")

# Test importing a specific chapter
import mastering_performant_code.chapter_01
import mastering_performant_code.chapter_02
print("Successfully imported chapter modules")

# Test importing specific classes
from mastering_performant_code.chapter_01 import DynamicArray, HashTable
from mastering_performant_code.chapter_02 import AlgorithmProfiler
print("Successfully imported specific classes")
"""
        
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Wheel installation test passed!")
            print(result.stdout)
            return True
        else:
            print("Wheel installation test failed!")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"Error testing wheel installation: {e}")
        return False

def main():
    """Main function."""
    print("=== Python Wheel Builder and Tester ===\n")
    
    # Build the wheel
    build_wheel()
    
    # Verify contents
    if not verify_wheel_contents():
        print("Wheel verification failed!")
        sys.exit(1)
    
    # Test installation
    if not test_wheel_installation():
        print("Wheel installation test failed!")
        sys.exit(1)
    
    print("\n=== All tests passed! ===")
    print("The wheel package is ready for distribution.")

if __name__ == "__main__":
    main() 
