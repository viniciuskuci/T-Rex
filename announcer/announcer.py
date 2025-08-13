from zeroconf import Zeroconf, ServiceInfo
import socket
from .utils import *
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
                logger.info(f"Successfully registered the service {service.name}, announced at {socket.inet_ntoa(service.addresses[0])}:{service.port}")
               
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


