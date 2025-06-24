#!/usr/bin/env python3
"""
Test runner script for the Math Expert LLM Application
"""
import argparse
import subprocess
import sys
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage=True, parallel=False):
    """
    Run tests with different configurations

    Args:
        test_type: Type of tests to run (unit, integration, performance, all)
        verbose: Enable verbose output
        coverage: Enable coverage reporting
        parallel: Run tests in parallel
    """

    # Base pytest command
    cmd = ["python", "-m", "pytest"]

    # Add test type specific arguments
    if test_type == "unit":
        cmd.extend(["tests/unit"])
    elif test_type == "integration":
        cmd.extend(["tests/integration"])
    elif test_type == "performance":
        cmd.extend(["tests/test_performance.py", "-m", "slow"])
    elif test_type == "fast":
        cmd.extend(["-m", "not slow"])
    elif test_type == "all":
        cmd.append("tests/")
    else:
        print(f"Unknown test type: {test_type}")
        return False

    # Add optional flags
    if verbose:
        cmd.append("-v")

    if coverage and test_type != "performance":
        cmd.extend(["--cov=src", "--cov-report=term-missing"])

    if parallel:
        cmd.extend(["-n", "auto"])

    # Add color output
    cmd.append("--color=yes")

    print(f"Running command: {' '.join(cmd)}")

    try:
        # Run from project root directory (parent of tests folder)
        result = subprocess.run(cmd, cwd=Path(__file__).parent.parent)
        return result.returncode == 0
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user")
        return False
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


def check_dependencies():
    """Check if all test dependencies are installed"""
    required_packages = ["pytest", "pytest-cov", "pytest-mock"]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("Missing test dependencies:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall with: poetry install --with dev")
        return False

    return True


def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(
        description="Run tests for Math Expert LLM Application"
    )
    parser.add_argument(
        "test_type",
        nargs="?",
        default="all",
        choices=["unit", "integration", "performance", "fast", "all"],
        help="Type of tests to run",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--no-coverage", action="store_true", help="Disable coverage reporting"
    )
    parser.add_argument(
        "-p", "--parallel", action="store_true", help="Run tests in parallel"
    )
    parser.add_argument(
        "--check-deps", action="store_true", help="Check test dependencies"
    )

    args = parser.parse_args()

    if args.check_deps:
        if check_dependencies():
            print("All test dependencies are installed ✓")
            return True
        else:
            return False

    # Check dependencies before running tests
    if not check_dependencies():
        return False

    print(f"Running {args.test_type} tests...")

    success = run_tests(
        test_type=args.test_type,
        verbose=args.verbose,
        coverage=not args.no_coverage,
        parallel=args.parallel,
    )

    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
