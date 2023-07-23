import re


def convert_to_function(code):
    """
    Converts the given JavaScript code string into a function string.

    Arguments:
    code (str): The JavaScript code string to convert.

    Returns:
    (str): The converted JavaScript function string.
    """

    # This regular expression matches any occurrence of "arguments[i]" in the code,
    # where "i" is a digit. It's used to identify and extract the arguments.
    argument_regex = re.compile(r"arguments\[(\d+)\]")

    # The args list will hold the names of the function arguments to be used in the
    # converted code. We initialize it as an empty list.
    args = []

    # For each match of the regular expression in the code, we add an argument
    # named "argumenti" to the args list, where "i" is the digit matched by the regular
    # expression. This effectively extracts the argument names.
    for match in re.finditer(argument_regex, code):
        args.append(f"argument{match.group(1)}")

    # We use the sub function to replace all occurrences of "arguments[i]" in the
    # code with "argumenti". The lambda function passed to sub is called with each
    # match object, and it returns the replacement string.
    new_code = re.sub(argument_regex, lambda match: f"argument{match.group(1)}", code)

    # Finally, we generate the JavaScript function string. The arguments of the function
    # are the elements of the args list, joined by commas. The body of the function is the
    # new_code string, which is the original code with "arguments[i]" replaced by "argumenti".
    result = f"function ({', '.join(args)}) {{\n{new_code}\n}}"

    # The resulting function string is returned.
    return result
