import urllib.parse
import re
from backports.datetime_fromisoformat import os
from unidecode import unidecode

from app import app


def normalize(string: str) -> str:
    return re.sub(r'[^a-z]', '', unidecode(string).lower())


def build_api_url(path: str) -> str:
    return urllib.parse.urljoin(app.config["BASE_API_URL"], path)
