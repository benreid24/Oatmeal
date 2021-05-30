import unittest
from datetime import datetime

from rules.daytime_light import DaytimeLightRule
from arduino.command import CommandType
from arduino.command_set import CommandSet


class DaytimeLightTest(unittest.TestCase):
    def test_morning_off(self):
        rule = DaytimeLightRule()
        commands = CommandSet()

        messages = rule.apply(
            datetime(2021, 5, 16, 8, 24, 0),
            None,
            None,
            commands
        )
        commands = commands.get_commands()

        self.assertEqual(len(messages), 0)
        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].command_type, CommandType.LIGHT_OFF)
