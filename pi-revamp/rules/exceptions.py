from web.message import Message


class RuleException(Exception):
    def __init__(self, message: Message):
        super().__init__(message.message)
        self.web_message = message
