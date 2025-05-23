

def stmt_to_string(stmt):
    """
    Convert an SQLAlchemy statement to a string with bound parameters included.

    :param stmt: The SQLAlchemy statement object.
    :return: A string representation of the SQL query with literal binds.
    """
    return str(stmt.compile(compile_kwargs={"literal_binds": True})).replace("\n", "")