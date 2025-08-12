from zeroconf import Zeroconf, ServiceInfo
import socket
from utils import *
import logging

logger = logging.getLogger("__name__")
logging.basicConfig(filename="logs.log", level=logging.INFO, format='%(asctime)s %(levelname)-7s - %(module)-9s - %(funcName)-20s - %(message)s', datefmt='[%Y-%m-%d %H:%M:%S] -')


class Announcer:
    def __init__(self):
        self.services = []
        self.zeroconf = Zeroconf()

    def announce_services(self):
        for service in self.services:
            try:
                self.zeroconf.register_service(service)
                logger.info(f"Successfully registered the service {service.name}, announced at {socket.inet_ntoa(service.addresses[0])}:{service.port}")
               
            except Exception as e:
                logger.error(f"Could not announce the service {service.name}: {e}")
                continue

    def unregister_services(self):
        for service in self.services:
            try:
                self.zeroconf.unregister_service(service)
                logger.info(f"Successfully unregistered the service {service.name}")
            except Exception as e:
                logger.error(f"Could not unregister the service {service.name}: {e}")
                continue
            
if __name__ == "__main__":
    announcer = Announcer()
    announcer.services = [
        ServiceInfo(
                    '_dinasore._tcp.local.',
                    f"{get_self_hostname()}._dinasore._tcp.local.",
                    addresses=[socket.inet_aton(get_self_ip())],
                    port=2901,
                    server=get_self_hostname(),
                    properties={},
                )
    ]
    announcer.announce_services()
    try:
        input("Press enter to exit...\n\n")
    finally:
        announcer.unregister_services()
        announcer.zeroconf.close()
