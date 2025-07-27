from zeroconf import Zeroconf, ServiceInfo
import socket
from utils import *


def announce_service():

    service_type = "_dinasore._tcp.local."
    host_name = get_self_hostname()
    port = 2901
    self_ip = get_self_ip()

    zeroconf = Zeroconf()

    service = ServiceInfo(
        service_type,
        f"{host_name}.{service_type}",
        addresses=[socket.inet_aton(self_ip)],
        port=port,
        server=f"{host_name}.local.",
        properties={},
    )

    zeroconf.register_service(service)
    print(f"Service {host_name} announced on {self_ip}:{port}")
    print(f"Service type: {service_type}")
    print(f"Hostname: {host_name}")

    try:
        input("Press enter to exit...\n\n")
    finally:
        zeroconf.unregister_service(service)
        zeroconf.close()
announce_service()
