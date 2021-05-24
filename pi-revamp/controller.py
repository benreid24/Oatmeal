from datetime import datetime
from typing  import List, Tuple

from arduino.interface import ArduinoInterface
from arduino.command import Command
from datastore.datastore import Datastore
from web.message import Message
from rules.rule import Rule

RULES: List[Rule] = []


def control_tank(
    current_time: datetime,
    arduino: ArduinoInterface,
    datastore: Datastore) -> Tuple[List[Command], List[Message]]:
    """
    Performs all control logic for the tank. No side effects. Tank controls
    are returned using the command pattern. All inputs are mockable
    """
    commands = []
    messages = []

    for rule in RULES:
        rule_cmds, rule_msgs = rule.apply(current_time, arduino, datastore)
        commands.extend(rule_cmds)
        messages.extend(rule_msgs)

    return commands, messages
