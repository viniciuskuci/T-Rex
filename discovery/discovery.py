from .mdns_states import *
from .base_fsm import *
import logging

logger = logging.getLogger("Discovery")

def start():
    logger.info("Starting the discovery state machine")
    sm = Context(SearchGateway())
    sm.start()
