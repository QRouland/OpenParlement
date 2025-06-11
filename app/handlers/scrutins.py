from datetime import date

from marshmallow import fields
from marshmallow.schema import Schema
from sqlalchemy.sql import func, select
from sqlalchemy.sql.expression import and_
from typing_extensions import Any

from app.db import session_scope
from app.models.scrutin import Scrutin
from app.utils.db import pagined_query, query_one

class ScrutinSchema(Schema):
    """Schema for the Departement model."""

    id = fields.String()
    titre = fields.String()
    date_scrutin = fields.String()
    sort = fields.String()


def scrutins_get_handler(start_date: date = None, end_date: date = None) -> Any:
    """
    Retrieve a paginated list of Scrutin records based on optional start and end dates.

    :param start_date: Optional start date to filter records.
    :param end_date: Optional end date to filter records.
    :return: Paginated query result of Scrutin records.
    """
    with session_scope() as session:
        stmt = select(Scrutin)
        stmt_count = select(func.count()).select_from(Scrutin)
        if start_date:
            stmt = stmt.filter(Scrutin.date_scrutin >= start_date)
            stmt_count = stmt_count.filter(Scrutin.date_scrutin >= start_date)
        if end_date:
            stmt = stmt.filter(Scrutin.date_scrutin <= end_date)
            stmt_count = stmt_count.filter(Scrutin.date_scrutin <= end_date)

        return pagined_query(
            session,
            stmt,
            stmt_count,
            ScrutinSchema(many=True),
            Scrutin.date_scrutin.desc(),
        )

def scrutin_get_handler(scrutin_id: str) -> Any:
    """
    Retrieve a single Scrutin record by its ID.

    :param scrutin_id: The ID of the Scrutin to retrieve.
    :return: Single Scrutin record.
    """
    with session_scope() as session:
        return query_one(
            session, Scrutin, and_(Scrutin.id == scrutin_id), ScrutinSchema()
        )


