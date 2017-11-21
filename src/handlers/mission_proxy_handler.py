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

    path = '/mission/<mission_id>/<path:mission_url>'
    async = False

    def run(self, input_data, mission_id, mission_url, *args, **kwargs):
        request_func = REQUEST_METHOD_FUNC[flask.request.method]
        key = 'skymission:mission:{mission_id}'.format(mission_id=mission_id)
        skymission_port = self.ctx.redis.get(key)

        if not skymission_port:
            return {
                'message': 'Service port for `{mission_id}` not registered!'.format(
                    mission_id=mission_id,
                )
            }

        url = 'http://127.0.0.1:{skymission_port}/{path}'.format(
            skymission_port=skymission_port,
            path=mission_url,
        )

        self.logger.debug('Proxying to {url}'.format(url=url))

        try:
            resp = request_func(
                url=url,
                headers={
                    'X-Skynet-Source': 'skyserve',
                    'X-Forwarded-For': flask.request.remote_addr,
                },
                json=input_data,
            )
            return resp.json()
        except (ConnectionError, ValueError):
            return None
