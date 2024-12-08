import dataclasses
import time

import requests
from requests import Response

DEFAULT_TIMEOUT = 120
DEFAULT_RETRY = 3
NO_RETRY = 1
WAIT_TIME = 10

def execute_get(url, params=None, retry=DEFAULT_RETRY, timeout=DEFAULT_TIMEOUT, wait_time=WAIT_TIME, **kwargs):
    return _retry(
        func=lambda: requests.get(url, params=params, timeout=timeout, **kwargs), retry=retry, wait_time=wait_time
    )