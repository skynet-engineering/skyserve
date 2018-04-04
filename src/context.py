import os

from redis import ConnectionError
from redis import StrictRedis
from skycommand import discovery
from skyengine.drone import DroneController
from skysense.camera import ImageClient

from __init__ import __version__
from exc import SkyserveException
from logger import Logger

logger = Logger(__name__)


class CameraFactory(object):
    """
    Context manager for creating and destroying a Pi camera client only when it is needed.
    """

    def __init__(self, *args, **kwargs):
        """
        Pass all arguments and keyword arguments transparently to the ImageClient.
        """
        self.client_args = args
        self.client_kwargs = kwargs

    def __enter__(self):
        """
        Obtain exclusive use of the camera when an image needs to be captured.

        :return: ImageClient for taking static photos from the camera.
        """
        self.camera = ImageClient(*self.client_args, **self.client_kwargs)
        return self.camera

    def __exit__(self, *args):
        """
        Release the exclusivity held on the camera so that other processes may use it.
        """
        self.camera.close()


class Context(object):
    """
    Global server-side context initialized with all clients relevant to endpoint handlers.
    """

    def __init__(self):
        # Port on which the HTTP server should listen
        self.port = int(os.environ.get('SKYSERVE_PORT', 5000))

        # Skyengine instance to interface with the drone.
        self.drone = DroneController(os.environ.get('FC_ADDR'))

        # Capturing images from the Pi camera, if available
        self.camera_factory = CameraFactory

        # Querying registered mission services
        self.redis = StrictRedis()

        # Skyserve version
        self.version = __version__

        # Publish this Skyserve instance to the network for discovery
        discovery.publish_drone(port=self.port)

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
