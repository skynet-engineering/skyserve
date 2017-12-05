from handlers.base_handler import BaseHandler


class VersionHandler(BaseHandler):
    """
    Report the running Skyserve version.
    """

    path = '/version'

    def run(self, *args, **kwargs):
        return {
            'version': self.ctx.version,
        }
