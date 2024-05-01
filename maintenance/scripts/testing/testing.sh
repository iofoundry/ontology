#!/bin/bash

# Define path to tests & where to save testing results 
TEST_DIR="$(dirname "$0")/tests" 
LOG_FILE="$(dirname "$0")/test_results.log"

# Run tests and redirect output to a log file
echo "Running tests..."
echo
python -m unittest discover "$TEST_DIR" -v > "$LOG_FILE" 2>&1

# Display testing results
echo "Test Results Overview:"
echo "----------------------"
cat "$LOG_FILE"
