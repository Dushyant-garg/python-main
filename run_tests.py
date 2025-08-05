#!/usr/bin/env python3
"""
Test runner script for the agents project
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Info:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def install_test_dependencies():
    """Install test dependencies"""
    print("📦 Installing test dependencies...")
    return run_command(
        "pip install -r requirements-test.txt",
        "Installing test dependencies"
    )


def run_unit_tests():
    """Run unit tests"""
    return run_command(
        "python -m pytest tests/ -m unit -v",
        "Running Unit Tests"
    )


def run_agent_tests():
    """Run agent-specific tests"""
    return run_command(
        "python -m pytest tests/ -m agent -v",
        "Running Agent Tests"
    )


def run_api_tests():
    """Run API endpoint tests"""
    return run_command(
        "python -m pytest tests/ -m api -v",
        "Running API Tests"
    )


def run_integration_tests():
    """Run integration tests"""
    return run_command(
        "python -m pytest tests/ -m integration -v",
        "Running Integration Tests"
    )


def run_all_tests_with_coverage():
    """Run all tests with coverage report"""
    return run_command(
        "python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80 -v",
        "Running All Tests with Coverage"
    )


def run_performance_tests():
    """Run performance tests"""
    return run_command(
        "python -m pytest tests/ -m performance -v",
        "Running Performance Tests"
    )


def run_slow_tests():
    """Run slow/integration tests"""
    return run_command(
        "python -m pytest tests/ -m slow -v",
        "Running Slow Tests"
    )


def lint_code():
    """Run code linting"""
    commands = [
        ("python -m flake8 app/ --max-line-length=120 --ignore=E501,W503", "Linting app/ directory"),
        ("python -m flake8 tests/ --max-line-length=120 --ignore=E501,W503", "Linting tests/ directory")
    ]
    
    results = []
    for command, description in commands:
        result = run_command(command, description)
        results.append(result)
    
    return all(results)


def generate_test_report():
    """Generate comprehensive test report"""
    print("\n" + "="*60)
    print("📊 GENERATING TEST REPORT")
    print("="*60)
    
    # Check if coverage HTML report exists
    coverage_dir = Path("htmlcov")
    if coverage_dir.exists():
        print(f"✅ Coverage report generated: {coverage_dir.absolute()}/index.html")
    else:
        print("❌ No coverage report found")
    
    # Check for pytest cache
    pytest_cache = Path(".pytest_cache")
    if pytest_cache.exists():
        print(f"📁 Pytest cache: {pytest_cache.absolute()}")
    
    print("\n📋 Test Categories:")
    categories = [
        ("unit", "Unit tests for individual functions and classes"),
        ("agent", "Tests for AI agent functionality"),
        ("api", "API endpoint tests"),
        ("integration", "Integration tests between components"),
        ("performance", "Performance and speed tests"),
        ("slow", "Slow tests that may take time")
    ]
    
    for category, description in categories:
        print(f"  🏷️  {category}: {description}")


def main():
    """Main test runner"""
    print("🚀 Agent Project Test Suite")
    print("="*60)
    
    # Check if we're in the right directory
    if not Path("app").exists():
        print("❌ Error: Run this script from the project root directory")
        sys.exit(1)
    
    # Parse command line arguments
    args = sys.argv[1:] if len(sys.argv) > 1 else ["all"]
    
    if "help" in args or "-h" in args:
        print("""
Usage: python run_tests.py [options]

Options:
  all           Run all tests with coverage (default)
  unit          Run unit tests only
  agent         Run agent tests only
  api           Run API tests only
  integration   Run integration tests only
  performance   Run performance tests only
  slow          Run slow tests only
  lint          Run code linting only
  install       Install test dependencies only
  
Examples:
  python run_tests.py              # Run all tests
  python run_tests.py unit api     # Run unit and API tests
  python run_tests.py lint         # Run linting only
""")
        return
    
    success_count = 0
    total_count = 0
    
    # Install dependencies if requested
    if "install" in args or "all" in args:
        total_count += 1
        if install_test_dependencies():
            success_count += 1
        else:
            print("❌ Failed to install dependencies")
            return
    
    # Run linting if requested
    if "lint" in args or "all" in args:
        total_count += 1
        if lint_code():
            success_count += 1
    
    # Run specific test categories
    test_functions = {
        "unit": run_unit_tests,
        "agent": run_agent_tests,
        "api": run_api_tests,
        "integration": run_integration_tests,
        "performance": run_performance_tests,
        "slow": run_slow_tests
    }
    
    # If "all" is specified, run comprehensive test suite
    if "all" in args:
        total_count += 1
        if run_all_tests_with_coverage():
            success_count += 1
    else:
        # Run specific test categories
        for test_name, test_func in test_functions.items():
            if test_name in args:
                total_count += 1
                if test_func():
                    success_count += 1
    
    # Generate report
    generate_test_report()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()