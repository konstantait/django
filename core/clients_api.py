import logging

import requests
from requests import RequestException, HTTPError

logger = logging.getLogger(__name__)


class APIBaseClient:
    base_url = ''

    def __init__(self):
        self.response = None

    def _request(self, method, url=None, **kwargs):
        try:
            self.response = requests.request(
                method=method,
                url=url or self.base_url,
                **kwargs
            )
        except (RequestException, HTTPError) as err:
            self.response = None
            logger.error(err)

    def parse(self):
        raise NotImplementedError
