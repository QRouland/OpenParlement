from flask import Blueprint

main_bp = Blueprint("main", __name__)
assemble_national_bp = Blueprint("assemble_national", __name__, url_prefix="/assemble-national")
