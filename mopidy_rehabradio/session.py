# future imports
from __future__ import unicode_literals

# stdlib imports
import logging

# local imports
from webhooks import Webhooks


logger = logging.getLogger(__name__)


class WebhookSession(object):

    def __init__(self, config):
        self.device = None
        self.token = config['webhook']['token']
        self.webhook = Webhooks(self.token)
        self.base_url = config['webhook']['webhook']

    def fetch_head(self):
        logger.info('Fetching head track')
        webhook_url = '{0}queues/{1}/head/'.format(
            self.base_url, self.device['queue']['id'])

        track = self.webhook.get(self.__class__.__name__, webhook_url)
        return track

    def pop_head(self):
        logger.info('Removing current head track')
        webhook_url = '{0}queues/{1}/head/'.format(
            self.base_url, self.device['queue']['id'])

        self.webhook.delete(self.__class__.__name__, webhook_url)

    def start(self):
        logger.info('Webhook session started')
        webhook_url = '{0}players/'.format(self.base_url)

        response = self.webhook.get(self.__class__.__name__, webhook_url)
        self.device = response['results'][0]

    def stop(self):
        logger.info('Session ended.')
        webhook_url = '{0}queues/{1}/head/'.format(
            self.base_url, self.device['queue']['id'])
        kwargs = {'state': 'stopped'}

        self.webhook.patch(self.__class__.__name__, webhook_url, **kwargs)

    def update_head(self, kwargs):
        logger.info('Updating current head track.')
        webhook_url = '{0}queues/{1}/head/'.format(
            self.base_url, self.device['queue']['id'])

        self.webhook.patch(self.__class__.__name__, webhook_url, **kwargs)

    def report_status(self, **kwargs):
        pass

    def report_event(self, **kwargs):
        pass
