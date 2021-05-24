from enum import Enum


class MessageLevel(Enum):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


class Message:
    def __init__(self, level: MessageLevel, message: str):
        self.level = level
        self.message = message
