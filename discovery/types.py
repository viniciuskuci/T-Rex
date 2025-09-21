from zeroconf import ServiceInfo
from dataclasses import dataclass
from enum import Enum
import socket


######### Constants #########
DISCOVERY_TIMEOUT = 5
DINASORE_SERVICE_TYPE = "_dinasore._tcp.local."
DINASORE_PORT = 2901
ROLE_GATEWAY = "gateway"
ROLE_WORKER = "worker"


######### Functions #########
def get_self_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None


def get_self_hostname() -> str:

    hostname = socket.gethostname()
    if hostname.endswith(".local"):
        hostname = hostname[:-6]
    return hostname


######### Classes #########
class DiscoveryEvent(Enum):
    ADDED = "add"
    REMOVED = "remove"
    UPDATED = "update"


class DinasoreService:

    @staticmethod
    def worker() -> ServiceInfo:
        ip = get_self_ip()
        name = f"{get_self_hostname()}.{DINASORE_SERVICE_TYPE}"

        return ServiceInfo(
            type_=DINASORE_SERVICE_TYPE,
            name=name,
            addresses=[socket.inet_aton(ip)],
            port=DINASORE_PORT,
            properties={"role": ROLE_WORKER},
        )

    @staticmethod
    def gateway() -> ServiceInfo:
        ip = get_self_ip()
        name = f"{get_self_hostname()}.{DINASORE_SERVICE_TYPE}"

        return ServiceInfo(
            type_=DINASORE_SERVICE_TYPE,
            name=name,
            addresses=[socket.inet_aton(ip)],
            port=DINASORE_PORT,
            properties={"role": ROLE_GATEWAY},
        )
