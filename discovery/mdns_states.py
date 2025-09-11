from .base_fsm import State
import time
from .mdns import Discover, Announcer
from .models import Constants, DinasoreService
from typing import Optional
from zeroconf import Zeroconf
import logging

logger = logging.getLogger("DiscoveryFSM")


class SearchGateway(State):

    def __init__(self, discover: Optional[Discover] = None) -> None:
        if not discover:
            discover = Discover(Zeroconf())
        self._discover = discover

    def run(self) -> None:
        self._discover.launch()
        if self._discover.not_alone.wait(float(Constants.DISCOVERY_TIMEOUT.value)):
            logger.info(f"{self.__class__.__name__}: Gateway found")
            self.context.set_state(GatewayFound(self._discover))
        else:
            logger.info(f"{self.__class__.__name__}: No gateway found")
            self.context.set_state(GatewayNotFound(self._discover))


class GatewayNotFound(State):

    def __init__(self, discover: Discover) -> None:
        self._discover = discover

    def run(self) -> None:
        self._discover.stop()

        self.context.set_role(Constants.ROLE_GATEWAY.value)
        self.context.set_state(GatewayState(self._discover))


class GatewayFound(State):

    def __init__(self, discover: Discover) -> None:
        self._discover = discover

    def run(self) -> None:
        self._discover.stop()
        self.context.set_state(WorkerState(self._discover))


class WorkerState(State):

    def __init__(self, discover: Discover) -> None:
        self._discover = discover

    def run(self) -> None:

        announcer = Announcer(self._discover.zeroconf_instance)
        announcer.add_service(DinasoreService.worker())
        announcer.announce_services()

        print("State WorkerState. Working...")
        while True:
            time.sleep(1)
            print(".", end="", flush=True)


class GatewayState(State):

    def __init__(self, discover: Discover) -> None:
        self._discover = discover

    def run(self) -> None:
        announcer = Announcer(self._discover.zeroconf_instance)
        announcer.add_service(DinasoreService.gateway())
        announcer.announce_services()
        self._discover.set_callback(self.context.discovery_callback)
        self._discover.launch()

        print("State GatewayState. Managing...")
        while True:
            time.sleep(1)
            print(".", end="", flush=True)
