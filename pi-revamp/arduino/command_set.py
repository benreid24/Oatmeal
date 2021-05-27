from typing import List

from .command import Command, CommandType

_HEAT_COMMANDS = (CommandType.HEAT_OFF, CommandType.HEAT_ON)
_LIGHT_COMMANDS = (CommandType.LIGHT_OFF, CommandType.LIGHT_ON)
_MIST_COMMANDS = (CommandType.MIST,)


class CommandSet:
    """
    Represents a set of commands to send to the Arduino once rules are applied.
    The point of this class is to prioritize conflicting commands.

    Example: Daytime heat rule turns off heat at night but emergency heat rule
             turns the heat on at night if temp is too low.
    """
    def __init__(self):
        self.heat_command = None
        self.light_command = None
        self.mist_command = None

    def add_command(self, command: Command, override: bool=False):
        """
        Adds the given command to the command set. Commands of the same type are only added
        if override is set to true. High priority (emergency) commands should specify override
        as true while low priority commands should specify as false
        """

        if command.command_type in _HEAT_COMMANDS:
            if not self.heat_command or override:
                self.heat_command = command
        
        elif command.command_type in _LIGHT_COMMANDS:
            if not self.light_command or override:
                self.light_command = command

        elif command.command_type in _MIST_COMMANDS:
            if not self.mist_command or override:
                self.mist_command = command

    def get_commands(self) -> List[Command]:
        """
        Returns the compiled list of commands to run
        """
        
        return [cmd for cmd in [self.heat_command, self.mist_command, self.light_command] if cmd]
