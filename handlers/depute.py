

from typing import Sequence
from typing_extensions import Any
from flask import jsonify
from sqlalchemy.sql import select

from db import session_scope
from models.depute import Departement, Depute
from marshmallow import Schema, fields

from utils.db import get_all_records, get_record_filter


class DepartementSchema(Schema):
    code = fields.String()
    name = fields.String()
    url = fields.Str(required=True)

class CirconscriptionSchema(Schema):
    code = fields.String()
    departement = fields.Nested(DepartementSchema)
    url = fields.Str(required=True)

class DeputeSchema(Schema):
    id = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    image = fields.Str(required=True)
    official_page = fields.Str(required=True)
    official_image = fields.Str(required=True)
    circonscription = fields.Nested(CirconscriptionSchema)
    url = fields.Str(required=True)



def deputes_get_handler() -> Any:
    with session_scope() as session:
        return get_all_records(session, Depute, DeputeSchema(many=True))


def depute_get_handler(depute_id: str) -> Any:
    with session_scope() as session:
        stmt = select(Depute).where(Depute.id == depute_id)
        result = session.execute(stmt)
        record = result.scalars().first()
        if record:
            return DeputeSchema().dump(record)
        return None

def departements_get_handler() -> Any:
    with session_scope() as session:
        return get_all_records(session, Departement, DepartementSchema(many=True))

def departement_get_handler(department_code: str) -> Any:
    with session_scope() as session:
        stmt = select(Departement).where(Departement.code == department_code)
        result = session.execute(stmt)
        record = result.scalars().first()
        if record:
            return DepartementSchema().dump(record)
        return None

def deputes_by_departement_handler(department_code: str):
    with session_scope() as session:
        stmt = select(Depute).where(Depute.circonscription_departement_code == department_code)
        result = session.execute(stmt)
        record = result.scalars().first()
        if record:
            return DeputeSchema().dump(record)
        return None
