"""
This script serves as a database connection helper.
"""

import sqlite3
from pathlib import Path
from typing import Generator


def get_db() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(str("data/mil_cha_game.db"), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()