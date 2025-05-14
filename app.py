import click
from flask import Flask
from sqlalchemy.engine.create import create_engine
from sqlalchemy.orm.session import sessionmaker

from db import init_db


app = Flask(__name__)
app.config.from_object('config_default')
app.config.from_prefixed_env()

if isinstance(app.config["DB_ECHO"], str) and app.config["DB_ECHO"].lower() == "true":
    app.config["DB_ECHO"] = True

engine = create_engine(app.config["DB_URL"], echo=app.config["DB_ECHO"])
Session = sessionmaker(bind=engine)
#init_db()


@app.cli.command("load")
def load():
    from loader.depute import load_from_json
    load_from_json()

@app.route("/")
def hello():
    return "Welcom to MyDeputerFRApi !"

from apis import depute
