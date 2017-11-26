import os

from redis import StrictRedis
from skyengine.drone import DroneController
from skysense.camera import ImageClient


class Context(object):
    """
    Global server-side context initialized with all clients relevant to endpoint handlers.
    """

    def __init__(self):
        # Skyengine instance to interface with the drone.
        self.drone = DroneController(os.environ.get('FC_ADDR'))

        # Capturing images from the Pi camera
        self.camera = ImageClient(resolution=(1280, 720))

        # Querying registered mission services
        self.redis = StrictRedis()
