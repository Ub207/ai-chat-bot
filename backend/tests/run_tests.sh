#!/bin/bash

# Test runner script for AI Chat Bot backend tests
# Run all tests and display clear pass/fail results

set -e  # Exit immediately if a command exits with a non-zero status

echo "==========================================="
echo "AI Chat Bot Backend Test Suite"
echo "==========================================="
echo ""

# Change to the project root directory
cd "$(dirname "$0")/../.."

# Function to run tests and report results
run_test_suite() {
    local suite_name=$1
    local test_file=$2

    echo "🧪 Running $suite_name..."
    echo "------------------------------------------"

    if python -m pytest "$test_file" -v; then
        echo "✅ $suite_name: PASSED"
        echo ""
        return 0
    else
        echo "❌ $suite_name: FAILED"
        echo ""
        return 1
    fi
}

# Initialize counters
total_suites=0
passed_suites=0

# Run MCP Tools tests
total_suites=$((total_suites + 1))
if run_test_suite "MCP Tools Tests" "backend/tests/test_mcp_tools.py"; then
    passed_suites=$((passed_suites + 1))
fi

# Run Chat Endpoint tests
total_suites=$((total_suites + 1))
if run_test_suite "Chat Endpoint Tests" "backend/tests/test_chat_endpoint.py"; then
    passed_suites=$((passed_suites + 1))
fi

echo "==========================================="
echo "TEST SUMMARY"
echo "==========================================="
echo "Total test suites: $total_suites"
echo "Passed: $passed_suites"
echo "Failed: $((total_suites - passed_suites))"
echo ""

if [ $passed_suites -eq $total_suites ]; then
    echo "🎉 ALL TESTS PASSED!"
    exit 0
else
    echo "⚠️  SOME TESTS FAILED!"
    exit 1
fi