from typing import Any

from marshmallow import Schema, fields
from sqlalchemy import select, func, and_

from app.db import session_scope
from app.models.depute import Departement
from app.utils.db import pagined_query, query_one


class DepartementSchema(Schema):
    """Schema for the Departement model."""

    code = fields.String()
    name = fields.String()
    url = fields.Str()


def departements_get_handler() -> Any:
    """
    Get a list of all Departement records.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the Departement records.
    """
    with session_scope() as session:
        stmt = select(Departement)
        stmt_count = select(func.count()).select_from(Departement)
        return pagined_query(
            session, stmt, stmt_count, DepartementSchema(many=True), Departement.code
        )


def departement_get_handler(departement_code: str) -> Any:
    """
    Get a single Departement record by its code.

    Args:
        departement_code (str): The coete of the Departement record to retrieve.

    Returns:
        Dict[str, str] :  A dictionary representing the Departement record that was retrieved.
    """
    with session_scope() as session:
        return query_one(session, Departement, and_(Departement.code == departement_code), DepartementSchema())
