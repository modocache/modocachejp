import inspect


def get_function_name():
    """Returns the name of the current function."""
    stack = inspect.stack()
    try:
        return stack[1][3]
    except IndexError:
        return None

