from .mdns_states import *
from .base_fsm import *
import logging
from typing import Optional

logger = logging.getLogger("Discovery")


def start_discovery(database: Optional[DatabaseInterface] = None) -> None:
    logger.info("Starting the discovery state machine")
    logger.info("Using database: " + (str(database) if database else "None"))
    sm = Context(SearchGateway(), database)
    sm.start()
