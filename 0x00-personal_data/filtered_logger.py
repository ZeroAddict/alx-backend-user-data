#!/usr/bin/env python3

"""Module for personal data project."""

import logging
import os
import mysql.connector
import re
from typing import List

# Constants
REDACTION = "***"
SEPARATOR = ";"
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

# Patterns for data extraction and replacement
patterns = {
    "extract": lambda fields, separator: r'(?P<field>{})=[^{}]*'.format('|'.join(fields), separator),
    "replace": lambda field: r'\g<field>={}'.format(field),
}

class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""

    def __init__(self, fields: List[str]):
        """Initializes the class."""
        super().__init__("[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s")
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records."""
        msg = super().format(record)
        return filter_datum(self.fields, REDACTION, msg, SEPARATOR)

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Returns the log message with certain fields obfuscated."""
    extract, replace = patterns["extract"], patterns["replace"]
    return re.sub(extract(fields, separator), replace(redaction), message)

def get_logger() -> logging.Logger:
    """Returns a logging.Logger object named "user_data"."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)

    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")

    return mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )

def main() -> None:
    """Obtains a database connection and retrieves all rows in the users table."""
    logger = get_logger()

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        message = "; ".join(f"{field}={value}" for field, value in row.items())
        logger.info(filter_datum(PII_FIELDS, REDACTION, message, SEPARATOR))

if __name__ == "__main__":
    main()