import unittest
from datetime import datetime

from datastore.test_datastore import TestDatastore
from rules.daytime_light import DaytimeLightRule
from arduino.command import CommandType
from arduino.command_set import CommandSet
from web.message import MessageLevel


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

    def test_morning_on(self):
        rule = DaytimeLightRule()
        commands = CommandSet()
        datastore = TestDatastore()

        messages = rule.apply(
            datetime(2021, 5, 16, 9, 24, 0),
            None,
            datastore,
            commands
        )
        commands = commands.get_commands()

        self.assertEqual(len(messages), 1)
        self.assertEqual(len(commands), 1)
        self.assertEqual(messages[0].level, MessageLevel.INFO)
        self.assertEqual(commands[0].command_type, CommandType.LIGHT_ON)

        # No duplicate messages
        messages = rule.apply(
            datetime(2021, 5, 16, 14, 24, 0),
            None,
            datastore,
            CommandSet()
        )

        self.assertEqual(len(messages), 0)

    def test_evening_off(self):
        rule = DaytimeLightRule()
        commands = CommandSet()
        datastore = TestDatastore()

        messages = rule.apply(
            datetime(2021, 5, 16, 21, 0, 0),
            None,
            datastore,
            commands
        )
        commands = commands.get_commands()

        self.assertEqual(len(messages), 1)
        self.assertEqual(len(commands), 1)
        self.assertEqual(messages[0].level, MessageLevel.INFO)
        self.assertEqual(commands[0].command_type, CommandType.LIGHT_OFF)

        # No duplicate messages
        messages = rule.apply(
            datetime(2021, 5, 16, 23, 24, 0),
            None,
            datastore,
            CommandSet()
        )

        self.assertEqual(len(messages), 0)
