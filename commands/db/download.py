import os
import shutil
import tempfile
import zipfile

import click
import requests
from click import pass_context
from clint.textui import progress
from flask import current_app as app

from commands import db_cli


@db_cli.command("download")
@pass_context
def download(ctx):
    """
    Download deputes and scrutins data.
    """
    download_deputes.invoke(ctx)
    download_scrutins.invoke(ctx)

@db_cli.command('download:deputes')
def download_deputes():
    """
    Download deputes data.
    """
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
    download_and_unzip(
        app.config['SCRUTINS_URL'],
        (("json", app.config['SCRUTINS_FOLDER']),))



def download_and_unzip(url : str, zip_mvs: tuple[tuple[(str, str)], ...]):
    temp_dir = tempfile.mkdtemp()

    # Download
    filename = os.path.join(temp_dir, 'file.zip')
    response = requests.head(url)
    total_size = int(response.headers.get('content-length', 0))

    click.echo(f'Downloading {url}.')
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in progress.bar(r.iter_content(chunk_size=8192), expected_size=(total_size//8192)+1):
                if chunk:
                    f.write(chunk)

    # Extract
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Move
    for zip_src, zip_dst in zip_mvs:
        zip_src = os.path.join(temp_dir, zip_src)
        click.echo(f'Moving {zip_src} to {zip_dst}.')
        shutil.rmtree(zip_dst, ignore_errors=True)
        shutil.move(zip_src, zip_dst)

    # clean up
    shutil.rmtree(temp_dir)

    click.echo('Download and unzip completed.')
