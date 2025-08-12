from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from utils import *
import logging

logger = logging.getLogger("__name__")
logging.basicConfig(filename="logs.log", level=logging.INFO, format='%(asctime)s %(levelname)-7s - %(module)-9s - %(funcName)-20s - %(message)s', datefmt='[%Y-%m-%d %H:%M:%S] -')


services = {}

class Discover(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logger.info(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logger.info(f"Service {name} removed")
        if name in services:
            del services[name]
            logger.info(f"Services list: {services}")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        address = translate_address(info.addresses[0])
        if address is None:
            logger.warning(f"Service {name} has no address. Cannot add to services list.")
            return
        services[name] = address
        logger.info(f"Service {name} added")
        print(f"Services list: {services}")
        


zeroconf = Zeroconf()
listener = Discover()
browser = ServiceBrowser(zeroconf, "_dinasore._tcp.local.", listener, question_type="A")
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()