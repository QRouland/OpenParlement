from flask import abort, jsonify, request
from app import app
from handlers.scrutin import depute_scrutin_vote_get_handler, depute_votes_get_handler, scrutin_get_handler, scrutins_get_handler, vote_get_handler, votes_get_handler

# =======================
# Scrutins
# =======================
@app.route('/scrutins', methods=['GET'])
def scrutins_get():
    scrutins = scrutins_get_handler()
    return jsonify(scrutins), 200


@app.route('/scrutins/<scrutin_id>', methods=['GET'])
def scrutin_get(scrutin_id : str):
    scrutin = scrutin_get_handler(scrutin_id)
    if scrutin:
        return jsonify(scrutin), 200
    abort(404, description="Scrutin not found")

# =======================
# Votes
# =======================
@app.route('/deputes/votes', methods=['GET'])
def votes_get():
    votes = votes_get_handler()
    return jsonify(votes), 200



@app.route('/deputes/votes/<scrutin_id>', methods=['GET'])
def vote_get(votes_id : str):
    vote = vote_get_handler(votes_id)
    if vote:
        return jsonify(vote), 200
    abort(404, description="Scrutin not found")


@app.route('/deputes/<depute_id>/votes', methods=['GET'])
def vote_depute_get(depute_id : str):
    votes = depute_votes_get_handler(depute_id)
    return jsonify(votes), 200


@app.route('/deputes/<depute_id>/votes/<scrutin_id>', methods=['GET'])
def vote_deputes_get(depute_id : str, scrutin_id: str):
    vote = depute_scrutin_vote_get_handler(depute_id, scrutin_id)
    if vote:
        return jsonify(vote), 200
    abort(404, description="Scrutin not found")
