# Skyserve

Skyserve is a service-agnostic framework for sending commands to drones via HTTP.

## Usage

```
$ virtualenv env
$ . env/bin/activate
$ make bootstrap
$ PORT=5000 make serve
```

Then,

```
$ curl http://localhost:5000/example/sync
{
  "async": false,
  "data": {
    "message": "Example handler"
  },
  "success": true
}
```

## Handlers

To add a new handler,

1. Create a new file in `src/handlers/`
2. Subclass `handlers.base_handlers.BaseHandler`
3. The actual logic lives inside the `run` function. Modify it as necessary for the command.
4. Add the handler to `src/api_handlers.py`

To keep the framework agnostic, the `run` function should ideally invoke other Python scripts on disk. No business logic should exist in this framework.
