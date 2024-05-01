# IOF-Maint Tests

## Objective
The objective of this testing work is to ensure the correctness and consistency of simple equivalence, subclass, and disjoint relations within the IOF Maintenance Reference Ontology (Iof-Maint). This includes verifying that classes are correctly defined as subclasses of others, ensuring disjointness between certain classes, and validating the ontology's logical consistency using reasoning tools. The scope of testing is restricted to the Maintenance ontology and as a result relations between maintenance classes and classes from other ontologies within the IOF suite are not tested. Moreover, the tests defined here are limited to the simple cases of equivalence, subclass, and disjoint relations; thus the tests here cover 8 of the 20 classes.

## Testing Structure
The testing work can be found in the IOF Ontology repository (currently in branch *maint_testing*) under *maintenance/scripts/testing/*. There are three items of interest inside this folder; the first is *requirements.txt* which outlines the packages necessary for testing, *testing.sh* which automates the testing process for all classes, and the *tests/* subdirectory which contains the individual Python testing files, one per class within the ontology. An additional subdirectory *tests/utility/* contains a Python script for common testing utilities including functions for loading ontologies, running a Hermit reasoner, executing SPARQL queries, and clearing staging files.

## Testing Workflow
The testing workflow follows the framework provided by the standard Python unittest module. Each individual test within *tests/* is a class that inherits from the unittest.TestCase class. Within each test case class, the following methods are defined:

1. **Setup:** Initializes the testing environment. This includes loading the required ontologies and imports.
2. **Test Case(s):** Outlines the test case(s) for the given ontology class (*test_subclass*, *test_disjointness*, and/or *test_equivalence*). Each test case follows the standard workflow of Arrange, Act, Assert.
    - **Arrange:** Sets up the namespace and instances for testing, runs the Hermit reasoner to infer logical consequences.
    - **Act:** Queries the ontology.
    - **Assert:** Asserts the query result is aligned to the expected behavior of the ontology.
3. **Teardown:** Cleans up the test environment.

## An Example: Testing Maintenance State Classes
As an example, consider the MaintenanceState class within Iof-Maint, which is equivalent to one of its disjoint subclasses of DegradedState, FailedState, and OperatingState.

For MaintenanceState, the relevant test case is *test_equivalence*. This test ensures equivalence by verifying that every instance of maintenance state is either classified as exactly one degraded, failed, or operating state. This is achieved through the following steps:
1. **Arrange:** Sets up the namespace and creates direct instances of DegradedState, FailedState, and OperatingState. Runs the Hermit reasoner.
2. **Act:** Queries the ontology to retrieve instances of MaintenanceState.
3. **Assert:** Asserts that every instance in the query result is of type DegradedState, FailedState, or OperatingState.

For DegradedState, FailedState, and OperatingState, the relevant test cases are *test_subclass* and *test_disjointness*. These tests verify that an instance of one of the three state classes is classified as a maintenance state but not classified as an instance of the other two state classes. The workflow for these tests is similar to that of MaintenanceState. For example, the *test_subclass* for DegradedState is given below:
1. **Arrange:** Sets up the namespace and creates an instance of DegradedState. Runs the Hermit reasoner.
2. **Act:** Queries the ontology to retrieve instances of MaintenanceState.
3. **Assert:** Asserts that the query result is the DegradedState instance.

For *test_disjointness* of DegradedState:
1. **Arrange:** Sets up the namespace and creates an instance of DegradedState, of FailedState, and of OperatingState. Runs the Hermit reasoner.
2. **Act:** Queries the ontology to retrieve a boolean value indicating if all instances of DegradedState are disjoint from instances of OperatingState and FailedState.
3. **Assert:** Asserts that the boolean value returned is True, i.e. all instances are disjoint.

## Running the Tests
The tests can be run individually or all at once. A prerequisite to running the tests is installing the packages listed in the requirements.txt file (Owlready2, RDFLib, and UnitTest2). The recommended workflow is to install these inside a virtual environment and run the tests from there. The tests should be run from the top level of the ontology repository.

### Environment Setup


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

### Running Individual Tests
The individual tests (per class) can be run using the command:

```
python maintenance/scripts/testing/tests/{TESTNAME}.py
```

For example, to run the tests for the Degraded State class execute:

```
python maintenance/scripts/testing/tests/test_DegradedState.py
```

### Running All Tests 

All tests can be run by executing the shell script testing.sh:
```
maintenance/scripts/testing/testing.sh
```