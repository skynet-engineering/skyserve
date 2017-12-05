from handlers.active_missions_handler import ActiveMissionsHandler
from handlers.camera_handler import CameraHandler
from handlers.discover_handler import DiscoverHandler
from handlers.flight_status_handler import FlightStatusHandler
from handlers.mission_proxy_handler import MissionProxyHandler
from handlers.version_handler import VersionHandler

# Every time a new handler is added, add its handler class to the list here.
HANDLERS = [
    ActiveMissionsHandler,
    CameraHandler,
    DiscoverHandler,
    FlightStatusHandler,
    MissionProxyHandler,
    VersionHandler,
]
