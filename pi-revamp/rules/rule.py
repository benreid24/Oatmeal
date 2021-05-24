from typing import List, Tuple
from datetime import datetime

from datastore.datastore import Datastore
from arduino.interface import ArduinoInterface
from arduino.command import Command
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
        datastore: Datastore) -> Tuple[List[Command], List[Message]]:
        """
        Derived classes should implement this method to enforce their rules
        """
        raise RuleException(Message(MessageLevel.WARNING, f'apply() is unimplemented in rule class {type(self).__name__}'))
