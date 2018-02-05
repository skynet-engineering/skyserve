from handlers.base_handler import BaseHandler


class FlightStatusHandler(BaseHandler):
    """
    Query the current flight parameters of the drone.
    """

    path = '/flight-status'
    async = False

    def run(self, *args, **kwargs):
        location = self.ctx.drone.vehicle.location.global_relative_frame
        airspeed = self.ctx.drone.vehicle.airspeed
        heading = self.ctx.drone.vehicle.heading
        battery = self.ctx.drone.read_battery_status()
        status = self.ctx.drone.status.name
        mode = self.ctx.drone.vehicle.mode.name

        return {
            # Default to a null latitude and longitude if no GPS lock exists.
            # (Dronekit reports coordinates at 0 when there is no GPS lock.)
            'lat': location.lat or None,
            'lon': location.lon or None,
            'alt': location.alt,
            'airspeed': airspeed,
            'heading': heading,
            'battery': battery.voltage,
            'status': status,
            'mode': mode,
        }
