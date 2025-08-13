from zeroconf import Zeroconf, ServiceInfo
from discover import Discover, DiscoverThread
from announcer import Announcer
from announcer.utils import get_self_hostname, get_self_ip
import socket
import threading
import logging
import os


logging.basicConfig(
    filename="logs.log", 
    level=logging.INFO, 
    format='%(asctime)s %(levelname)-7s - %(module)-9s - %(funcName)-20s - %(message)s', 
    datefmt='[%Y-%m-%d %H:%M:%S] -'
)

def main():
    main_thread = threading.current_thread()
    logging.info(f"Main thread - {main_thread.name} - started with process ID: {os.getpid()}")
    
    zeroconf = Zeroconf()
    announcer = None
    
    try:
        discover = Discover(zeroconf)
        discover_thread = DiscoverThread(discover)
        discover_thread.start()
        
        if discover.found_service.wait(20):
            logging.info("Service found. Instance is assuming worker role.")
            print("Running in WORKER mode...")
        else:
            logging.info("Service not found. Instance assuming announcer role.")
            discover_thread.stop()
            print("Running in ANNOUNCER mode...")
            announcer = Announcer(zeroconf)
            services = [
                ServiceInfo(
                    '_dinasore._tcp.local.',
                    f"{get_self_hostname()}._dinasore._tcp.local.",
                    addresses=[socket.inet_aton(get_self_ip())],
                    port=2901,
                    server=get_self_hostname(),
                    properties={},
                )
            ]
            for service in services:
                announcer.add_service(service)

            announcer.announce_services()

        try:
            input("Press enter to exit...\n")
        except KeyboardInterrupt:
            logging.info("Program interrupted")
            
    finally:
        print("Exiting main thread...")
        if announcer:
            announcer.unregister_services()
        discover_thread.stop()
        zeroconf.close()


if __name__ == "__main__":
    main()
