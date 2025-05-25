from datetime import date

from flasgger import swag_from
from flask import request, abort, jsonify

from app.apis import main_bp
from app.handlers.scrutins import (
    depute_scrutin_vote_get_handler,
    depute_votes_get_handler,
    scrutin_get_handler,
    scrutins_get_handler,
    scrutin_votes_get_handler,
    vote_get_handler,
    votes_get_handler, depute_votes_stats_get_handler,
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
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Validate dates
    if start_date is not None:
        try:
            start_date = date.fromisoformat(start_date)
        except ValueError:
            abort(400, description=f"Invalid 'start_date' date format. Expected ISO format (YYYY-MM-DD), got '{start_date}'.")

    if end_date is not None:
        try:
            end_date = date.fromisoformat(end_date)
        except ValueError:
            abort(400, description=f"Invalid 'end_date' date format. Expected ISO format (YYYY-MM-DD), got '{end_date}'.")

    scrutins = scrutins_get_handler(start_date=start_date, end_date=end_date)

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
    abort(404, description=f"Député with ID '{depute_id}' not found.")


@main_bp.route("/deputes/<string:depute_id>/votes/<string:scrutin_id>", methods=["GET"])
def vote_by_depute_and_scrutin(depute_id: str, scrutin_id: str):
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
