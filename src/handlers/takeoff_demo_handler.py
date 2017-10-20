import time
from threading import Lock

from dronekit import VehicleMode

from handlers.mixins.avionics_mixin import AvionicsMixin
from handlers.base_handler import BaseHandler

# Height to ascend to, in meters.
_DEMO_HEIGHT = 5
# Time to spend hovering, in meters.
_DEMO_HOVERTIME = 15


class TakeoffDemoHandler(BaseHandler, AvionicsMixin):
    """
    A handler that starts a short, autonomous flight demonstration.
    The vehicle should do the following:
    1. Fly up to 3 meters.
    2. Hover there for a short while.
    3. Land.
    """

    path = '/demo/takeoff'
    async = True
    _demo_lock = Lock()

    def run(self, *args, **kwargs):
        self._demo_lock.acquire()
        # Place the vehicle in guided mode so we can make it take off.
        self.vehicle().mode = VehicleMode("GUIDED")

        # Arm the vehicle, if needed.
        if not self.ensure_armed():
            self._demo_lock.release()
            return

        # Take off.
        self._takeoff(_DEMO_HEIGHT)
        # XXX: Because _takeoff() does not block, and because dronekit does not
        # provide any mechanism to notify us when the drone has reached its target
        # altitude, the time we spend ascending counts as hover time. Therefore,
        # the next line is a little misleading!
        time.sleep(_DEMO_HOVERTIME)
        # Land the drone.
        self._land()
        self._demo_lock.release()
        return

    def _takeoff(self, height):
        """
        Make the drone take off.
        :param height: Number of meters to ascend to.
        """
        self.logger.debug('Taking off!')
        self.vehicle().simple_takeoff(height)

    def _land(self):
        """
        Land the drone.
        """
        self.logger.debug('Landing!')
        self.vehicle().mode = VehicleMode("LAND")
