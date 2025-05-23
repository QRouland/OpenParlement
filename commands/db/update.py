from click import pass_context

from commands import db_cli
from commands.db.download import download, download_deputes, download_scrutins
from commands.db.load import load, load_deputes, load_scrutins


@db_cli.command("update")
@pass_context
def update(ctx):
    """
    Download and load deputes and scrutins data.
    """
    download.invoke(ctx)
    load.invoke(ctx)

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

