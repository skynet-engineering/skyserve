import os
import time
from threading import Lock

import dronekit_sitl
from dronekit import connect


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
    connection_string = os.environ.get("FC_ADDR")
    # Software in-the-loop
    sitl = None

    @classmethod
    def ensure_armed(avionics, timeout=30):
        """
        Attempt to arm the vehicle. This step should not be performed until a flight
        mode has been selected for the drone.
        :param timeout: A timeout for the vehicle to become armable, in seconds.
        :return: True if drone was already armed or just armed, False otherwise.
        """
        if avionics.vehicle().armed:
            return True

        start_time = time.time()
        while not avionics._vehicle.is_armable:
            print "Waiting for drone to become armable..."
            time.sleep(0.5)
            if time.time() - start_time > timeout:
                print "Drone could not be armed!"
                return False

        print "Arming drone..."
        avionics._vehicle.armed = True
        while not (avionics._vehicle.armed):
            print "Waiting for drone to confirm that it's armed..."
            time.sleep(0.25)
        return True

    @classmethod
    def vehicle(avionics):
        """
        Getter for the 'vehicle', which exposes an interface for the
        physical drone. If no connection is established to the vehicle, then this
        function guarantees that one will be attempted.
        """
        if avionics._vehicle is None:
            avionics.connect_vehicle()
        return avionics._vehicle

    @classmethod
    def connect_vehicle(avionics):
        """
        Establish a connection with the vehicle's flight controller.
        If no connection string was specified, then assume we're using SITL.
        """
        avionics._connect_lock.acquire()
        # If another thread was blocked on the connection initialization lock,
        # let it abort now so we don't repeat work and cause problems.
        if avionics._vehicle is not None:
            avionics._connect_lock.release()
            return
        if avionics.connection_string is None:
            print "No connection string found -- starting SITL!"
            avionics.sitl = dronekit_sitl.start_default()
            avionics.connection_string = avionics.sitl.connection_string()

        print "Connecting to vehicle at %s..." % avionics.connection_string
        avionics._vehicle = connect(avionics.connection_string, wait_ready=True)
        avionics._connect_lock.release()

    @classmethod
    def cleanup(avionics):
        """
        Stop SITL (if started) and close the connection to the vehicle (if opened).
        """
        if avionics.sitl is not None:
            avionics.sitl.stop()
        if avionics._vehicle is not None:
            avionics._vehicle.close()
