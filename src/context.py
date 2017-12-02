import os

from redis import StrictRedis
from skyengine.drone import DroneController
from skysense.camera import ImageClient

from logger import Logger

logger = Logger(__name__)


class Context(object):
    """
    Global server-side context initialized with all clients relevant to endpoint handlers.
    """

    def __init__(self):
        # Skyengine instance to interface with the drone.
        self.drone = DroneController(os.environ.get('FC_ADDR'))

        # Capturing images from the Pi camera, if available
        try:
            self.camera = ImageClient(resolution=(1280, 720))
        except Exception:
            logger.warn('Camera hardware not available! Skipping camera initialization.')
            self.camera = None

        # Querying registered mission services
        self.redis = StrictRedis()
