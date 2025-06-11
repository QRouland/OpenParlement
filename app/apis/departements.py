from flasgger import swag_from
from flask import jsonify, abort

from app import main_bp
from app.handlers.departements import departements_get_handler, departement_get_handler


# =======================
# Départements
# =======================

@main_bp.route("/departements", methods=["GET"])
@swag_from("../../specs/departements.yml")
def departements_get():
    """
    Get the list of all départements.
    """
    return jsonify(departements_get_handler()), 200


@main_bp.route("/departements/<string:departement_code>", methods=["GET"])
@swag_from("../../specs/departement.yml")
def departement_get(departement_code):
    """
    Get a département.
    """
    departement = departement_get_handler(departement_code)

    if departement:
        return jsonify(departement), 200

    abort(404, description=f"Département with code '{departement_code}' not found.")
