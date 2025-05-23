import traceback

from flask import Flask, jsonify, request
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker
from commands import db_cli

from flask import json,request, abort
from werkzeug.exceptions import HTTPException
from flasgger import Swagger


app = Flask(__name__)


# Load Configuration
app.config.from_object('config_default')
app.config.from_prefixed_env()

# Make flask stateless
app.config['SESSION_COOKIE_NAME'] = ''
app.config['PERMANENT_SESSION_LIFETIME'] = 0

if isinstance(app.config["DB_ECHO"], str) and app.config["DB_ECHO"].lower() == "true":
    app.config["DB_ECHO"] = True


# Setup Flasgger
template = {
  "swagger": "2.0",
  "info": {
    "title": "Open Parlement API",
    "description": "OpenParlement is providing a public API to access data related to the French Parliament",
    "version": "0.0.1"
  },
  "host": "localhost:5000",  # overrides localhost:5000
  "schemes": [
    "http",
    "https"
  ],
}
swagger = Swagger(app, template=template)

# Setup Sqlalchemy
engine = create_engine(app.config["DB_URL"], echo=app.config["DB_ECHO"])
Session = sessionmaker(bind=engine)

# Add cli custom commands
app.cli.add_command(db_cli)

# Custom exception handler  to json
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    app.logger.error(traceback.format_exc())
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "msg": e.description,
    })
    response.content_type = "application/json"
    return response


# Ensure correct pagination arguments globally
@app.before_request
def before_request():
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            raise ValueError
    except ValueError:
        return abort(400, description="Invalid 'page' parameter. It should be a positive integer.")

    try:
        per_page = int(request.args.get('per_page', app.config['MAX_PER_PAGE']))
        if per_page < 1 or per_page > app.config['MAX_PER_PAGE']:
            raise ValueError
    except ValueError:
        return abort(400, description=f"Invalid 'per_page' parameter. It should be a positive integer no greater than {app.config['MAX_PER_PAGE']}.")



# Setup routes
from apis import depute
from apis import scrutin


@app.route("/")
def hello():
    return "Welcome to OpenParlement !"