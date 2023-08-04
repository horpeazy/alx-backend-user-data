import re
import logging
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str):
    """filters a message and obfuscates data
    fields: List[str]
        list of fields to obfuscate
    redaction: str
        string to replace obfuscated data with
    message: str
        message to obfuscate
    seperator: str
        seperator string in message
    """
    for field in fields:
        message = re.sub(rf"{field}=[^{seperator}]+",
                         f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initializes the class and sets instance attributes
        Parameters:
        fields: List[str]
            list of strings of fields to obfuscate
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ formats the specified log record as text
        Parameters:
        ----------
        record: logging.LogRecord
            record to format
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)
