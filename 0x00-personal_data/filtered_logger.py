#!/usr/bin/env python3
# File: filtered_logger.py
# Author: Oluwatobiloba Light
"""lOG MESSAGE"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated"""
    pattern = r'({0})=([^{1}]+)(?={1}|$)'.\
        format('|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, r'\1=' + redaction + ';', message)
