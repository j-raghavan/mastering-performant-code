#!/usr/bin/env python3
"""
Script to verify wheel contents for GitHub Actions.
"""

import zipfile
import glob
import sys

def check_wheel_contents():
    """Check that the wheel contains mastering_performant_code files."""
    wheels = glob.glob('dist/*.whl')
    if not wheels:
        print("No wheel files found in dist/")
        return False
    
    wheel_path = wheels[0]
    print(f"Checking wheel: {wheel_path}")
    
    with zipfile.ZipFile(wheel_path, 'r') as wheel:
        files = wheel.namelist()
        pkg_files = [f for f in files if f.startswith('mastering_performant_code/')]
        
        print(f'Wheel contains {len(pkg_files)} mastering_performant_code files')
        print('Sample package files:', pkg_files[:5])
        
        if not pkg_files:
            print('ERROR: No mastering_performant_code files found in wheel!')
            return False
        
        print('Wheel verification passed!')
        return True

if __name__ == "__main__":
    success = check_wheel_contents()
    sys.exit(0 if success else 1) 