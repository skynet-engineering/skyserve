from handlers.base_handler import BaseHandler


# Redis prefix for all Skymission service-port registrations.
SKYMISSION_KEY_PREFIX = 'skymission:mission:'


class ActiveMissionsHandler(BaseHandler):
    """
    Handler for reading all currently active self-registered mission services.
    """

    path = '/active-missions'
    async = False

    def run(self, *args, **kwargs):
        return {
            'missions': [
                {
                    'mission_id': mission_key[len(SKYMISSION_KEY_PREFIX):],
                    'port': int(self.ctx.redis.get(mission_key))
                }
                for mission_key in self.ctx.redis.scan_iter('{}*'.format(SKYMISSION_KEY_PREFIX))
            ]
        }
