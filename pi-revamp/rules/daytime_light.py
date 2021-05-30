from datetime import datetime
from typing import List

from arduino.command import Command, CommandType
from web.message import Message, MessageLevel
from arduino.interface import ArduinoInterface
from datastore.datastore import Datastore
from arduino.command_set import CommandSet
from .rule import Rule
from .util import is_daytime

MORNING_LIGHT = 'daytime-morning-light'
EVENING_LIGHT = 'daytime-evening-light'


class DaytimeLightRule(Rule):
    def apply(
        self,
        current_time: datetime,
        arduino: ArduinoInterface,
        datastore: Datastore,
        command_set: CommandSet) -> List[Message]:
        
        messages = []

        # daytime is 9am to 9pm
        if is_daytime(current_time):
            command_set.add_command(Command(CommandType.LIGHT_ON), False)

            if datastore.get_event_day(MORNING_LIGHT) != current_time.day:
                datastore.set_event_day(MORNING_LIGHT, current_time.day)
                messages.append(Message(
                    MessageLevel.INFO,
                    'Turning on tank light'
                ))
        else:
            command_set.add_command(Command(CommandType.LIGHT_OFF), False)

            if current_time.hour >= 21 and datastore.get_event_day(EVENING_LIGHT) != current_time.day:
                datastore.set_event_day(EVENING_LIGHT, current_time.day)
                messages.append(Message(
                    MessageLevel.INFO,
                    'Turning off tank light'
                ))
        
        return messages
