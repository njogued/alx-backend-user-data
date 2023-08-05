#!/usr/bin/env python3
"""A filter_datum function that logs obfuscated messages"""
from typing import List
import re
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize an object"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats messages after filtering them"""
        info = record.getMessage()
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  info, self.SEPARATOR)
        return super().format(record)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """"Separate fields and remove personal info using regex"""
    for field in fields:
        pattern = r'(?<={}=)(.+?)(?={})'.format(field, separator)
        message = re.sub(pattern, redaction, message)
    return message


def get_logger() -> logging.Logger:
    """Get logger returns a logger object"""
    user_data_logger = logging.Logger("user_data", logging.INFO)
    user_data_logger.propagate = False
    stream_handler = logging.StreamHandler()
    # Stream handler determines where log messages are sent
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    # Add the handler to the logger
    user_data_logger.addHandler(stream_handler)
    return user_data_logger

# if __name__ == '__main__':
#     main()
