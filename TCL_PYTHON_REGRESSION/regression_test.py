"""REGRESSION TESTING : is a type of software testing
that verifies that changes made to that system,
such as bug fixes or new features,
do not impact previously workking functionalities """

def add(a, b):
    """Function to add two numbers."""
    return a + b
def test_add():
    """Test cases for the add function."""
    assert add(1,3) == 3  # Test case 1: 1 + 2 should equal 3
    assert add(-1, 1) == 0  # Test case 2: -1 + 1 should equal 0
    assert add(10, -5) == 5  # Test case 3: 10 + (-5) should equal 5

    # Add more test cases as needed...

# Run the regression tests
test_add()
# Print a message after running the tests
print("Regression tests completed.")
