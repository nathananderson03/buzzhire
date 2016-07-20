import time
from huey.djhuey import task
import logging

logger = logging.getLogger('project')


@task()
def test_logging():
    """Huey task which can be used to test logging of the consumer.
    Simply does some logging and raises an exception.
    """
    print('[%s] Test print message from test_logging task.' % time.ctime())
    logger.debug('Test log message (level DEBUG) from test_logging task.')
    logger.error('Test log message (level ERROR) from test_logging task.')
    try:
        raise Exception('Test caught exception from test_logging task.')
    except Exception as e:
        logger.exception(e)
    raise Exception('Test uncaught exception from test_logging task.')
