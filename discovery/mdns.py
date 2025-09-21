from zeroconf import Zeroconf, ServiceInfo, ServiceBrowser, ServiceListener
from typing import Optional, Callable
import threading
import os
from .types import DiscoveryEvent
import socket
import logging

logger = logging.getLogger(__name__)


class Announcer:
    def __init__(self, zeroconf: Zeroconf) -> None:
        self._services = []
        self.zeroconf = zeroconf

    def add_service(self, service: ServiceInfo) -> None:
        self._services.append(service)

    def announce_services(self) -> None:
        for service in self._services:
            try:
                self.zeroconf.register_service(service)
                logger.info(
                    f"Successfully registered the service {service.name}, announced at {socket.inet_ntoa(service.addresses[0])}:{service.port}"
                )

            except Exception as e:
                logger.error(f"Could not announce the service {service.name}: {e}")
                continue

    def unregister_services(self) -> None:
        for service in self._services:
            try:
                self.zeroconf.unregister_service(service)
                logger.info(f"Successfully unregistered the service {service.name}")
            except Exception as e:
                logger.error(f"Could not unregister the service {service.name}: {e}")
                continue

    @property
    def services(self) -> list[ServiceInfo]:
        return self._services.copy()


class Discover(ServiceListener):
    def __init__(self, zeroconf: Zeroconf, callback: Optional[Callable] = None) -> None:
        self._zeroconf = zeroconf
        self._browser = None
        self._callback = callback
        self.not_alone = threading.Event()

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        try:
            info = zc.get_service_info(type_, name)
            if self._callback:
                self._callback(info=info, event=DiscoveryEvent.UPDATED)

        except Exception as e:
            logger.error(f"Error updating service {name}: {e}")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        try:
            if self._callback:
                self._callback(
                    info=zc.get_service_info(type_, name), event=DiscoveryEvent.REMOVED
                )
        except Exception as e:
            logger.error(f"Error removing service {name}: {e}")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        try:
            info = zc.get_service_info(type_, name)
            if not self.not_alone.is_set():
                if info.properties.get(b"role", b"").decode("utf-8") == "gateway":
                    self.not_alone.set()
            if self._callback:
                self._callback(info=info, event=DiscoveryEvent.ADDED)
        except Exception as e:
            logger.error(f"Error adding service {name}: {e}")

    def launch(self) -> bool:
        try:
            if self._browser:
                logger.warning("ServiceBrowser already running")
                return True
            self._browser = ServiceBrowser(
                self._zeroconf, "_dinasore._tcp.local.", self, question_type="A"
            )
            logger.info("ServiceBrowser started")
            return True

        except Exception as e:
            logger.error(f"Error starting ServiceBrowser: {e}")
            return False

    def stop(self) -> None:
        if self._browser:
            try:
                self._browser.cancel()
                self._browser = None
                logger.info("ServiceBrowser stopped")
            except Exception as e:
                logger.error(f"Error while stopping ServiceBrowser: {e}")
        else:
            logger.warning("ServiceBrowser was not running")

    def set_callback(self, callback: Callable) -> None:
        self._callback = callback

    @property
    def zeroconf_instance(self) -> Zeroconf:
        return self._zeroconf


"""
------- Review -------
"""


class DiscoverThread(threading.Thread):
    def __init__(self, discover: Discover) -> None:
        super().__init__(daemon=True)
        self._discover = discover
        self._sleep_time = 60
        self._pid = None
        self._stop_event = threading.Event()

    def run(self) -> None:
        self._pid = os.getpid()
        self._process_name = threading.current_thread().name
        logger.info(
            f"Discover thread - {self._process_name} - started with thread ID: {self._pid}"
        )

        if not self._discover.launch():
            return

        try:
            while not self._stop_event.is_set():
                self._health_check()
                if self._stop_event.wait(self._sleep_time):
                    break

        except Exception as e:
            logger.error(f"Error in discover thread: {e}")

        finally:
            self._discover.stop()
            logger.info(
                f"Discover thread - {self._process_name} - stopped with thread ID: {self._pid}"
            )

    def _health_check(self) -> None:
        logger.info(
            f"Discover thread - {self._process_name} - running with thread ID: {self._pid}"
        )

    def stop(self) -> None:
        logger.info(
            f"Stopping discover thread - {self._process_name} - with thread ID: {self._pid}"
        )
        self._stop_event.set()
