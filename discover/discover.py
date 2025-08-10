from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from utils import *

services = {}

class Discover(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")
        if name in services:
            del services[name]
            print(f"Services list: {services}")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        address = translate_address(info.addresses[0])
        if address is None:
            print(f"Service {name} has no address")
            return
        services[name] = address
        print(f"Service {name} added")
        print(f"Services list: {services}")
        


zeroconf = Zeroconf()
listener = Discover()
browser = ServiceBrowser(zeroconf, "_dinasore._tcp.local.", listener, question_type="A")
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()