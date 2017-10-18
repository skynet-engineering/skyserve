from logger import Logger


class BaseHandler(object):
    """
    Base API handler class.
    """

    # Path/route for this endpoint
    path = ''
    # True if the endpoint is asynchronous. Async endpoints will return to the client with a
    # response immediately and run the task in the background. Sync endpoint will wait until the
    # run() function completes before returning to the client.
    async = False

    def __init__(self):
        """
        Initialize a handler.
        """
        # Initialize the logger with the name of the current BaseHandler subclass.
        self.logger = Logger(self.__class__.__name__)

    def run(self, *args, **kwargs):
        """
        Function to run when this endpoint is requested by a client.
        Non-keyword arguments include:
            - input_data: JSON-parsed request body from a POST request (if supplied, otherwise None)

        :param args: Arbitrary function arguments
        :param kwargs: Arbitrary function keyword arguments
        :return: None, or a JSON-serializable dictionary describing the status of the action.
        """
        raise NotImplementedError('Handler logic is not implemented!')
