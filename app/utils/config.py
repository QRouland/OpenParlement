def str_to_bool(value):
    """
    Convert a string to a boolean.

    :param value: The string value to convert.
    :return: True if the string represents a truthy value, False otherwise.
    :raises ValueError: If the string is not a valid truthy or falsy value.
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError(f'Invalid truth value "{value}"')

def str_to_int(value):
    """
    Convert a string to an integer.

    :param value: The string value to convert.
    :return: The integer representation of the string.
    :raises ValueError: If the string cannot be converted to an integer.
    """
    try:
        return int(value)
    except ValueError:
        raise ValueError(f'Invalid integer value "{value}"')
