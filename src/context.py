import os

from redis import ConnectionError
from redis import StrictRedis
from skyengine.drone import DroneController
from skysense.camera import ImageClient

from __init__ import __version__
from exc import SkyserveException
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

        # Skyserve version
        self.version = __version__

        # Verify the instantiated context before continuing
        self._verify_ctx()

    def _verify_ctx(self):
        """
        Verify health of all necessary clients instantiated by the context.
        """
        self._verify_redis()

    def _verify_redis(self):
        """
        Verify health and availability of the Redis server.

        :raises SkyserveException: If a Redis server is not available on the default port.
        """
        try:
            self.redis.ping()
        except ConnectionError:
            logger.error('Redis server not available!')
            raise SkyserveException(' '.join([
                'Unable to connect to Redis server at port 6379!',
                'Are you sure it is installed and running?',
                'Redis is required to self-register a mission with Skyserve.',
                'See installation instructions here: https://redis.io/download',
            ]))
