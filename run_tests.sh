#!/bin/bash

# Make sure script exits if any command fails
set -e
source ".venv/bin/activate"
echo "Looking for test files..."

# Directory where your test files are stored
TEST_DIR="tests"

# Loop through all test_*.py files in the tests directory
for test_path in "$TEST_DIR"/test_*.py; do
    test_file=$(basename "$test_path")
    test_module="${test_file%.py}"            
    module_path="${TEST_DIR}.${test_module}"  

    python3 -m "$module_path"
done

echo -e "✅ All tests completed!"
