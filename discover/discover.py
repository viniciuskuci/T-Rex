from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
from .utils import *
import logging
import threading
import os

logger = logging.getLogger(__name__)

SERVICES = {} #will be replaced by a database in the future

class Discover(ServiceListener):
    def __init__(self, zeroconf: Zeroconf) -> None:
        self._zeroconf = zeroconf
        self._browser = None
        
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logger.info(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        logger.info(f"Service {name} removed")
        if name in SERVICES:
            del SERVICES[name]
            logger.info(f"Services list: {SERVICES}")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        address = translate_address(info.addresses[0])
        if address is None:
            logger.warning(f"Service {name} has no address. Cannot add to services list.")
            return
        SERVICES[name] = address
        logger.info(f"Service {name} added")
        print(f"Services list: {SERVICES}")
        #add here the script to add the device to the database
    
    def _add_to_database(self) -> None:
        """adds a new device to the database"""
        pass

    def launch(self) -> bool:
        try:
            if self._browser:
                logger.warning("ServiceBrowser already running")
                return True
            self._browser = ServiceBrowser(self._zeroconf, "_dinasore._tcp.local.", self, question_type="A")
            logger.info("ServiceBrowser started")
            return True
        
        except Exception as e:
            logger.error(f"Error starting ServiceBrowser: {e}")
            return False
    
    def stop(self) -> None:
        if self._browser:
            try:
                self._browser.cancel()
                self._browser = None
                logger.info("ServiceBrowser stopped")
            except Exception as e:
                logger.error(f"Error while stopping ServiceBrowser: {e}")
        else:
            logger.warning("ServiceBrowser was not running")

class DiscoverThread(threading.Thread):
    def __init__(self, discover: Discover) -> None:
        super().__init__(daemon=True)
        self._discover = discover
        self._sleep_time = 60
        self._pid = None
        self._stop_event = threading.Event()

    def run(self) -> None:
        self._pid = os.getpid()
        self._process_name = threading.current_thread().name
        logger.info(f"Discover thread - {self._process_name} - started with thread ID: {self._pid}")

        if not self._discover.launch(): 
            return
        
        try:
            while not self._stop_event.is_set():
                self._health_check()
                if(self._stop_event.wait(self._sleep_time)):
                    break

        except Exception as e:
            logger.error(f"Error in discover thread: {e}")

        finally:
            self._discover.stop()
            logger.info(f"Discover thread - {self._process_name} - stopped with thread ID: {self._pid}")

    def _health_check(self) -> None:
        logger.info(f"Discover thread - {self._process_name} - running with thread ID: {self._pid}")

    def stop(self) -> None:
        logger.info(f"Stopping discover thread - {self._process_name} - with thread ID: {self._pid}")
        self._stop_event.set()