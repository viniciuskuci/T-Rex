from zeroconf import Zeroconf, ServiceInfo
import socket
from utils import *


class Announcer:
    def __init__(self):
        self.services = []
        self.zeroconf = Zeroconf()

    def announce_services(self):
        for service in self.services:
            try:
                self.zeroconf.register_service(service)
                print(f"Service {service.server} announced on {socket.inet_ntoa(service.addresses[0])}:{service.port}")
            except Exception as e:
                print(f"Error announcing service {service.server}: {e}")
                continue

    def unregister_services(self):
        for service in self.services:
            try:
                self.zeroconf.unregister_service(service)
                print(f"Service {service.server}.{service.type} unregistered")
            except Exception as e:
                print(f"Error unregistering service {service.server}.{service.type}: {e}")
                continue
            
if __name__ == "__main__":
    announcer = Announcer()
    announcer.services = [
        ServiceInfo(
                    '_dinasore._tcp.local.',
                    f"{get_self_hostname()}._dinasore._tcp.local.",
                    addresses=[socket.inet_aton(get_self_ip())],
                    port=2901,
                    server=f"{get_self_hostname()}.local.",
                    properties={},
                )
    ]
    announcer.announce_services()
    try:
        input("Press enter to exit...\n\n")
    finally:
        announcer.unregister_services()
        announcer.zeroconf.close()
