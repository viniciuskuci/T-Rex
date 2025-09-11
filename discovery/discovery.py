from .mdns_states import *
from .base_fsm import *
import logging

logger = logging.getLogger("Discovery")


def start_discovery():
    logger.info("Starting the discovery state machine")
    sm = Context(SearchGateway())
    sm.start()
