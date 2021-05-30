import unittest
from datetime import datetime

from datastore.test_datastore import TestDatastore
from rules.daytime_light import DaytimeLightRule
from arduino.command import CommandType
from arduino.command_set import CommandSet
from web.message import MessageLevel

EVENING_LIGHT = 'daytime-evening-light'


class DaytimeLightTest(unittest.TestCase):
    def test_morning_off(self):
        rule = DaytimeLightRule()
        commands = CommandSet()
        datastore = TestDatastore()

        messages = rule.apply(
            datetime(2021, 5, 16, 8, 24, 0),
            None,
            datastore,
            commands
        )
        commands = commands.get_commands()

        self.assertEqual(len(messages), 0)
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].command_type, CommandType.LIGHT_OFF)
