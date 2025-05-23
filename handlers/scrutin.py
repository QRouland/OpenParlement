from sqlalchemy.sql import func, select
from sqlalchemy.sql.expression import and_
from typing_extensions import Any
from marshmallow import fields
from marshmallow.schema import Schema
from db import session_scope
from models.scrutin import Scrutin, Vote
from utils.db import pagined_query, query_one


class ScrutinSchema(Schema):
    """Schema for the Departement model."""
    id = fields.String()
    titre = fields.String()
    date_scrutin = fields.String()
    sort = fields.String()

class VoteSchema(Schema):
    """Schema for the Vote model."""
    depute_id = fields.String()
    scrutin_id = fields.String()
    ballot = fields.String()


def scrutins_get_handler() -> Any:
    with session_scope() as session:
        stmt = select(Scrutin)
        stmt_count = select(func.count()).select_from(Scrutin)
        return pagined_query(session, stmt, stmt_count, ScrutinSchema(many=True), Scrutin.date_scrutin.desc())


def scrutin_get_handler(scrutin_id: str) -> Any:
    with session_scope() as session:
        return query_one(session, Scrutin, and_(Scrutin.id == scrutin_id), ScrutinSchema())


def votes_get_handler() -> Any:
    with session_scope() as session:
        stmt = select(Vote)
        stmt_count = select(func.count()).select_from(Vote)
        return pagined_query(session, stmt, stmt_count, VoteSchema(many=True), Vote.scrutin_id)


def vote_get_handler(vote_id: str) -> Any:
    with session_scope() as session:
        return query_one(session, Vote, and_(Vote.depute_id == vote_id), VoteSchema())


def depute_votes_get_handler(depute_id : str) -> Any:
    with session_scope() as session:
        stmt = select(Vote).where(Vote.depute_id == depute_id)
        stmt_count = select(func.count()).select_from(Vote).where(Vote.depute_id == depute_id)
        return pagined_query(session, stmt, stmt_count, VoteSchema(many=True), Vote.scrutin_id)


def depute_scrutin_vote_get_handler(depute_id: str, scrutin_id: str) -> Any:
    with session_scope() as session:
        return query_one(session, Vote, and_(Vote.depute_id == depute_id, Vote.scrutin_id == scrutin_id), VoteSchema())
