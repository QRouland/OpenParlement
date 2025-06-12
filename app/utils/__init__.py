import json
import os
from os import PathLike
from typing_extensions import Generator, Union
import urllib.parse
import re
from unidecode import unidecode

from flask import current_app as app


def normalize(string: str) -> str:
    return re.sub(r'[^a-z]', '', unidecode(string).lower())


def build_api_url(path: str) -> str:
    return urllib.parse.urljoin(app.config["BASE_API_URL"], path)


def read_files_from_directory(directory: Union[str, PathLike]) -> Generator[dict, None, None]:
    """
    Reads and yields the JSON data of each file in a given directory.
    Skips files that cannot be read or parsed.

    Parameters:
        directory (str | PathLike): The directory containing the files to be read.

    Yields:
        dict: The parsed JSON data from each file.
    """
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                yield json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            app.logger.error(f"Error reading {file}: {e}")
            continue
