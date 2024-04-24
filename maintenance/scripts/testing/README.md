# IOF Maintenance Reference Ontology Tests

## Environment Setup


1. Install `virtualenv`

    ```
    pip install virtualenv
    ```

2. Create a virtual environment (named "env" or choose a different name):

    ```
    python -m venv env
    ```

3. Activate the virtual environment
  
- On Windows:

  ```
  env\Scripts\activate
  ```

- On macOS/Linux:

  ```
  source env/bin/activate
  ```
  
4. Install Dependencies from `requirements.txt`

    ```
    pip install -r requirements.txt
    ```

## Running Individual Tests

Individual tests (per class) can be run using the command

```
python maintenance/scripts/testing/tests/{TESTNAME}.py
```

For example, to run the tests for the Degraded State class execute 

```
python maintenance/scripts/testing/tests/test_DegradedState.py
```

## Running All Tests 

To run all tests (for all 20 classes) execute

```
maintenance/scripts/testing/tests/testing.sh
```