from datetime import datetime
from typing import List

from arduino.command import Command, CommandType
from web.message import Message
from arduino.interface import ArduinoInterface
from datastore.datastore import Datastore
from arduino.command_set import CommandSet
from .rule import Rule
from .util import is_daytime


class DaytimeLightRule(Rule):
    def apply(
        self,
        current_time: datetime,
        arduino: ArduinoInterface,
        datastore: Datastore,
        command_set: CommandSet) -> List[Message]:
        
        # daytime is 9am to 9pm
        if is_daytime(current_time):
            command_set.add_command(Command(CommandType.LIGHT_ON), False)
        else:
            command_set.add_command(Command(CommandType.LIGHT_OFF), False)
        return []
