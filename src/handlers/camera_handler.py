from handlers.base_handler import BaseHandler


class CameraHandler(BaseHandler):
    """
    Capture a single live image from the camera.
    """

    path = '/camera'
    async = False

    def run(self, *args, **kwargs):
        return {
            'image': self.ctx.camera.read(),
        }
