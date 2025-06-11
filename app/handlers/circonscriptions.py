from typing import Any

from marshmallow import Schema, fields
from sqlalchemy import select, func, and_

from app.db import session_scope
from app.handlers.departements import DepartementSchema
from app.models.depute import Circonscription, Departement
from app.utils.db import pagined_query, query_one


class CirconscriptionSchema(Schema):
    """Schema for the Circonscription model."""

    code = fields.String()
    departement = fields.Nested(DepartementSchema)
    url = fields.String()


def circonscriptions_get_handler() -> Any:
    """
    Get a list of all Circonscription records.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the Circonscription records.
    """
    with session_scope() as session:
        stmt = select(Circonscription)
        stmt_count = select(func.count()).select_from(Circonscription)
        return pagined_query(
            session,
            stmt,
            stmt_count,
            CirconscriptionSchema(many=True),
            Circonscription.departement_code,
        )


def circonscription_get_handler(
    departement_code: str, circonscription_code: str
) -> Any:
    """
    Get a single Circonscription record by its code and the code of its associated Departement.

    Args:
        departement_code (str): The code of the Departement record to search for Circonscription records in.
        circonscription_code (str): The code of the Circonscription record to retrieve.

    Returns:
        Dict[str, str]: A dictionary representing the Circonscription record that was retrieved.
    """
    with session_scope() as session:
        return query_one(
            session,
            Circonscription,
            and_(
                Circonscription.code == circonscription_code,
                Circonscription.departement_code == departement_code,
            ),
            CirconscriptionSchema(),
        )


def circonscriptions_by_departement_handler(department_code: str) -> Any:
    """
    Get a single Departement record by its code.

    Args:
        department_code (str): The code of the Departement record to retrieve.

    Returns:
        Dict[str, str]: A dictionary representing the Departement record that was retrieved.
    """
    with session_scope() as session:
        return query_one(
            session,
            Departement,
            and_(Departement.code == department_code),
            DepartementSchema(),
        )
