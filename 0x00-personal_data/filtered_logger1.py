#!/usr/bin/env python3
"""A filter_datum function that logs obfuscated messages"""
import re


def filter_datum(fields, redaction, messages, separator):
    """Function to separate fields and redact info using regex"""
    blocks = messages.split(separator)
    newblock = []
    for item in blocks:
        param = item.split('=')[0]
        if param in fields:
            newitem = re.sub(r'({})=[^&]+'.format(param),
                             f'{param}={redaction}', item)
        else:
            newitem = item
        newblock.append(newitem)
    return ";".join(newblock)


def filter_datum1(fields, redaction, message, separator):
    for field in fields:
        message = re.sub(rf"{field}=(.*?)\{separator}",
                         f'{field}={redaction}{separator}', message)
    return message


def filter_datum2(fields, redaction, message, separator):
    """ask gpt to explain"""
    return ';'.join([re.sub(r'({})=[^&]+'.format(i), f'{i}={redaction}', x)
                     if (i := x.split('=')[0]) in fields else x
                     for x in message.split(separator)])
