import json

from .exceptions import DatastoreException

_EVENTS_FILE = 'event_history.json'

class Datastore:
    """
    Simple file backed datastore for tracking which events occurred
    on a given day. Prevents duplicate events on restarts
    """

    def __init__(self):
        self.events = {}
        try:
            with open(_EVENTS_FILE, 'r') as file:
                self.events = json.loads(file.read())
        except Exception as e:
            print(f'Failed to load event history: {e}')

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
        try:
            with open(_EVENTS_FILE, 'w') as file:
                file.write(json.dumps(self.events))
        except Exception as e:
            raise DatastoreException(f'Failed to write events: {e}')
