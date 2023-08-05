#!/usr/bin/env python3
"""A filter_datum function that logs obfuscated messages"""
from typing import List
import re
import logging
import os
from mysql.connector.connection import MySQLConnection

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
    user_data_logger = logging.Logger("user_data")
    user_data_logger.setLevel(logging.INFO)
    user_data_logger.propagate = False
    stream_handler = logging.StreamHandler()
    # Stream handler determines where log messages are sent
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    # Add the handler to the logger
    user_data_logger.addHandler(stream_handler)
    return user_data_logger


def get_db() -> MySQLConnection:
    """Get the db credentials and create a connector obj"""
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    passwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    connector = MySQLConnection(host=db_host,
                                database=db_name,
                                user=user,
                                password=passwd)
    return connector


def main():
    """Retrieve info on users from db and displays a filtered format"""
    connector = get_db()
    logger = get_logger()
    cursor = connector.cursor()
    cursor.execute("SELECT * FROM users")
    usrs = cursor.fetchall()
    message = 'name={}; email={}; phone={}; ssn={}; password={}; ip={}; \
        last_login={}; user_agent={};'
    for row in usrs:
        name, email, phone, ssn, password,\
            ip, last_login, user_agent = row
        logger.info(message.format(name, email, phone, ssn, password, ip,
                                   last_login, user_agent))


if __name__ == '__main__':
    main()
