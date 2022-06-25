""" SQL
    Provide tools for dealing with SQLite3 database.

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
from datetime import datetime, date
from typing_extensions import TypeGuard


DB = TypeVar("DB", bound="Database")
SqlType = Union[None, int, float, str, bytes, date, datetime]
SqlSeq = Union[tuple[SqlType, ...], dict[str, SqlType]]


class Database:
    """Interface for SQLite3 database"""

    def __init__(self, filename: str = None):
        self.connection: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None
        self.filename = filename if filename else "db.sql"

    def __enter__(self: DB):
        self.connection = sqlite3.connect(self.filename)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, *args, **kwargs) -> None:
        if self.connection:
            self.connection.close()

    def __repr__(self):
        return f'DB("{self.filename}")'

    def read_query(
        self, query: str, parameters: Union[tuple, dict] = None
    ) -> list[tuple]:
        """Send query for data from database"""
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
        Writes to database.

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
                elif isinstance(
                    parameters, Sequence
                ) and self.is_list_of_iter(parameters):
                    self.cursor.executemany(query, parameters)
                elif self.is_not_string(parameters):
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
        """Type checks if object is a string"""
        iter(obj)
        if isinstance(obj, str):
            return False
        return True

    def is_list_of_iter(
        self,
        obj: Sequence,
    ) -> TypeGuard[Sequence[Union[Sequence, Mapping]]]:
        """Type checks that parameter
        is a list of sequences (tuples) or mappings (dicts)"""
        return all(self.is_not_string(x) for x in obj)

    def script(self, sql_script: str):
        """Executes multiple SQL queries"""
        if self.connection:
            with self.connection as con:
                cur = con.cursor()
                cur.executescript(sql_script)


class TimeblockDB(Database):
    """SQL database tools for Timeblock app"""

    def __enter__(self):
        super().__enter__()
        if not self.check_for_db():
            self.create_db()
        return self

    def create_db(self):
        """Create SQLite database"""
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
        """Check if database exists"""
        query = """
            SELECT name FROM sqlite_master
            WHERE type='table' ORDER BY name
        """
        db_tables = [table for (table,) in self.read_query(query)]
        if set(["action", "app_data"]).issubset(db_tables):
            return True
        return False
