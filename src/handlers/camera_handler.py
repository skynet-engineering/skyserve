from handlers.base_handler import BaseHandler


class CameraHandler(BaseHandler):
    """
    Capture a single live image from the camera.
    """

    path = '/camera'
    async = False

    def capture_image(self):
        """
        Attempt to capture an image, if the hardware allows it.

        :return: Base64-encoded image data if available; None otherwise.
        """
        try:
            with self.ctx.camera_factory(resolution=(1280, 720)) as camera:
                return camera.read()
        except Exception as exc:
            self.logger.error('Error starting camera client: is it in use by another process?')
            self.logger.error(exc)

    def run(self, *args, **kwargs):
        return {
            'image': self.capture_image(),
        }
