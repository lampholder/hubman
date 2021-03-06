"""Simple module to wrangle database connectivity."""
import sqlite3

_CONNECTION = None

def connect(filename='timelines.db'):
    """Establishes shared connection to specified sqlite3 db"""
    global _CONNECTION

    _CONNECTION = sqlite3.connect(filename)
    _CONNECTION.row_factory = sqlite3.Row

def connection():
    """Retrieves the shared connection, connecting if necessary."""
    global _CONNECTION
    if _CONNECTION is None:
        connect()
    return _CONNECTION
