from zeroconf import Zeroconf
from discover import Discover, DiscoverThread
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
        
        try:
            input("Press enter to exit...\n")
        except KeyboardInterrupt:
            logging.info("Program interrupted")
            
    finally:
        print("Exiting main thread...")
        discover_thread.stop()
        zeroconf.close()


if __name__ == "__main__":
    main()