import click
from click import pass_context
from flask.cli import AppGroup, with_appcontext
from flask import Flask, current_app as app

db_cli = AppGroup('db', help='Database management commands.')

@db_cli.command("update:deputes")
@pass_context
def update_deputes(ctx):
    """
    Download and load deputes data.
    """
    download_deputes.invoke(ctx)
    load_deputes.invoke(ctx)

@db_cli.command("update:scrutins")
@pass_context
def update_scrutins(ctx):
    """
    Download and load scrutins data.
    """
    download_scrutins.invoke(ctx)
    load_scrutins.invoke(ctx)

@db_cli.command("update")
@pass_context
def update(ctx):
    """
    Download and load deputes and scrutins data.
    """
    download.invoke(ctx)
    load.invoke(ctx)

@db_cli.command("load:deputes")
def load_deputes():
    """
    Load deputes data from JSON files.
    """
    from commands.load.depute import load_from_json
    click.echo("Loading deputes")
    load_from_json(app.config["ACTEURS_FOLDER"], app.config["ORGANES_FOLDER"])
    click.echo("Deputes loaded successfully")

@db_cli.command("load:scrutins")
def load_scrutins():
    """
    Load srutins data from JSON files.
    """
    from commands.load.scrutin import load_from_json
    click.echo("Loading scrutins")
    load_from_json(app.config['SCRUTINS_FOLDER'])
    click.echo("Scrutins loaded successfully")

@db_cli.command("load")
@pass_context
def load(ctx):
    """
    Load deputes and scrutins data from JSON files.
    """
    load_deputes.invoke(ctx)
    load_scrutins.invoke(ctx)

@db_cli.command('download:deputes')
def download_deputes():
    """
    Download deputes data.
    """
    from commands.download import download_and_unzip
    download_and_unzip(
        app.config['ACTEURS_ORGANES_URL'],
        (
            ("json/acteur/", app.config['ACTEURS_FOLDER']),
            ("json/organe/", app.config['ORGANES_FOLDER']),
        )
    )

@db_cli.command('download:scrutins')
def download_scrutins():
    """
    Download scrutins data.
    """
    from commands.download import download_and_unzip
    download_and_unzip(
        app.config['SCRUTINS_URL'],
        (("json", app.config['SCRUTINS_FOLDER']),))

@db_cli.command("download")
@pass_context
def download(ctx):
    """
    Download deputes and scrutins data.
    """
    download_deputes.invoke(ctx)
    download_scrutins.invoke(ctx)
