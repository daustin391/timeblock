"""
Provide classes for working with SQLite3 database.

Database class provides a context manager for managing SQLite connections
and cursors. It provides methods for executing queries and scripts.

TimeblockDB is a subclass of Database that provides methods specific
to the Timeblock application.

This module contains the following constants:
    - DB: TypeVar for Database class, for type hinting
    - SqlType: Union of types that can be stored in SQLite3 database
    - SqlSeq: Type for parameters in queries
"""

import sqlite3
from sqlite3 import Error, Connection, Cursor

from typing import (
    Union,
    Optional,
    TypeVar,
    Sequence,
    Mapping,
    Iterable,
)
from datetime import datetime, date, timedelta
from typing_extensions import TypeGuard
from timeblock.action import Action


DB = TypeVar("DB", bound="Database")
SqlType = Union[None, int, float, str, bytes, date, datetime, timedelta]
SqlSeq = Union[tuple[SqlType, ...], dict[str, SqlType]]


class Database:
    """
    Context manager for managing SQLite connections and cursors.

    Attributes:
        connection: SQLite3 connection object
        cursor: SQLite3 cursor object
        filename: Name of database file

    Methods:
        read_query(query: str, parameters: Optional = None) -> list[tuple]:
            Send SQL query for data to database, optionally with parameters,
            and return result as list of tuples.
        write_query(
            query: str,
            parameters: Union[SqlSeq, Sequence[SqlSeq], None] = None,
        ) -> Optional[int]: Send query to write to database
        is_not_string: Type checks if object is a string
        is_list_of_iter: Type checks if object is a list of iterables
        script: Execute SQL script
    """

    def __init__(self, filename: Optional[str] = None):
        """
        Initialize Database object.

        Args:
            filename (str): Name or path to database file.
        """
        self.connection: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None
        self.filename = filename if filename else "db.sql"

    def __enter__(self: DB):
        """Enter context manager, open connection and cursor."""
        self.connection = sqlite3.connect(self.filename)
        print(f"Connected to {self.filename}")
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        """Exit context manager, close connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def __repr__(self):
        """Return string resembling constructor call."""
        return f'DB("{self.filename}")'

    def read_query(
        self, query: str, parameters: Optional[Union[tuple, dict]] = None
    ) -> list[tuple]:
        """Send query for data from database."""
        result: list[tuple] = []
        if self.cursor:
            try:
                if parameters:
                    self.cursor.execute(query, parameters)
                else:
                    self.cursor.execute(query)
                result = self.cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
        else:
            print("Error: no cursor, are you using 'with'?")
        return result

    def write_query(
        self,
        query: str,
        parameters: Union[SqlSeq, Sequence[SqlSeq], None] = None,
    ) -> Optional[int]:
        """
        Write to database.

        Returns lastrowid, the row number of the last
        successful INSERT or REPLACE using execute().
        executemany() and executescript() don't update lastrowid.
        If no successful INSERTs into table occurred
        on connection then lastrowid == 0.
        """
        if self.cursor and self.connection:
            try:
                if not parameters:
                    self.cursor.execute(query)
                elif isinstance(parameters, Sequence) and self.is_list_of_iter(
                    parameters
                ):
                    self.cursor.executemany(query, parameters)
                elif isinstance(parameters, (dict, tuple, list)):
                    self.cursor.execute(query, parameters)
                self.connection.commit()
                return self.cursor.lastrowid

            except Error as e:
                print(f"Error: {e}")
        else:
            print("Error: no cursor, are you using 'with'?")
        return None

    @staticmethod
    def is_not_string(obj) -> TypeGuard[Iterable]:
        """Type checks if object is a string."""
        iter(obj)
        if isinstance(obj, str):
            return False
        return True

    def is_list_of_iter(
        self,
        obj: Sequence,
    ) -> TypeGuard[Sequence[Union[Sequence, Mapping]]]:
        """Type check that obj is a list of tuples or dicts."""
        return all(self.is_not_string(x) for x in obj)

    def script(self, sql_script: str):
        """Execute multiple SQL queries."""
        if self.connection:
            with self.connection as con:
                cur = con.cursor()
                cur.executescript(sql_script)


class TimeblockDB(Database):
    """SQL database tools for Timeblock app."""

    def __enter__(self):
        """Enter context manager, create database if it doesn't exist."""
        super().__enter__()
        if not self.check_for_db():
            self.create_db()
        return self

    def create_db(self):
        """Create SQLite database."""
        script = """
            CREATE TABLE IF NOT EXISTS action(
                id INTEGER PRIMARY KEY,
                desc TEXT NOT NULL UNIQUE,
                est_duration INTEGER,
                actual_duration INTEGER,
                start_datetime REAL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS app_data(
                selected INTEGER,
                FOREIGN KEY(selected) REFERENCES action(id)
            );

        """
        self.script(script)

    def check_for_db(self) -> bool:
        """Check if database exists."""
        query = """
            SELECT name FROM sqlite_master
            WHERE type='table' ORDER BY name
        """
        db_tables = [table for (table,) in self.read_query(query)]
        if set(["action", "app_data"]).issubset(db_tables):
            return True
        return False

    def add_action(self, action: Action) -> Optional[int]:
        """Add action to database."""
        query = """
            INSERT INTO action(desc, est_duration)
            VALUES (?, ?)
        """
        desc = action.desc
        est_duration = action.est_duration
        return self.write_query(query, (desc, est_duration))
