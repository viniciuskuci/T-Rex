from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from utils import *

services = {}

class MyListener(ServiceListener):

    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        address = translate_address(info.addresses[0]) if info.addresses else "No address"
        print(f"Service {name} added, service: {info}")
        print(f"Service {name} address: {address}")


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_dinasore._tcp.local.", listener, question_type="A")
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()