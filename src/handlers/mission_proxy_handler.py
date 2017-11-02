import os

import flask
import requests
from requests import ConnectionError

from handlers.base_handler import BaseHandler


REQUEST_METHOD_FUNC = {
    'GET': requests.get,
    'POST': requests.post,
}


class MissionProxyHandler(BaseHandler):
    """
    Proxy handler to Skymission for all mission action requests.
    """

    path = '/mission/<path:mission_url>'
    async = False

    def run(self, input_data, mission_url, *args, **kwargs):
        request_func = REQUEST_METHOD_FUNC[flask.request.method]
        skymission_port = os.getenv('SKYMISSION_PORT', 4000)

        url = 'http://127.0.0.1:{skymission_port}/{path}'.format(
            skymission_port=skymission_port,
            path=mission_url,
        )

        try:
            resp = request_func(
                url=url,
                headers={
                    'X-Skynet-Source': 'skyserve',
                },
                json=input_data,
            )
            return resp.json()
        except (ConnectionError, ValueError):
            return {}
