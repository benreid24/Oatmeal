from typing import List
from datetime import datetime

from datastore.datastore import Datastore
from arduino.interface import ArduinoInterface
from arduino.command_set import CommandSet
from web.message import Message, MessageLevel
from.exceptions import RuleException


class Rule:
    """
    Base class for tank controller rules
    """
    
    def apply(
        self,
        current_time: datetime,
        arduino: ArduinoInterface,
        datastore: Datastore,
        command_set: CommandSet) -> List[Message]:
        """
        Derived classes should implement this method to enforce their rules. Commands
        should be added to the command_set parameter object. Any messages to be published
        to the website should be returned as a list
        """
        raise RuleException(Message(
            MessageLevel.WARNING,
            f'apply() is unimplemented in rule class {type(self).__name__}'
        ))
