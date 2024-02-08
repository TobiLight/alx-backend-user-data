#!/usr/bin/env python3
# File: filtered_logger.py
# Author: Oluwatobiloba Light
"""lOG MESSAGE"""

import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated"""
    pattern = r'({0})=([^{1}]+)(?={1}|$)'.\
        format('|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, r'\1=' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


PII_FIELDS = ["name", "email", "phone", "ssn", "password"]


def get_logger() -> logging.Logger:
    """Configure and return a logger named 'user_data'"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Create StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    # Add StreamHandler to logger
    logger.addHandler(stream_handler)

    return logger
