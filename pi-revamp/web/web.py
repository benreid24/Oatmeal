from arduino.sensor import Sensor
from .message import Message


class Web:
    """
    This class provides the interface for publishing data live to
    oatmeal.rocks. No mock is needed
    """

    def __init__(self):
        pass

    def send_sensor(self, sensor: Sensor):
        """
        Sends the sensor information to the website
        """
        pass

    def send_message(self, message: Message):
        """
        Sends the message to the website. Performs throttling on error
        messages as they tend to come in bursts
        """
        pass
