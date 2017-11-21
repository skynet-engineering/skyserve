from handlers.active_missions_handler import ActiveMissionsHandler
from handlers.discover_handler import DiscoverHandler
from handlers.example_async_handler import ExampleAsyncHandler
from handlers.example_sync_handler import ExampleSyncHandler
from handlers.flight_status_handler import FlightStatusHandler
from handlers.mission_proxy_handler import MissionProxyHandler

# Every time a new handler is added, add its handler class to the list here.
HANDLERS = [
    ActiveMissionsHandler,
    DiscoverHandler,
    ExampleAsyncHandler,
    ExampleSyncHandler,
    FlightStatusHandler,
    MissionProxyHandler,
]
