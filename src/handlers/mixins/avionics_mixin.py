import os
import time
from threading import Lock

import dronekit_sitl
from dronekit import connect

from logger import Logger

logger = Logger('AvionicsMixin')


class AvionicsMixin:
    """
    A 'mixin' class that mediates a single connection to the flight controller between handlers
    and encapsulates a few tedious, vehicle control-related tasks.
    """
    # Vehicle shared by handlers
    _vehicle = None
    # Lock to linearize the connection initialization
    _connect_lock = Lock()
    # Connection string for the connection to the flight controller.
    connection_string = os.environ.get('FC_ADDR')
    # Software in-the-loop
    sitl = None

    @classmethod
    def ensure_armed(cls, timeout=30):
        """
        Attempt to arm the vehicle. This step should not be performed until a flight
        mode has been selected for the drone.
        :param timeout: A timeout for the vehicle to become armable, in seconds.
        :return: True if drone was already armed or just armed, False otherwise.
        """
        if cls.vehicle().armed:
            return True

        start_time = time.time()
        while not cls._vehicle.is_armable:
            logger.debug('Waiting for drone to become armable...')
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                logger.debug('Drone could not be armed!')
                return False

        logger.debug('Arming drone...')
        cls._vehicle.armed = True
        while not cls._vehicle.armed:
            logger.debug('Waiting for drone to confirm that it\'s armed...')
            time.sleep(0.25)
        return True

    @classmethod
    def vehicle(cls):
        """
        Getter for the 'vehicle', which exposes an interface for the
        physical drone. If no connection is established to the vehicle, then this
        function guarantees that one will be attempted.
        """
        if cls._vehicle is None:
            cls.connect_vehicle()
        return cls._vehicle

    @classmethod
    def connect_vehicle(cls):
        """
        Establish a connection with the vehicle's flight controller.
        If no connection string was specified, then assume we're using SITL.
        """
        cls._connect_lock.acquire()
        # If another thread was blocked on the connection initialization lock,
        # let it abort now so we don't repeat work and cause problems.
        if cls._vehicle is not None:
            cls._connect_lock.release()
            return
        if cls.connection_string is None:
            logger.debug('No connection string found -- starting SITL!')
            cls.sitl = dronekit_sitl.start_default()
            cls.connection_string = cls.sitl.connection_string()

        logger.debug('Connecting to vehicle at {}...'.format(cls.connection_string))
        cls._vehicle = connect(cls.connection_string, wait_ready=True)
        cls._connect_lock.release()

    @classmethod
    def cleanup(cls):
        """
        Stop SITL (if started) and close the connection to the vehicle (if opened).
        """
        if cls.sitl is not None:
            cls.sitl.stop()
        if cls._vehicle is not None:
            cls._vehicle.close()
