from flask import request
from sqlalchemy.sql import func, select
from typing_extensions import Any, Callable

from config_default import MAX_PER_PAGE
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


def get_paginated_records(session, model,  schema, order_by=None) -> Any:
    stmt = select(model)
    stmt_count = select(func.count(model.id))
    return pagined_query(session, stmt, stmt_count, order_by)

def query_one(session, model, filter, schema) -> Any | None:
    per_page = int(request.args.get('per_page', MAX_PER_PAGE))

    stmt = select(model).where(filter)
    result = session.execute(stmt)
    record = result.scalars().first()
    if record:
        return {
            'data': schema.dump(record),
            'meta': {
                'current_page': 1,
                'per_page': per_page,
                'total_items': 1,
                'total_pages': 1
            }
        }
    return None

def pagined_query(session, stmt_query, stmt_count, schema, order_by=None):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', MAX_PER_PAGE))

    if per_page > MAX_PER_PAGE:
        per_page = MAX_PER_PAGE

    stmt_query = stmt_query.order_by(order_by).offset((page - 1) * per_page).limit(per_page)
    total_items = session.execute(stmt_count).scalar_one()
    result = session.execute(stmt_query)
    records = result.scalars().all()
    return {
        'data': schema.dump(records),
        'meta': {
            'current_page': page,
            'per_page': per_page,
            'total_items': total_items,
            'total_pages': len(records)
        }
    }
