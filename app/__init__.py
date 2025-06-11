import os
import traceback

from dotenv import load_dotenv
from flasgger import Swagger
from flask import Flask
from flask import json, request, abort
from werkzeug.exceptions import HTTPException

from app.apis import main_bp
from app.db import init_db
from app.utils.config import str_to_bool, str_to_int
from commands import db_cli


def create_app(config_class="app.config", load_env_=True):
    app = Flask(__name__)


    # Load Configuration
    load_dotenv()
    app.config['HOST'] = os.getenv('FLASK_HOST', "127.0.0.1:5000")
    app.config['MAX_PER_PAGE'] = str_to_int(os.getenv('FLASK_MAX_PER_PAGE', 200))
    app.config['DEFAULT_PER_PAGE'] = str_to_int(os.getenv('FLASK_DEFAULT_PER_PAGE', 100))
    app.config['ACTEURS_FOLDER'] = os.getenv('FLASK_ACTEURS_FOLDER', "data/acteurs")
    app.config['ORGANES_FOLDER'] = os.getenv('FLASK_ORGANES_FOLDER', "data/organes")
    app.config['SCRUTINS_FOLDER'] = os.getenv('FLASK_SCRUTINS_FOLDER', "data/scrutins")
    app.config['ACTEURS_ORGANES_URL'] = (
        os.getenv(
            'FLASK_ACTEURS_ORGANES_URL',
            "https://data.assemblee-nationale.fr/static/openData/repository/17/amo/deputes_actifs_mandats_actifs_organes/"
            "AMO10_deputes_actifs_mandats_actifs_organes.json.zip"
        )
    )
    app.config['SCRUTINS_URL'] = os.getenv(
        'FLASK_SCRUTINS_URL',
        "https://data.assemblee-nationale.fr/static/openData/repository/17/loi/scrutins/Scrutins.json.zip"
    )

    app.config['DB_ECHO'] = str_to_bool(os.getenv('FLASK_DB_ECHO', "False"))
    db_url = os.getenv('FLASK_DB_URL')
    if db_url is None:
        raise Exception("The FLASK_DB_URL environment variable must be set")
    app.config['DB_URL'] = db_url

    # Make flask stateless
    app.config["SESSION_COOKIE_NAME"] = ""
    app.config["PERMANENT_SESSION_LIFETIME"] = 0

    # Setup Flasgger
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Open Parlement API",
            "description": "OpenParlement is providing a public API to access data related to the French Parliament",
            "version": "dev",
        },
        "host": "localhost:5000",  # overrides localhost:5000
        "schemes": ["http", "https"],
    }
    Swagger(app, template=template)

    # Add cli custom commands
    app.cli.add_command(db_cli)

    # Custom exception handler  to json
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        app.logger.error(traceback.format_exc())
        response = e.get_response()
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "msg": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    # Ensure correct pagination arguments globally
    @app.before_request
    def before_request():
        try:
            page = int(request.args.get("page", 1))
            if page < 1:
                raise ValueError
        except ValueError:
            return abort(
                400,
                description="Invalid 'page' parameter. It should be a positive integer.",
            )

        try:
            per_page = int(request.args.get("per_page", app.config["MAX_PER_PAGE"]))
            if per_page < 1 or per_page > app.config["MAX_PER_PAGE"]:
                raise ValueError
        except ValueError:
            return abort(
                400,
                description=f"Invalid 'per_page' parameter. It should be a positive integer no greater than {app.config['MAX_PER_PAGE']}.",
            )

    # Setup routes
    from app.apis import circonscriptions
    from app.apis import departements
    from app.apis import deputes
    from app.apis import scrutins
    from app.apis import votes


    app.register_blueprint(main_bp)

    @app.route("/")
    def hello():
        return "Welcome to OpenParlement !"

    init_db(app.config["DB_URL"], app.config["DB_ECHO"])
    return app
