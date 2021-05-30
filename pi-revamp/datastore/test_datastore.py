import json

from .exceptions import DatastoreException


class TestDatastore:
    """
    Simple in memory datastore for tracking which events occurred
    on a given day. Useful for unit tests
    """

    def __init__(self):
        self.events = {}

    def get_event_day(self, event: str) -> int:
        """
        Returns the day of the month that the given event last
        occurred on. See event module for event types
        """
        return self.events[event] if event in self.events else -1

    def set_event_day(self, event: str, day: int):
        """
        Sets the day of the month that the given event last
        occurred on
        """
        self.events[event] = day
