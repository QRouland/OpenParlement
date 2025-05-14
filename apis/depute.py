from flask import jsonify
from app import app
from handlers.depute import departement_get_handler, departements_get_handler, depute_get_handler, deputes_by_departement_handler, deputes_get_handler

# =======================
# Députés
# =======================
@app.route('/deputes', methods=['GET'])
def deputes_get():
    return jsonify(deputes_get_handler()), 200

@app.route('/deputes/<depute_id>', methods=['GET'])
def depute_get(depute_id : str):
    depute = depute_get_handler(depute_id)
    if depute:
        return jsonify(depute), 200
    return jsonify({'error': 'Député not found'}), 404

# =======================
# Départements
# =======================
@app.route('/departements', methods=['GET'])
def departements_get():
    return jsonify(departements_get_handler()), 200

@app.route('/departements/<department_code>', methods=['GET'])
def departement_get(department_code : str):
    return jsonify(departement_get_handler(department_code)), 200


@app.route('/departements/<department_code>/deputes', methods=['GET'])
def deputes_by_departement(department_code : str):
    return jsonify(deputes_by_departement_handler(department_code)), 200

@app.route('/departements/<department_code>/circonscriptions', methods=['GET'])
def circonscriptions_by_departement(department_code):
    # Stubbed circonscriptions by department
    circonscriptions = [
        {"id": "1", "departement_id": department_code},
        {"id": "2", "departement_id": department_code}
    ]
    return jsonify(circonscriptions), 200

# =======================
# Circonscriptions
# =======================
@app.route('/circonscriptions', methods=['GET'])
def circonscriptions_get():
    circonscriptions = [
        {"id": "1", "departement_id": "75"},
        {"id": "2", "departement_id": "13"}
    ]
    return jsonify(circonscriptions), 200

@app.route('/circonscriptions/<circonscription_id>', methods=['GET'])
def circonscription_get(circonscription_id):
    # Stubbed single circonscription
    circonscription = {
        "id": circonscription_id,
        "departement_id": "75",
        "name": f"Circonscription {circonscription_id}"
    }
    return jsonify(circonscription), 200
