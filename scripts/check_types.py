#!/usr/bin/env python3
"""
Type checking validation script for the project.
This script runs mypy on the source code to validate type hints.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_mypy() -> int:
    """Run mypy type checking on the src directory.
    
    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    project_root = Path(__file__).parent.parent
    src_path = project_root / "src"
    
    if not src_path.exists():
        print("❌ Source directory 'src' not found!")
        return 1
    
    print("🔍 Running mypy type checking...")
    print(f"📁 Checking: {src_path}")
    print("-" * 50)
    
    # Set PYTHONPATH to include src directory
    env = os.environ.copy()
    current_pythonpath = env.get('PYTHONPATH', '')
    if current_pythonpath:
        env['PYTHONPATH'] = f"{src_path}:{current_pythonpath}"
    else:
        env['PYTHONPATH'] = str(src_path)
    
    try:
        result = subprocess.run(
            ["poetry", "run", "mypy", "src/"],
            cwd=project_root,
            env=env,
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print("-" * 50)
            print("✅ Type checking passed! No type errors found.")
        else:
            print("-" * 50)
            print("❌ Type checking failed! Please fix the errors above.")
            
        return result.returncode
        
    except FileNotFoundError:
        print("❌ mypy not found! Please install it with:")
        print("   poetry install --with dev")
        return 1
    except Exception as e:
        print(f"❌ Error running mypy: {e}")
        return 1


if __name__ == "__main__":
    exit_code = run_mypy()
    sys.exit(exit_code)
