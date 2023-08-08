from typing import List


def initialize_matrix(rows, cols):
    """
    Initialize a matrix for the Wagner-Fischer algorithm.

    Args:
    rows (int): Number of rows in the matrix, corresponding to the length of the first string plus one.
    cols (int): Number of columns in the matrix, corresponding to the length of the second string plus one.

    Returns:
    list: A 2D list (matrix) initialized with zeros.
    """
    return [[0 for _ in range(cols)] for _ in range(rows)]


def initialize_base_distance_cost(matrix, actual, expected):
    """
    Initialize the base distance costs in the Wagner-Fischer matrix.

    This method sets up the initial values for the edit distance matrix, which are based on the lengths
    of the input sequences (actual and expected). The first row and the first column of the matrix are
    initialized with incremental values starting from 0. This represents the cost of converting a string
    of length n to an empty string (or vice versa) through deletions (or insertions).

    Args:
    matrix (list of list of int): The matrix used in the Wagner-Fischer algorithm. It should be
                                  initialized with zeroes and have dimensions
                                  (len(actual) + 1) x (len(expected) + 1).
    actual (str or list): The actual string or list of elements. Used to determine the operations made on each element.
    expected (str or list): The expected string or list of elements. Compared against the actual sequence.

    Returns:
    None: The function modifies the matrix in place and does not return anything.

    Example:
    >>> matrix = initialize_matrix(4, 5) # For strings of length 3 and 4
    >>> initialize_base_distance_cost(matrix, [1, 2, 3], [2, 3, 4, 5])
    >>> matrix
    [[0, 1, 2, 3, 4], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0]]

    Note:
    - The function assumes that the matrix is already initialized with the correct dimensions.
    - This method is typically called at the beginning of the Wagner-Fischer algorithm to set up the
      initial conditions for the dynamic programming approach.
    """
    for i in range(len(actual) + 1):
        matrix[i][0] = i
    for j in range(len(expected) + 1):
        matrix[0][j] = j


def calculate_distances(matrix, actual, expected):
    """
    Populate the matrix with the edit distances between substrings of the actual and expected strings.

    This function implements the Wagner-Fischer algorithm to compute the edit distances,
    which are used to determine the minimum number of edits (insertions, deletions, substitutions)
    needed to transform the actual string into the expected string.

    Args:
    matrix (list): The initialized matrix.
    actual (str or list): The actual string or list of elements. Used to determine the operations made on each element.
    expected (str or list): The expected string or list of elements. Compared against the actual sequence.
    """
    for i in range(1, len(actual) + 1):
        for j in range(1, len(expected) + 1):
            diff = 0 if actual[i - 1] == expected[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + diff
            )


def handle_deletion(i, j):
    """
    Determine the indices and character representation for a deletion operation.

    Args:
    i (int): The current row index in the matrix.
    j (int): The current column index in the matrix.

    Returns:
    tuple: Updated indices (i, j) and the character '-' representing a deletion.
    """
    return i - 1, j, "-"


def handle_addition(i, j):
    """
    Determine the indices and character representation for an addition operation.

    Args:
    i (int): The current row index in the matrix.
    j (int): The current column index in the matrix.

    Returns:
    tuple: Updated indices (i, j) and the character '+' representing an addition.
    """
    return i, j - 1, "+"


def handle_substitution(i, j, actual, expected):
    """
    Determine the indices and character representation for a substitution operation.

    Args:
    i (int): The current row index in the matrix.
    j (int): The current column index in the matrix.
    actual (str or list): The actual string or list of elements. Used to determine the operations made on each element.
    expected (str or list): The expected string or list of elements. Compared against the actual sequence.

    Returns:
    tuple: Updated indices (i, j) and the character '^' representing a substitution, or a character from the actual string if no substitution is needed.
    """
    if actual[i - 1] != expected[j - 1]:
        return i - 1, j - 1, "^"
    else:
        return i - 1, j - 1, actual[i - 1]


def is_deletion(matrix, i, j):
    """
    Check if the current matrix position indicates a deletion operation.

    Args:
    matrix (list): The matrix containing edit distances.
    i (int): The current row index in the matrix.
    j (int): The current column index in the matrix.

    Returns:
    bool: True if the current operation is a deletion, False otherwise.
    """
    return i > 0 and matrix[i][j] == matrix[i - 1][j] + 1


def is_addition(matrix, i, j):
    """
    Check if the current matrix position indicates an addition operation.

    Args:
    matrix (list): The matrix containing edit distances.
    i (int): The current row index in the matrix.
    j (int): The current column index in the matrix.

    Returns:
    bool: True if the current operation is an addition, False otherwise.
    """
    return j > 0 and matrix[i][j] == matrix[i][j - 1] + 1


def need_to_process(i, j):
    """
    Determine if there are more operations to process in the matrix.

    Args:
    i (int): The current row index in the matrix.
    j (int): The current column index in the matrix.

    Returns:
    bool: True if more operations need to be processed, False otherwise.
    """
    return (i > 0 and j > 0) or (i == 0) ^ (j == 0)


def trace_operations(matrix, actual, expected, result, i, j):
    """
    Trace the operations from the bottom-right to the top-left of the matrix, constructing the difference string.

    Args:
    matrix (list): The matrix containing edit distances.
    actual (str or list): The actual string or list of elements. Used to determine the operations made on each element.
    expected (str or list): The expected string or list of elements. Compared against the actual sequence.
    result (list): The list to store the result characters.
    i (int): The starting row index for tracing back.
    j (int): The starting column index for tracing back.
    """
    while need_to_process(i, j):
        if is_deletion(matrix, i, j):
            i, j, char = handle_deletion(i, j)
        elif is_addition(matrix, i, j):
            i, j, char = handle_addition(i, j)
        else:
            i, j, char = handle_substitution(i, j, actual, expected)
        result.append(str(char))


def reconstruct_string(matrix, actual, expected, delimiter: str = ""):
    """
    Reconstruct the difference string from the distance matrix.

    This function creates a string that represents the differences between the actual and expected strings,
    using the Wagner-Fischer algorithm. The differences are denoted by '+' (addition), '-' (deletion), and '^' (substitution).
    The resulting string is composed of these symbols and the unchanged elements from the actual string, separated
    by the specified delimiter.

    Args:
    matrix (list of list of int): The matrix containing edit distances. It is filled by the Wagner-Fischer algorithm.
    actual (str or list): The actual string or list of elements. Used to determine the operations made on each element.
    expected (str or list): The expected string or list of elements. Compared against the actual sequence.
    delimiter (str): The delimiter to use between items in the reconstructed string. Defaults to an empty string (''),
                     which concatenates the items directly without any separator. A common alternative is a comma (',')
                     for clearer separation of items.

    Returns:
    str: The reconstructed string showing the differences, with items separated by the specified delimiter.
    """
    result: List[str] = []
    i, j = len(actual), len(expected)

    trace_operations(matrix, actual, expected, result, i, j)

    return delimiter.join(reversed(result))


def generate_distance_matrix(actual, expected):
    """
    Generate the distance matrix using the Wagner-Fischer algorithm for the given strings.

    This function initializes the matrix and calculates the edit distances between
    substrings of the actual and expected strings.

    Args:
    actual (str or list): The actual string or list of elements. Used to determine the operations made on each element.
    expected (str or list): The expected string or list of elements. Compared against the actual sequence.

    Returns:
    list: The matrix filled with edit distances.
    """
    matrix = initialize_matrix(len(actual) + 1, len(expected) + 1)

    # Initialize base distance costs
    initialize_base_distance_cost(matrix, actual, expected)

    calculate_distances(matrix, actual, expected)

    return matrix


def string_diff(actual, expected):
    """
    Calculate the string difference between two strings using the Wagner-Fischer algorithm.

    This function determines the minimum number of single-character edits (insertions, deletions, or substitutions)
    required to change one string into the other and represents these changes in a resultant string.

    Args:
    actual (str): The actual string.
    expected (str): The expected string.

    Returns:
    str: The string representing the differences with specific symbols ('+', '-', '^').
    """
    matrix = generate_distance_matrix(actual, expected)
    return reconstruct_string(matrix, actual, expected)


def array_diff(actual, expected):
    """
    Calculate the differences between two arrays using the Wagner-Fischer algorithm.

    This function determines the minimum number of edits (insertions, deletions, or substitutions)
    required to transform one array into another. The differences are expressed in a string format,
    where each edit operation is represented by a specific symbol: '+' for insertions, '-' for deletions,
    and '^' for substitutions. Unchanged elements are included as they are. The result is a concise
    representation of how to modify the 'actual' array to match the 'expected' array.

    The output is formatted as a string representing a list, with each element separated by commas
    and enclosed in square brackets. This format makes it easy to understand the sequence of operations
    and elements.

    Args:
    actual (list): The original array to compare. It can contain elements of any type that supports equality comparison.
    expected (list): The target array to compare against. It should contain elements of a comparable type to 'actual'.

    Returns:
    str: A string representing the list of operations and elements that show how to transform 'actual' into 'expected'.
         For example, "[0, 1, -, +, +]" indicates that to transform 'actual' into 'expected', we keep the first two elements (0, 1),
         delete the next element from 'actual', and then insert two new elements from 'expected'.

    Example:
    >>> actual = [0, 1, 2, 3]
    >>> expected = [0, 1, 3, 4]
    >>> array_diff(actual, expected)
    "[0, 1, ^, +, +]"
    """
    matrix = generate_distance_matrix(actual, expected)
    return f"[{reconstruct_string(matrix, actual, expected, ', ')}]"
