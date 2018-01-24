# Skyserve

Skyserve is a service-agnostic framework for sending commands to drones via HTTP.

## Usage

```
$ virtualenv env
$ . env/bin/activate
$ make bootstrap
$ FC_ADDR=<flight controller mavproxy address> make serve
```

Then,

```
$ curl http://localhost:5000/example/sync -d '{"hello": "world"}'
{
  "async": false,
  "data": {
    "message": "Example handler",
    "input_data": {"hello": "world"}
  },
  "success": true
}
```

## Configuration

The following environment variables may be set to alter Skyserve's behavior:

* `SKYSERVE_PORT` - HTTP port listened on by Skyserve.
* `FC_ADDR` - The address of the flight controller (eg, `udp:127.0.0.1:6002`).
If left unspecified, a "Software In-The-Loop" (SITL) simulator will be used to
simulate the drone's flight controller.

## Handlers

To add a new handler,

1. Create a new file in `src/handlers/`
2. Subclass `handlers.base_handlers.BaseHandler`
3. The actual logic lives inside the `run` function. Modify it as necessary for the command.
4. Add the handler to `src/api_handlers.py`

To keep the framework agnostic, the `run` function should ideally route the request to other services for servicing. No business logic should exist in this framework.
