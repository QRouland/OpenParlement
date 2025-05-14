from sqlalchemy.sql import select
from typing_extensions import Any, Callable

from utils import normalize


def normalize_field(field_name: str) -> Callable:
    """
    Returns a function that normalizes a given field from the SQLAlchemy context.

    Args:
        field_name (str): The name of the field to normalize.

    Returns:
        Callable: A function usable as a SQLAlchemy default/onupdate callable.
    """

    def _normalize(context) -> str:
        original_value = context.current_parameters.get(field_name)
        if original_value is None:
            raise Exception("Invalid filed name")
        return normalize(original_value)

    return _normalize


def get_all_records(session, model, schema) -> Any:
    stmt = select(model)
    result = session.execute(stmt)
    records = result.scalars().all()
    return schema.dump(records)



def get_record_filter(session, filter, model, schema) -> Any:
    stmt = select(model).where(filter)
    result = session.execute(stmt)
    record = result.scalars().first()
    if record:
        return schema.dump(record)
    return None
