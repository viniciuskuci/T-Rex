from __future__ import annotations  # python 3.7
from typing import Optional
from abc import ABC, abstractmethod
from .models import Constants, DiscoveryEvent, get_self_ip
from zeroconf import ServiceInfo
import socket
import logging
from database.interface import DatabaseInterface

logger = logging.getLogger("DiscoveryFSM")


class Context:

    _state: Optional[State] = None

    def __init__(
        self, initial_state: State, database: Optional[DatabaseInterface] = None
    ):
        self._state = initial_state
        self._state.context = self
        self._role = None
        self._database = database

    def start(self) -> None:
        while self._state is not None:
            self._state.run()

    def set_state(self, state: State) -> None:
        logger.info(f"{self._state.__class__.__name__} -> {state.__class__.__name__}")
        self._state = state
        self._state.context = self

    def set_role(self, role: str) -> None:
        self._role = role

    def discovery_callback(self, info: ServiceInfo, event: DiscoveryEvent) -> None:

        if get_self_ip() == socket.inet_ntoa(info.addresses[0]):
            return

        if event == DiscoveryEvent.ADDED:
            role = info.properties.get(b"role", b"").decode("utf-8")
            if role == self._role == Constants.ROLE_GATEWAY.value:
                logger.warning(
                    f"{get_self_ip()}: Another gateway found in the network! {socket.inet_ntoa(info.addresses[0])}:{info.port}"
                )
            elif (
                role == Constants.ROLE_WORKER.value
                and self._role == Constants.ROLE_GATEWAY.value
            ):
                logger.info(f"New Worker found: {info}")
                if self._database:
                    self._database.add_devices(
                        [
                            {
                                "name": info.name,
                                "ip": socket.inet_ntoa(info.addresses[0]),
                                "mac": ":".join(
                                    f"{b:02x}" for b in info.properties.get(b"mac", b"")
                                ),
                            }
                        ]
                    )

        elif event == DiscoveryEvent.REMOVED:
            logger.info(f"Service removed: {info}")
            if self._database:
                self._database.remove_device(
                    {
                        "name": info.name,
                        "ip": socket.inet_ntoa(info.addresses[0]),
                        "mac": ":".join(
                            f"{b:02x}" for b in info.properties.get(b"mac", b"")
                        ),
                    }
                )

        elif event == DiscoveryEvent.UPDATED:
            logger.info(f"Service updated: {info}")
            if self._database:
                self._database.update_device(
                    {
                        "name": info.name,
                        "ip": socket.inet_ntoa(info.addresses[0]),
                        "mac": ":".join(
                            f"{b:02x}" for b in info.properties.get(b"mac", b"")
                        ),
                    }
                )


class State(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context) -> None:
        self._context = context

    @abstractmethod
    def run(self):
        pass
