class ArduinoPythonException(Exception):
    """
    This denotes an error with the Python code interfacing with an Arduino.
    Example: Reading a sensor that does not exist
    """
    def __init__(self, message: str):
        super().__init__(message)

class ArduinoRuntimeException(Exception):
    """
    This denotes an error with an actual Arduino. May be caused by bad serial
    data, disconnect, or any other runtime error
    """
    def __init__(self, message: str):
        super().__init__(message)
