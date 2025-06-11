from typing import Any

from marshmallow import Schema, fields
from sqlalchemy import select, func

from app.db import session_scope
from app.models.depute import Departement
from app.utils.db import pagined_query


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


def departement_get_handler(departement_code) -> Any:
    raise NotImplementedError
