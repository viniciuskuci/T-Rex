import json
from typing import Optional
import os
from .interface import DatabaseInterface
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class JsonDatabase(DatabaseInterface):

    def __init__(self, filepath: str):

        if os.path.exists(filepath) and filepath.endswith(".json"):
            
            with open(filepath, "r+") as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    f.truncate()
                    json.dump([], f, indent=4)

        else:
            logger.warning(f"Database does not exists. Creating {filepath}")
            try:
                with open(filepath, "w") as f:
                    json.dump([], f, indent=4)
            except Exception as err:
                logger.error(f"Could not create a Json database: {err}")

        self._file = filepath

    def connect(self):
        return super().connect()
    
    def disconnect(self):
        return super().disconnect()
    
    def add_devices(self, devices: list) -> Optional[list]:

        with open(self._file, "r") as f:
            data = json.load(f)

        for device in devices:
            if not self.exists(device["name"], data):
                data.append(device)
            else:
                logger.info(f"Device {device["name"]} already exists on database. Skipping")
        
        with open(self._file, "w") as f:
            json.dump(data, f, indent=4)
        
    def remove_device(self, device):

        with open(self._file, "r") as f:
            data = json.load(f)

        idx = next((i for i, item in enumerate(data) if item["name"] == device["name"]), None)

        if idx is None:
            logger.info("Could not remove the device: Device not found.")
            return False
        
        else:
            data.pop(idx)
            logger.info(f"Device {device["name"]} removed successfully.")

            with open(self._file, "w") as f:
                json.dump(data, f, indent=4)

            return True
    
    def get_devices(self, filter):
        return super().get_devices(filter)
    
    def update_device(self, filter, devices):

        with open(self._file, "r") as f:
            data = json.load(f)

        if filter[0] == "name":
            for item in data:
                for device in devices:
                    if item.get("name") == device.get("name"):
                        item["ip"] = device["ip"]
        
        with open(self._file, "w") as f:
            json.dump(data, f, indent=4)
        
    
    @staticmethod
    def exists(name: str, database: list):
        return any(device["name"] == name for device in database)
     
if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    device_1 = {
        "name": "dinasore1",
        "ip": "10.20.30.2",
       "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    }

    device_2 = {
        "name": "dinasore2",
        "ip": "10.20.30.3",
       "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    }

    database = JsonDatabase("teste.json")
    database.add_devices([device_1, device_2])
    database.add_devices([device_2])
    database.remove_device(device_2)
    database.update_device(("name", "dinasore1"), [{"name": "dinasore1", "ip": "10.20.30.4"}])