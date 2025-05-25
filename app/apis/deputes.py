from flasgger import swag_from
from flask import request, jsonify, abort, current_app as app

from app.apis import main_bp
from app.handlers.deputes import (
    circonscription_get_handler,
    circonscriptions_get_handler,
    circonscriptions_by_departement_handler,
    departements_get_handler,
    depute_by_circonscription_handler,
    depute_get_handler,
    deputes_by_departement_handler,
    deputes_get_handler,
)


# =======================
# Députés
# =======================

@main_bp.route("/deputes", methods=["GET"])
@swag_from("../../specs/deputes.yml")
def deputes_get():
    """
    Get a list of all députés.
    Supports optional filtering by first name and/or last name via query parameters.
    Example: /deputes?first_name=Jean&last_name=Dupont
    """
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")

    app.logger.debug(f"Filtering députés - first_name: {first_name}, last_name: {last_name}")

    deputes = deputes_get_handler(first_name, last_name)

    if deputes is not None:
        return jsonify(deputes), 200

    abort(400, description="Invalid query parameters or internal error retrieving députés.")


@main_bp.route("/deputes/<string:depute_id>", methods=["GET"])
@swag_from("../../specs/depute.yml")
def depute_get(depute_id: str):
    """
    Get detailed information about a specific député by ID.
    """
    depute = depute_get_handler(depute_id)

    if depute:
        return jsonify(depute), 200

    abort(404, description=f"Député with ID '{depute_id}' not found.")



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


@main_bp.route("/departements/<departement_code>/deputes", methods=["GET"])
def deputes_by_departement_get(departement_code):
    """
    Get all députés elected in a given département.
    """
    deputes = deputes_by_departement_handler(departement_code)
    if deputes:
        return jsonify(deputes), 200
    abort(404, description="No députés found for this département.")


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
def circonscriptions_by_departement_get(departement_code):
    """
    Get all circonscriptions for a specific département.
    """
    circonscriptions = circonscriptions_by_departement_handler(departement_code)
    if circonscriptions:
        return jsonify(circonscriptions), 200
    abort(404, description="No circonscriptions found for this département.")


@main_bp.route("/departements/<departement_code>/circonscriptions/<circonscription_code>", methods=["GET"])
def circonscription_get(departement_code, circonscription_code):
    """
    Get a specific circonscription within a département.
    """
    circonscription = circonscription_get_handler(departement_code, circonscription_code)
    if circonscription:
        return jsonify(circonscription), 200
    abort(404, description="Circonscription not found.")


@main_bp.route("/departements/<departement_code>/circonscriptions/<circonscription_code>/depute", methods=["GET"])
def depute_by_circonscription_get(departement_code, circonscription_code):
    """
    Get the député elected in a specific circonscription of a département.
    """
    depute = depute_by_circonscription_handler(departement_code, circonscription_code)
    if depute:
        return jsonify(depute), 200
    abort(404, description="Député not found for this circonscription.")
