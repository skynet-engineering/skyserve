import os
import threading

from flask import Flask
from flask import jsonify
from flask import request

from api_handlers import HANDLERS
from handlers.base_handler import BaseHandler
from logger import Logger

logger = Logger(__name__)


def init_handlers(app):
    """
    Initialize all user-defined API handlers for Skyserve.

    :param app: Flask application instance.
    """
    def map_handler_func(HandlerClass):
        """
        Create the sync/async handler function invoked by the client that abstracts actual handler
        logic.

        :param HandlerClass: Handler class to register.
        :return: A tuple of path, name, func. Path is the API endpoint for this handler. Name is
                 a unique string identifying the handler. Func is the actual function registered to
                 Flask and invoked by the client.
        """
        if not issubclass(HandlerClass, BaseHandler):
            logger.error(
                '{handler_class} is not an instance of BaseHandler! Skipping.'.format(
                    handler_class=HandlerClass.__name__,
                )
            )
            return None, None, None

        handler = HandlerClass()

        def with_tracing(handler_untraced):
            """
            Higher-order function to add request/response tracing to an arbitrary handler.

            :param handler_untraced: Untraced handler function.
            :return: Higher-order function wrapper with request/response log tracing.
            """
            def traced_handler():
                handler.logger.debug('Handler invoked from {ip}'.format(ip=request.remote_addr))
                ret = handler_untraced()
                handler.logger.debug('Handler invocation complete')
                return ret

            return traced_handler

        def handler_func():
            """
            Function registered to Flask as the route handler.

            :return: Flask JSON object to return to the client.
            """
            def async_task():
                data = handler.run()
                return {
                    'success': True,
                    'async': handler.async,
                    'data': data,
                }

            if handler.async:
                thread = threading.Thread(target=async_task, args=())
                thread.daemon = True
                thread.start()
                # Async tasks will ignore the return value of the actual handler logic function
                return jsonify({
                    'success': True,
                    'async': handler.async,
                    'data': None,
                })

            return jsonify(async_task())

        return handler.path, HandlerClass.__name__, with_tracing(handler_func)

    for (path, name, func) in map(map_handler_func, HANDLERS):
        if name:
            app.add_url_rule(path, name, func)
            logger.info('Successfully registered {handler_class}'.format(handler_class=name))

    # Catch-all route for routes without a corresponding handler
    @app.errorhandler(404)
    def handler_not_found(err):
        return jsonify({
            'success': False,
            'message': 'Route not found. Are you sure you registered the handler?',
        })


def main():
    app = Flask(__name__)
    init_handlers(app)
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        threaded=True,
        debug=True,
    )


if __name__ == '__main__':
    main()
