from flask import Flask, jsonify, request
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker
from commands import db_cli

from flask import json,request, abort
from werkzeug.exceptions import HTTPException

from config_default import MAX_PER_PAGE

app = Flask(__name__)
app.config.from_object('config_default')
app.config.from_prefixed_env()

# Make flask stateless
app.config['SESSION_COOKIE_NAME'] = ''
app.config['PERMANENT_SESSION_LIFETIME'] = 0

if isinstance(app.config["DB_ECHO"], str) and app.config["DB_ECHO"].lower() == "true":
    app.config["DB_ECHO"] = True

engine = create_engine(app.config["DB_URL"], echo=app.config["DB_ECHO"])
Session = sessionmaker(bind=engine)

app.cli.add_command(db_cli)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "msg": e.description,
    })
    response.content_type = "application/json"
    return response



MAX_PER_PAGE = 100  # or whatever your desired max per page is

@app.before_request
def before_request():
    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            raise ValueError
    except ValueError:
        return abort(400, description="Invalid 'page' parameter. It should be a positive integer.")

    try:
        per_page = int(request.args.get('per_page', MAX_PER_PAGE))
        if per_page < 1 or per_page > MAX_PER_PAGE:
            raise ValueError
    except ValueError:
        return abort(400, description=f"Invalid 'per_page' parameter. It should be a positive integer no greater than {MAX_PER_PAGE}.")

@app.route("/")
def hello():
    return "Welcome to MyDeputerFRApi !"

from apis import depute
from apis import scrutin
