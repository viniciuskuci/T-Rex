from __future__ import annotations  # python 3.7
from typing import Optional
from abc import ABC, abstractmethod
from . import types
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

    def discovery_callback(
        self, info: ServiceInfo, event: types.DiscoveryEvent
    ) -> None:

        if types.get_self_ip() == socket.inet_ntoa(info.addresses[0]):
            return

        if event == types.DiscoveryEvent.ADDED:
            role = info.properties.get(b"role", b"").decode("utf-8")
            if role == self._role == types.ROLE_GATEWAY:
                logger.warning(
                    f"{types.get_self_ip()}: Another gateway found in the network! {socket.inet_ntoa(info.addresses[0])}:{info.port}"
                )
            elif role == types.ROLE_WORKER and self._role == types.ROLE_GATEWAY:
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

        elif event == types.DiscoveryEvent.REMOVED:
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

        elif event == types.DiscoveryEvent.UPDATED:
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
