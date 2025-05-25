from flask import jsonify, request
from flask.helpers import abort, redirect

from app.apis import main_bp
from app.handlers.deputes import (
    circonscription_get_handler,
    circonscriptions_get_handler,
    departement_get_handler,
    departements_get_handler,
    depute_by_circonscription_handler,
    depute_get_handler,
    deputes_by_departement_handler,
    deputes_get_handler,
)
from flasgger import swag_from
from flask import current_app as app


# =======================
# Députés
# =======================
@main_bp.route("/deputes", methods=["GET"])
@swag_from("../specs/deputes.yml")
def deputes_get():
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")

    app.logger.debug(f"first_name : {first_name}")
    app.logger.debug(f"last_name : {last_name}")

    deputes = deputes_get_handler(first_name, last_name)
    if deputes:
        return jsonify(deputes), 200
    abort(400)


@main_bp.route("/deputes/<depute_id>", methods=["GET"])
@swag_from("../specs/depute.yml")
def depute_get(depute_id: str):
    depute = depute_get_handler(depute_id)
    if depute:
        return jsonify(depute), 200
    abort(404, description="Depute not found.")


# =======================
# Départements
# =======================
@main_bp.route("/departements", methods=["GET"])
def departements_get():
    return jsonify(departements_get_handler()), 200


# =======================
# Circonscriptions
# =======================
@main_bp.route("/circonscriptions", methods=["GET"])
def circonscriptions_get():
    return jsonify(circonscriptions_get_handler()), 200


@main_bp.route("/circonscriptions/<departement_code>", methods=["GET"])
def circonscription_redirect_departement(departement_code):
    departement = departement_get_handler(departement_code)
    if departement:
        return jsonify(departement), 200
    abort(404)


@main_bp.route("/circonscriptions/<departement_code>/deputes", methods=["GET"])
def circonscription_redirect_departement_depute(departement_code):
    return jsonify(deputes_by_departement_handler(departement_code)), 200


@main_bp.route(
    "/circonscriptions/<departement_code>/<circonscription_code>", methods=["GET"]
)
def circonscription_get(departement_code, circonscription_code):
    circonscription = circonscription_get_handler(
        departement_code, circonscription_code
    )
    if circonscription:
        return jsonify(circonscription), 200
    abort(404)


@main_bp.route(
    "/circonscriptions/<departement_code>/<circonscription_code>/depute",
    methods=["GET"],
)
def deputes_by_circonscription(departement_code, circonscription_code):
    return (
        jsonify(
            depute_by_circonscription_handler(departement_code, circonscription_code)
        ),
        200,
    )
