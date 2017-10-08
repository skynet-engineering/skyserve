from handlers.base_handler import BaseHandler


class ExampleSyncHandler(BaseHandler):
    """
    This is an example demonstrating how synchronous handlers are used.
    """

    path = '/example/sync'
    async = False

    def run(self, *args, **kwargs):
        return {
            'message': 'Example handler',
        }
