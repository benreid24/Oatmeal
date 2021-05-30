from typing import List

from .sensor import Sensor
from .exceptions import ArduinoPythonException
from .command import Command

class ArduinoInterface:
    def __init__(self):
        self.sensors = {}
        self.messages = []

    def update(self):
        """
        Updates the Arduino module. The live Arduino class will read
        from serial and updates the sensors and messages members
        """
        raise ArduinoPythonException('update() not implemented')

    def process_command(self, cmd: Command):
        """
        Meant to be implemented in child classes to handle commands from the controller
        """
        raise ArduinoPythonException('process_command() not implemented')

    def get_messages(self) -> List[str]:
        """
        Returns messages received from Arduino since last call. Clears
        internal message queue
        """
        messages = self.messages
        self.messages = []
        return messages

    def get_sensor(self, name:str , index:int=None) -> Sensor:
        """
        Returns the most recently read value for the given sensor. If an
        index is specified that is also used to resolve the sensor to read
        """
        if index:
            name = f'{name}:{index}'
        if name in self.sensors:
            return self.sensors[name]
        else:
            raise ArduinoPythonException(f'Attempted to read invalild sensor: {name}')

    def update_sensor(self, sensor: Sensor):
        """
        Updates the sensor information for the passed sensor. Meant to be called by
        derived classes
        """
        self.sensors[sensor.name] = sensor

    def add_message(self, message: str):
        """
        Adds the given message to the message queue. Meant to be called by child classes
        """
        self.messages.append(message)
