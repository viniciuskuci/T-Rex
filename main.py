from discovery import discovery
import logging
from database.json_db import JsonDatabase

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(name)s - %(message)s",
    datefmt="[%Y-%m-%d %H:%M:%S] -",
)


def main():
    database = JsonDatabase("devices.json")
    discovery.start_discovery(database)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted by user.")
