#!/bin/bash

cd "$(dirname "$0")"

# Use the project virtual environment if there is one
if [ -f ".venv/bin/activate" ]; then
    source ".venv/bin/activate"
fi

echo "Looking for test files..."

# Directory where your test files are stored
TEST_DIR="tests"
failed=0

# Loop through all test_*.py files in the tests directory
for test_path in "$TEST_DIR"/test_*.py; do
    test_file=$(basename "$test_path")
    test_module="${test_file%.py}"
    module_path="${TEST_DIR}.${test_module}"

    # Tests report results by printing ✅/❌, so check the output as well as the exit code
    if ! output=$(python3 -m "$module_path" 2>&1); then
        failed=1
    fi
    echo "$output"
    if grep -q "❌" <<< "$output"; then
        failed=1
    fi
done

if [ "$failed" -ne 0 ]; then
    echo "❌ Some tests failed."
    exit 1
fi

echo "✅ All tests passed!"
