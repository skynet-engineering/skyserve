from handlers.active_missions_handler import ActiveMissionsHandler
from handlers.discover_handler import DiscoverHandler
from handlers.example_async_handler import ExampleAsyncHandler
from handlers.example_sync_handler import ExampleSyncHandler
from handlers.mission_proxy_handler import MissionProxyHandler
from handlers.takeoff_demo_handler import TakeoffDemoHandler


# Every time a new handler is added, add its handler class to the list here.
HANDLERS = [
    ActiveMissionsHandler,
    DiscoverHandler,
    ExampleAsyncHandler,
    ExampleSyncHandler,
    MissionProxyHandler,
    TakeoffDemoHandler,
]
