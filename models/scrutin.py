from typing import Any, List
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Enum as SAEnum
from sqlalchemy.sql import func, select
from sqlalchemy.sql.sqltypes import Date

from models import Base


class Ballot(Enum):
    """Enum representing the possible voting results."""
    ABSENT = 0
    NONVOTANT = 1
    POUR = 2
    CONTRE = 3
    ABSTENTION = 4


class Scrutin(Base):
    """Represents a parliamentary vote session (scrutiny)."""
    __tablename__ = "scrutin"

    id: Mapped[str] = mapped_column(String(), primary_key=True)
    titre: Mapped[str] = mapped_column(String())
    date_scrutin: Mapped[Date] = mapped_column(Date())
    sort: Mapped[str] = mapped_column(String())
    type: Mapped[str] = mapped_column(String())
    votes: Mapped[List["Vote"]] = relationship(back_populates="scrutin")

    @hybrid_property
    def nombreVotants(self) -> int:
        """Number of deputies who voted (not ABSENT)."""
        return sum(1 for vote in self.votes if vote.vote_sort != Ballot.ABSENT)

    @nombreVotants.expression
    def nombreVotants(cls) -> Any:
        """SQL expression for nombreVotants."""
        return (
            select(func.count(Vote.id))
            .where(Vote.scrutin_id == cls.id)
            .scalar_subquery()
        )

    @hybrid_property
    def nonVotant(self) -> int:
        """Number of deputies marked as NONVOTANT."""
        return sum(1 for vote in self.votes if vote.vote_sort == Ballot.NONVOTANT)

    @nonVotant.expression
    def nonVotant(cls) -> Any:
        """SQL expression for nonVotant."""
        return (
            select(func.count(Vote.id))
            .where((Vote.scrutin_id == cls.id) & (Vote.vote_sort == Ballot.NONVOTANT))
            .scalar_subquery()
        )

    @hybrid_property
    def pour(self) -> int:
        """Number of POUR votes."""
        return sum(1 for vote in self.votes if vote.vote_sort == Ballot.POUR)

    @pour.expression
    def pour(cls) -> Any:
        """SQL expression for pour."""
        return (
            select(func.count(Vote.id))
            .where((Vote.scrutin_id == cls.id) & (Vote.vote_sort == Ballot.POUR))
            .scalar_subquery()
        )

    @hybrid_property
    def contre(self) -> int:
        """Number of CONTRE votes."""
        return sum(1 for vote in self.votes if vote.vote_sort == Ballot.CONTRE)

    @contre.expression
    def contre(cls) -> Any:
        """SQL expression for contre."""
        return (
            select(func.count(Vote.id))
            .where((Vote.scrutin_id == cls.id) & (Vote.vote_sort == Ballot.CONTRE))
            .scalar_subquery()
        )

    @hybrid_property
    def abstention(self) -> int:
        """Number of ABSTENTION votes."""
        return sum(1 for vote in self.votes if vote.vote_sort == Ballot.ABSTENTION)

    @abstention.expression
    def abstention(cls) -> Any:
        """SQL expression for abstention."""
        return (
            select(func.count(Vote.id))
            .where((Vote.scrutin_id == cls.id) & (Vote.vote_sort == Ballot.ABSTENTION))
            .scalar_subquery()
        )


class Vote(Base):
    """Represents an individual vote by a deputy."""
    __tablename__ = "vote"

    scrutin_id: Mapped[str] = mapped_column(ForeignKey("scrutin.id"), primary_key=True)
    scrutin: Mapped[Scrutin] = relationship(back_populates="votes")

    depute_id: Mapped[str] = mapped_column(ForeignKey("depute.id"), primary_key=True)
    depute: Mapped["Depute"] = relationship(back_populates="votes")

    ballot: Mapped[Ballot] = mapped_column(SAEnum(Ballot), nullable=False)
