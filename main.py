from zeroconf import ServiceBrowser, Zeroconf
from discover import Discover, DiscoverThread
import announcer
import threading
import logging


logging.basicConfig(
    filename="logs.log", 
    level=logging.INFO, 
    format='%(asctime)s %(levelname)-7s - %(module)-9s - %(funcName)-20s - %(message)s', 
    datefmt='[%Y-%m-%d %H:%M:%S] -'
)

def main():
    main_thread = threading.current_thread()
    logging.info(f"Main thread - {main_thread.name} - started with thread ID: {threading.get_ident()}")
    with Zeroconf() as zeroconf:
        discover = Discover(zeroconf)
        discover_thread = DiscoverThread(discover)
        discover_thread.start()
    try:
        input("Press enter to exit...\n\n")
    finally:
        discover_thread.stop()
        logging.info("T-Rex service discovery stopped.")

if __name__ == "__main__":
    main()