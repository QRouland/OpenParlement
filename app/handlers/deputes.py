from typing import Any

from marshmallow import Schema, fields
from sqlalchemy.sql import func, select
from sqlalchemy.sql.expression import and_

from app.db import session_scope
from app.models.depute import Circonscription, Departement, Depute
from app.utils import normalize
from app.utils.db import pagined_query, query_one


class DepartementSchema(Schema):
    """Schema for the Departement model."""

    code = fields.String()
    name = fields.String()
    url = fields.Str()


class CirconscriptionSchema(Schema):
    """Schema for the Circonscription model."""

    code = fields.String()
    departement = fields.Nested(DepartementSchema)
    url = fields.Str()


class DeputeSchema(Schema):
    """Schema for the Depute model."""

    id = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    image = fields.Str()
    official_page = fields.Str()
    official_image = fields.Str()
    circonscription = fields.Nested(CirconscriptionSchema)
    url = fields.Str()


def deputes_get_handler(first_name=None, last_name=None) -> Any:
    """
    Get a list of Depute records that match the given first and/or last name.

    Args:
        first_name (str): The first name to search for.
        last_name (str): The last name to search for.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the Depute records that matched the search criteria.
    """
    with session_scope() as session:
        stmt = select(Depute)
        stmt_count = select(func.count()).select_from(Depute)
        if first_name is not None:
            stmt = stmt.where(
                Depute.first_name_normalize == f"{normalize(first_name)}"
            )
            stmt_count = stmt_count.where(
                Depute.first_name_normalize == f"{normalize(first_name)}"
            )
        if last_name is not None:
            stmt = stmt.where(
                Depute.last_name_normalize == f"{normalize(last_name)}"
            )
            stmt_count = stmt_count.where(
                Depute.last_name_normalize == f"{normalize(last_name)}"
            )

        return pagined_query(
            session, stmt, stmt_count, DeputeSchema(many=True), Depute.last_name
        )


def depute_get_handler(depute_id: str) -> Any:
    """
    Get a single Depute record by its ID.

    Args:
        depute_id (str): The ID of the Depute record to retrieve.

    Returns:
        Dict[str, str]: A dictionary representing the Depute record that was retrieved.
    """
    with session_scope() as session:
        return query_one(session, Depute, and_(Depute.id == depute_id), DeputeSchema())


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


def departement_get_handler(department_code: str) -> Any:
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


def deputes_by_departement_handler(department_code: str) -> Any:
    """
    Get a list of Depute records by the code of their associated Departement.

    Args:
        department_code (str): The code of the Departement record to search for Depute records in.

    Returns:
        List[Dict[str, str]]: A list of dictionaries representing the Depute records that matched the search criteria.
    """
    with session_scope() as session:
        stmt = select(Depute).where(
            Depute.circonscription_departement_code == department_code
        )
        stmt_count = (
            select(func.count())
            .select_from(Depute)
            .where(Depute.circonscription_departement_code == department_code)
        )
        return pagined_query(
            session, stmt, stmt_count, DeputeSchema(many=True), Depute.last_name
        )


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


def depute_by_circonscription_handler(
    department_code: str, circonscription_code: str
) -> Any:
    """
    Get a single Depute record by the code of their associated Circonscription and the code of its associated Departement.

    Args:
        departement_code (str): The code of the Departement record to search for Circonscription records in.
        circonscription_code (str): The code of the Circonscription record to search for Depute records in.

    Returns:
        Dict[str, str]: A dictionary representing the Depute record that was retrieved.
    """
    with session_scope() as session:
        return query_one(
            session,
            Depute,
            and_(
                Depute.circonscription_departement_code == department_code
                and Depute.circonscription_code == circonscription_code
            ),
            DeputeSchema(),
        )
