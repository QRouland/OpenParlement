from commands import db_cli
from click import pass_context
import click

from flask import current_app as app

@db_cli.command("load")
@pass_context
def load(ctx):
    """
    Load deputes and scrutins data from JSON files.
    """
    load_deputes.invoke(ctx)
    load_scrutins.invoke(ctx)

@db_cli.command("load:deputes")
def load_deputes():
    """
    Load deputes data from JSON files.
    """
    from commands.db.load.deputes import load_from_json
    click.echo("Loading deputes")
    load_from_json(app.config["ACTEURS_FOLDER"], app.config["ORGANES_FOLDER"])
    click.echo("Deputes loaded successfully")

@db_cli.command("load:scrutins")
def load_scrutins():
    """
    Load srutins data from JSON files.
    """
    from commands.db.load.scrutins import load_from_json
    click.echo("Loading scrutins")
    load_from_json(app.config['SCRUTINS_FOLDER'])
    click.echo("Scrutins loaded successfully")

