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
