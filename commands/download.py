import os
import click
import requests
import zipfile
import tempfile
from clint.textui import progress
import shutil

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
