from enum import Enum


class CommandType(Enum):
    LIGHT_ON = 1
    LIGHT_OFF = 2

    HEAT_ON = 3
    HEAT_OFF = 4

    MIST = 5


class Command:
    def __init__(self, command_type: CommandType, length: int=None):
        self.command_type = command_type
        if length:
            self.length = length
