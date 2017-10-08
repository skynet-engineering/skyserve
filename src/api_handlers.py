from handlers.example_async_handler import ExampleAsyncHandler
from handlers.example_sync_handler import ExampleSyncHandler


# Every time a new handler is added, add its handler class to the list here.
HANDLERS = [
    ExampleAsyncHandler,
    ExampleSyncHandler,
]
