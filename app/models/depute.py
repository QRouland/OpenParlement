from sqlalchemy import String, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models import Base
from app.utils.db import normalize_field


class Depute(Base):
    """
    Represents a deputy (député) with identification, constituency, and group affiliations.

    Attributes:
        id (str): Unique identifier for the deputy.
        last_name (str): Deputy's last name.
        last_name_normalize (str): Normalized last name (lowercase, accent-free).
        first_name (str): Deputy's first name.
        first_name_normalize (str): Normalized first name (lowercase, accent-free).
        gp_id (int): Foreign key linking to the parliamentary group.
        gp (GroupParlementaire): Relationship to the deputy's group.
        circonscription_departement_code (str): Department number of the constituency.
        circonscription_code (int): Constituency number within the department.
        circonscription (Circonscription): Relationship to the constituency.
    """

    __tablename__ = "depute"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)

    last_name: Mapped[str] = mapped_column(String(255))
    last_name_normalize: Mapped[str] = mapped_column(
        String(255),
        default=normalize_field("last_name"),
        onupdate=normalize_field("last_name"),
        index=True,
    )

    first_name: Mapped[str] = mapped_column(String(255))
    first_name_normalize: Mapped[str] = mapped_column(
        String(255),
        default=normalize_field("first_name"),
        onupdate=normalize_field("first_name"),
        index=True,
    )

    gp_id: Mapped[int] = mapped_column(ForeignKey("groupe_parlementaire.id"))
    gp: Mapped["GroupParlementaire"] = relationship(back_populates="members")

    circonscription_departement_code: Mapped[str] = mapped_column(String(32))
    circonscription_code: Mapped[int] = mapped_column(Integer())
    circonscription: Mapped["Circonscription"] = relationship(
        back_populates="representative"
    )

    votes: Mapped[list["Vote"]] = relationship(back_populates="depute")

    __table_args__ = (
        ForeignKeyConstraint(
            ["circonscription_departement_code", "circonscription_code"],
            ["circonscription.departement_code", "circonscription.code"],
        ),
        {},
    )

    @property
    def official_page(self) -> str:
        """
        URL to the official page of the deputy.

        Returns:
            str: Web URL to the deputy's profile.
        """
        return f"https://www.assemblee-nationale.fr/dyn/deputes/{self.id}"

    @property
    def official_image(self) -> str:
        """
        URL to the deputy's official portrait image.

        Returns:
            str: Image URL of the deputy.
        """
        return f"https://www.assemblee-nationale.fr/dyn/static/tribun/17/photos/carre/{self.id[2:]}.jpg"


class GroupParlementaire(Base):
    """
    Represents a parliamentary group (groupe parlementaire).

    Attributes:
        id (str): Unique identifier of the group.
        name (str): Name of the parliamentary group.
        members (list[Depute]): Deputies associated with the group.
    """

    __tablename__ = "groupe_parlementaire"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)

    members: Mapped[list["Depute"]] = relationship(back_populates="gp")


class Circonscription(Base):
    """
    Represents an electoral district (circonscription).

    Attributes:
        departement_code (str): Foreign key to the related department.
        departement (Departement): Department this constituency belongs to.
        code (int): Constituency number within the department.
        representative (Depute): Deputy representing this constituency.
    """

    __tablename__ = "circonscription"

    departement_code: Mapped[str] = mapped_column(
        ForeignKey("departement.code"), primary_key=True
    )
    departement: Mapped["Departement"] = relationship(back_populates="circonscriptions")

    code: Mapped[int] = mapped_column(Integer(), primary_key=True)

    representative: Mapped["Depute"] = relationship(back_populates="circonscription")


class Departement(Base):
    """
    Represents a French administrative department.

    Attributes:
        code (str): Unique identifier for the department.
        name (str): Name of the department.
        region_id (int): Foreign key to the associated region.
        region (Region): Region this department belongs to.
        circonscriptions (list[Circonscription]): Constituencies in the department.
    """

    __tablename__ = "departement"

    code: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)

    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    region: Mapped["Region"] = relationship(back_populates="departements")

    circonscriptions: Mapped[list["Circonscription"]] = relationship(
        back_populates="departement"
    )


class Region(Base):
    """
    Represents a French administrative region.

    Attributes:
        id (int): Unique identifier of the region.
        name (str): Name of the region.
        departements (list[Departement]): Departments within the region.
    """

    __tablename__ = "region"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    departements: Mapped[list["Departement"]] = relationship(back_populates="region")
