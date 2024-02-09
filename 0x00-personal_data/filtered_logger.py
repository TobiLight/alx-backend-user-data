#!/usr/bin/env python3
# File: filtered_logger.py
# Author: Oluwatobiloba Light
"""lOG MESSAGE"""

import logging
from typing import List
import re
import os
import mysql.connector


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


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connect to the MySQL database and return a connector"""
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")

    # conntect to database
    return mysql.connector.connection.MySQLConnection(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )


def main() -> None:
    """doc doc doc"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    log = get_logger()
    # for row in cursor:
    #     data = []
    #     for desc, value in zip(cursor.description, row):
    #         pair = f"{desc[0]}={str(value)}"
    #         data.append(pair)
    #     row_str = "; ".join(data)
    #     log.info(row_str)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
