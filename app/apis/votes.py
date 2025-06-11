from flasgger import swag_from
from flask import jsonify, abort

from app import main_bp
from app.handlers.votes import votes_get_handler, vote_get_handler, depute_votes_get_handler, \
    depute_scrutin_vote_get_handler, scrutin_votes_get_handler, depute_votes_stats_get_handler


# =======================
# Votes
# =======================

@main_bp.route("/scrutins/<string:scrutin_id>/votes", methods=["GET"])
@swag_from("../../specs/votes_by_scrutin.yml")
def votes_by_scrutin_get(scrutin_id: str):
    """
    Retrieve all votes for a specific scrutin.
    """
    votes = scrutin_votes_get_handler(scrutin_id)
    if votes:
        return jsonify(votes), 200
    abort(404, description=f"No votes found for scrutin with ID '{scrutin_id}'.")


@main_bp.route("/deputes/<string:depute_id>/votes", methods=["GET"])
def votes_by_depute_get(depute_id: str):
    """
    Retrieve all votes cast by a specific député.
    """
    votes = depute_votes_get_handler(depute_id)
    if votes:
        return jsonify(votes), 200
    abort(404, description=f"Député with ID '{depute_id}' not found.")


@main_bp.route("/deputes/<string:depute_id>/votes/<string:scrutin_id>", methods=["GET"])
def vote_by_depute_scrutin_get(depute_id: str, scrutin_id: str):
    """
    Retrieve the vote cast by a specific député on a specific scrutin.
    """
    vote = depute_scrutin_vote_get_handler(depute_id, scrutin_id)
    if vote:
        return jsonify(vote), 200
    abort(404, description=f"Vote not found for député '{depute_id}' on scrutin '{scrutin_id}'.")


@main_bp.route("/deputes/<string:depute_id>/votes/stats", methods=["GET"])
def votes_stats_by_depute(depute_id: str):
    """
    Retrieve all votes cast by a specific député.
    """
    votes = depute_votes_stats_get_handler(depute_id)
    if votes:
        return jsonify(votes), 200
    abort(404, description=f"Député with ID '{depute_id}' not found.")
