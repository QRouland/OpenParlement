from flasgger import swag_from
from flask import abort, jsonify, current_app as app
from app.apis import main_bp
from app.handlers.scrutins import (
    depute_scrutin_vote_get_handler,
    depute_votes_get_handler,
    scrutin_get_handler,
    scrutins_get_handler,
    scrutin_votes_get_handler,
    vote_get_handler,
    votes_get_handler,
)


# =======================
# Scrutins
# =======================

@main_bp.route("/scrutins", methods=["GET"])
@swag_from("../../specs/scrutins.yml")
def scrutins_get():
    """
    Retrieve a list of all scrutins.
    """
    scrutins = scrutins_get_handler()
    return jsonify(scrutins), 200


@main_bp.route("/scrutins/<string:scrutin_id>", methods=["GET"])
def scrutin_get(scrutin_id: str):
    """
    Retrieve details of a specific scrutin by ID.
    """
    scrutin = scrutin_get_handler(scrutin_id)
    if scrutin:
        return jsonify(scrutin), 200
    abort(404, description=f"Scrutin with ID '{scrutin_id}' not found.")


# =======================
# Votes
# =======================

@main_bp.route("/votes", methods=["GET"])
def votes_get():
    """
    Retrieve all votes.
    """
    votes = votes_get_handler()
    return jsonify(votes), 200


@main_bp.route("/votes/<string:vote_id>", methods=["GET"])
def vote_get(vote_id: str):
    """
    Retrieve details of a specific vote by ID.
    """
    vote = vote_get_handler(vote_id)
    if vote:
        return jsonify(vote), 200
    abort(404, description=f"Vote with ID '{vote_id}' not found.")


@main_bp.route("/scrutins/<string:scrutin_id>/votes", methods=["GET"])
def votes_by_scrutin(scrutin_id: str):
    """
    Retrieve all votes for a specific scrutin.
    """
    votes = scrutin_votes_get_handler(scrutin_id)
    if votes:
        return jsonify(votes), 200
    abort(404, description=f"No votes found for scrutin with ID '{scrutin_id}'.")


@main_bp.route("/deputes/<string:depute_id>/votes", methods=["GET"])
def votes_by_depute(depute_id: str):
    """
    Retrieve all votes cast by a specific député.
    """
    votes = depute_votes_get_handler(depute_id)
    if votes:
        return jsonify(votes), 200
    abort(404, description=f"No votes found for député with ID '{depute_id}'.")


@main_bp.route("/deputes/<string:depute_id>/votes/<string:scrutin_id>", methods=["GET"])
def vote_by_depute_and_scrutin(depute_id: str, scrutin_id: str):
    """
    Retrieve the vote cast by a specific député on a specific scrutin.
    """
    vote = depute_scrutin_vote_get_handler(depute_id, scrutin_id)
    if vote:
        return jsonify(vote), 200
    abort(404, description=f"Vote not found for député '{depute_id}' on scrutin '{scrutin_id}'.")
