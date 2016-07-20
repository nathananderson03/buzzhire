import json, httplib
import logging
from django.conf import settings


logger = logging.getLogger('project')

CLIENT_APP = 'CLIENT'
FREELANCER_APP = 'FREELANCER'

class ParseConnection(object):
    """Object for handling push requests via Parse.
    
    Should be initialized with either CLIENT_APP or FREELANCER_APP:
    
        connection = ParseConnection(CLIENT_APP)
    
    or:
    
        connection = ParseConnection(FREELANCER_APP)
    
    """
    PARSE_URL = 'api.parse.com'
    PARSE_PORT = 443
    PARSE_PUSH_ENDPOINT = '/1/push'


    def __init__(self, app):
        self.app = app
        try:
            self.connection = httplib.HTTPSConnection(self.PARSE_URL,
                                                      self.PARSE_PORT)
            self.connection.connect()
        except Exception as e:
            logger.exception(e)


    def get_app_id(self):
        "Returns the id for the app we're connecting to."
        return getattr(settings, 'PARSE_%s_APPLICATION_ID' % self.app)

    def get_app_key(self):
        "Returns the key for the app we're connecting to."
        return getattr(settings, 'PARSE_%s_REST_API_KEY' % self.app)


    def push_message(self, message, user, category,
                     content_type_name, object_id):
        data = {
           "where": {
             # The user email is used to identify the user
             # TODO - this should really be the user id, in case they change
             # their email address
             "userEmail": user.email,
           },
           "data": {
             "alert": message,
             "category": category,
             "content_type": content_type_name,
             "object_id": object_id,
           }
        }
        logger.debug('Attempting to send push notification to %s: %s' % (
                                            self.get_app_id(), data))
        try:
            self.connection.request('POST', self.PARSE_PUSH_ENDPOINT,
                                    json.dumps(data), {
                   "X-Parse-Application-Id": self.get_app_id(),
                   "X-Parse-REST-API-Key": self.get_app_key(),
                   "Content-Type": "application/json"
                 })
        except Exception as e:
            logger.debug('Push failed.')
            logger.exception(e)
        else:
            logger.debug('Push sent.')
