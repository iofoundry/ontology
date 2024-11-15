import os
import unittest

script_dir = os.path.dirname(os.path.abspath(__file__))
test_dir = os.path.join(script_dir, 'tests')
log_file = os.path.join(script_dir, 'test_results.log')

print("Running tests...\n")

with open(log_file, 'w') as log:
    loader = unittest.defaultTestLoader
    tests = loader.discover(test_dir)
    runner = unittest.TextTestRunner(stream=log, verbosity=2)
    runner.run(tests)

print("Test Results Overview:")
print("----------------------")
with open(log_file, 'r') as log:
    print(log.read())
