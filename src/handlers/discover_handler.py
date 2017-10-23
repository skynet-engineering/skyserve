import time

from handlers.base_handler import BaseHandler


class DiscoverHandler(BaseHandler):
    """
    This handler is used for discovery by other drones.
    """

    path = '/discover'

    def run(self, *args, **kwargs):
        return {
            'timestamp': time.time(),
        }
