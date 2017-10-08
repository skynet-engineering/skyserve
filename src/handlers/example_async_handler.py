import time

from handlers.base_handler import BaseHandler


class ExampleAsyncHandler(BaseHandler):
    """
    This is an example demonstrating how asynchronous handlers are used.
    """

    path = '/example/async'
    async = True

    def run(self, *args, **kwargs):
        time.sleep(10)
