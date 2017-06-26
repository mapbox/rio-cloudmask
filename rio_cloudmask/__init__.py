import logging

__version__ = '0.3.0'


# attach NullHandler to the 'rio_cloudmask' logger and its descendents.
# See # https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
class NullHandler(logging.Handler):
    def emit(self, record):
        pass  # pragma: no cover
log = logging.getLogger(__name__)
log.addHandler(NullHandler())
