from abc import ABC, abstractmethod
from typing import Optional


class DatabaseInterface(ABC):

    """
    Interface for different database implementations.

    Methods:
        connect: Connect to the database.
        disconnect: Disconnect from the database.
        add_device: Add a list of devices to the database.
        remove_device: Remove a list of devices from the database.
        get_devices: Get a list of devices from the database.
        update_device: Update a list of devices in the database.
    """

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass
    
    @abstractmethod
    def add_devices(self, devices: list) -> list:
        """
        Add a list of devices to the database.

        Args:
            devices (list): List of devices to add. Each device must be a dictionary.

        Returns:
            Optional(list): List of failed additions.
        """
        pass

    @abstractmethod
    def remove_device(self, device: dict) -> bool:
        """
        Remove a device from the database.

        Args:
            device (dict): The device to remove.

        Returns:
            bool: True if the device was removed successfully, False otherwise.
        """
        pass

    @abstractmethod
    def get_devices(self, filter: tuple) -> Optional[list]:
        """
        Get a list of devices from the database.

        Args:
            filter (tuple): A filter tuple to narrow down the search.

        Returns:
            Optional(list): A list of devices matching the filter or None.
        """
        pass

    @abstractmethod
    def update_device(self, filter: tuple, device: dict) -> list:
        """
        Update a list of devices in the database.

        Args:
            filter (tuple): A filter tuple to narrow down the search.
            devices (dict): Device to update. Must be a dictionary.

        Returns:
            list: List of failed updates.
        """
        pass

