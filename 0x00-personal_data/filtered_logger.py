#!/usr/bin/env python3
"""A filter_datum function that logs obfuscated messages"""
import re


def filter_datum(fields, redaction, messages, separator):
    """Function to separate fields and redact info using regex"""
    return ';'.join([re.sub(r'({})=[^&]+'.format(i), f'{i}={redaction}', x)
                     if (i := x.split('=')[0]) in fields else x
                     for x in messages.split(separator)])
