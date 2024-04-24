#!/bin/bash

# Define variables
TEST_DIR="$(dirname "$0")/"  # Directory containing the script
LOG_FILE="maintenance/scripts/testing/test_results.log"

# Run tests and redirect output to a log file
echo "Running tests..."
python -m unittest discover "$TEST_DIR" -v > "$LOG_FILE" 2>&1

# Display overview
echo "Test Results Overview:"
echo "----------------------"
cat "$LOG_FILE"
