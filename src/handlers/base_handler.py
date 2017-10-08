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

    def run(self, *args, **kwargs):
        """
        Function to run when this endpoint is requested by a client.

        :param args: Arbitrary function arguments
        :param kwargs: Arbitrary function keyword arguments
        :return: None, or a JSON-serializable dictionary describing the status of the action.
        """
        raise NotImplementedError('Handler logic is not implemented!')
