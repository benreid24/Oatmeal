from typing import Tuple, List

from .sensor import Sensor


def parse_serial(line: str) -> Sensor:
    """
    Parses a complete serial line from an Arduino (or mock) and
    returns a Sensor object with the parsed data
    """
    pass


def split_serial(lines: str) -> Tuple[str, List[str]]:
    """
    Takes a sequence of input from an Arduino and splits it into a
    list of full packets and returns a string containing a partial
    packet if present
    """
    packets = lines.split('\n')
    residual = ''
    if lines[-1] != '\n':
        residual = packets[-1]
        packets.pop()
    return residual, packets
