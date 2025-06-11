from flasgger import swag_from
from flask import jsonify, abort

from app import main_bp
from app.handlers.circonscriptions import circonscriptions_get_handler, circonscription_get_handler, \
    circonscriptions_by_departement_handler


# =======================
# Circonscriptions
# =======================

@main_bp.route("/circonscriptions", methods=["GET"])
@swag_from("../../specs/circonscriptions.yml")
def circonscriptions_get():
    """
    Get the list of all circonscriptions.
    """
    return jsonify(circonscriptions_get_handler()), 200


@main_bp.route("/departements/<departement_code>/circonscriptions", methods=["GET"])
@swag_from("../../specs/circonscriptions_by_departement.yml")
def circonscriptions_by_departement_get(departement_code):
    """
    Get all circonscriptions for a specific département.
    """
    circonscriptions = circonscriptions_by_departement_handler(departement_code)
    if circonscriptions:
        return jsonify(circonscriptions), 200
    abort(404, description="No circonscriptions found for this département.")


@main_bp.route("/departements/<departement_code>/circonscriptions/<circonscription_code>", methods=["GET"])
@swag_from("../../specs/circonscription.yml")
def circonscription_get(departement_code, circonscription_code):
    """
    Get a specific circonscription.
    """
    circonscription = circonscription_get_handler(departement_code, circonscription_code)
    if circonscription:
        return jsonify(circonscription), 200
    abort(404, description="Circonscription not found.")
