from datetime import date

from flasgger import swag_from
from flask import request, abort, jsonify

from app.apis import main_bp
from app.handlers.scrutins import (
    scrutin_get_handler,
    scrutins_get_handler,
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
@swag_from("../../specs/scrutin.yml")
def scrutin_get(scrutin_id: str):
    """
    Retrieve details of a specific scrutin by ID.
    """
    scrutin = scrutin_get_handler(scrutin_id)
    if scrutin:
        return jsonify(scrutin), 200
    abort(404, description=f"Scrutin with ID '{scrutin_id}' not found.")





