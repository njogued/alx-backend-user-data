#!/usr/bin/env python3
"""A filter_datum function that logs obfuscated messages"""
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError


def filter_datum(fields, redaction, message, separator):
    """Function to separate fields and redact info using regex"""
    return ';'.join([re.sub(r'({})=[^&]+'.format(i), f'{i}={redaction}', x)
                     if (i := x.split('=')[0]) in fields else x
                     for x in message.split(separator)])
