from flask import jsonify, request
from flask.helpers import abort, redirect
from app import app
from handlers.depute import circonscription_get_handler, circonscriptions_get_handler, departement_get_handler, departements_get_handler, depute_by_circonscription_handler, depute_get_handler, deputes_by_departement_handler, deputes_get_handler

# =======================
# Députés
# =======================
@app.route('/deputes', methods=['GET'])
def deputes_get():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    app.logger.debug(f"first_name : {first_name}" )
    app.logger.debug(f"last_name : {last_name}")

    deputes = deputes_get_handler(first_name, last_name)
    if deputes:
        return jsonify(deputes), 200
    abort(400)

@app.route('/deputes/<depute_id>', methods=['GET'])
def depute_get(depute_id : str):
    depute = depute_get_handler(depute_id)
    if depute:
        return jsonify(depute), 200
    abort(404, description="Depute not found.")

# =======================
# Départements
# =======================
@app.route('/departements', methods=['GET'])
def departements_get():
    return jsonify(departements_get_handler()), 200

@app.route('/departements/<departement_code>', methods=['GET'])
def departement_get(departement_code : str):
    departement = departement_get_handler(departement_code)
    if departement:
        return jsonify(departement), 200
    abort(404)

@app.route('/departements/<departement_code>/deputes', methods=['GET'])
def deputes_by_departement(departement_code : str):
    return jsonify(deputes_by_departement_handler(departement_code)), 200


# =======================
# Circonscriptions
# =======================
@app.route('/circonscriptions', methods=['GET'])
def circonscriptions_get():
    return jsonify(circonscriptions_get_handler()), 200

@app.route('/circonscriptions/<departement_code>', methods=['GET'])
def circonscription_redirect_departement(departement_code):
    return redirect(f"/departements/{departement_code}")

@app.route('/circonscriptions/<departement_code>/deputes', methods=['GET'])
def circonscription_redirect_departement_depute(departement_code):
    return redirect(f"/departements/{departement_code}/deputes")

@app.route('/circonscriptions/<departement_code>/<circonscription_code>', methods=['GET'])
def circonscription_get(departement_code, circonscription_code):
    circonscription = circonscription_get_handler(departement_code, circonscription_code)
    if circonscription:
        return jsonify(circonscription), 200
    abort(404)

@app.route('/circonscriptions/<departement_code>/<circonscription_code>/depute', methods=['GET'])
def deputes_by_circonscription(departement_code, circonscription_code):
    return jsonify(depute_by_circonscription_handler(departement_code, circonscription_code)), 200
