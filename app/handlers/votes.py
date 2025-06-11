from marshmallow import Schema, fields
from sqlalchemy import select, func, and_
from typing_extensions import Any

from app.db import session_scope
from app.models.scrutin import Vote, Scrutin, Ballot
from app.utils.db import pagined_query, query_one


class VoteSchema(Schema):
    """Schema for the Vote model."""

    depute_id = fields.String()
    scrutin_id = fields.String()
    ballot = fields.String()


def votes_get_handler() -> Any:
    """
    Retrieve a paginated list of all Vote records.

    :return: Paginated query result of Vote records.
    """
    with session_scope() as session:
        stmt = select(Vote)
        stmt_count = select(func.count()).select_from(Vote)
        return pagined_query(
            session, stmt, stmt_count, VoteSchema(many=True), Vote.scrutin_id
        )


def vote_get_handler(vote_id: str) -> Any:
    """
    Retrieve a single Vote record by its depute ID.

    :param vote_id: The depute ID of the Vote to retrieve.
    :return: Single Vote record.
    """
    with session_scope() as session:
        return query_one(session, Vote, and_(Vote.depute_id == vote_id), VoteSchema())


def depute_votes_get_handler(depute_id: str) -> Any:
    """
    Retrieve a paginated list of Vote records for a specific depute.

    :param depute_id: The ID of the depute to filter Vote records.
    :return: Paginated query result of Vote records for the specified depute.
    """
    with session_scope() as session:
        stmt = select(Vote).where(Vote.depute_id == depute_id)
        stmt_count = (
            select(func.count()).select_from(Vote).where(Vote.depute_id == depute_id)
        )
        return pagined_query(
            session, stmt, stmt_count, VoteSchema(many=True), Vote.scrutin_id
        )


def depute_scrutin_vote_get_handler(depute_id: str, scrutin_id: str) -> Any:
    """
    Retrieve a single Vote record by its depute and scrutin IDs.

    :param depute_id: The ID of the depute to filter the Vote.
    :param scrutin_id: The ID of the scrutin to filter the Vote.
    :return: Single Vote record for the specified depute and scrutin.
    """
    with session_scope() as session:
        return query_one(
            session,
            Vote,
            and_(Vote.depute_id == depute_id, Vote.scrutin_id == scrutin_id),
            VoteSchema(),
        )


def scrutin_votes_get_handler():
    raise NotImplemented


def depute_votes_stats_get_handler(depute_id: str) -> Any:
    with session_scope() as session:
        # Count of each Ballot type
        ballot_counts_stmt = (
            select(
                Vote.ballot,
                func.count().label("count")
            )
            .where(Vote.depute_id == depute_id)
            .group_by(Vote.ballot)
        )

        # Subquery for scrutins the depute has participated in
        participated_scrutins_subq = (
            select(Vote.scrutin_id)
            .where(Vote.depute_id == depute_id)
            .subquery()
        )

        # Number of non-participations (no vote cast in a scrutin)
        non_participation_stmt = (
            select(func.count())
            .select_from(Scrutin)
            .where(~Scrutin.id.in_(participated_scrutins_subq))
        )

        # Execute
        ballot_counts = dict(session.execute(ballot_counts_stmt).all())
        non_participation = session.execute(non_participation_stmt).scalar()

        # Combine
        data = {
            "pour": ballot_counts.get(Ballot.POUR, 0),
            "contre": ballot_counts.get(Ballot.CONTRE, 0),
            "abstention": ballot_counts.get(Ballot.ABSTENTION, 0),
            "nonvotant": ballot_counts.get(Ballot.NONVOTANT, 0),
            "absent": non_participation
        }

        return {
            'data': data,
            'meta': {
                'current_page': 1,
                'per_page': 1,
                'total_items': 1,
                'total_pages': 1
            }
        }
