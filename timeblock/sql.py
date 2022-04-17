""" SQL
    Provide tools for dealing with SQLite3 database.

"""

import sqlite3
from sqlite3 import Error
from typing import Union
import os.path


class DB:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = sqlite3.connect("db.sql")
            self.cursor = self.connection.cursor()
        except Error as e:
            print(f"The error {e} occured.")
        return self

    def __exit__(self, *args, **kwargs):
        self.connection.close()

    def read_query(
        self, query: str, parameters: Union[tuple, dict] = None
    ) -> Union[list[tuple], None]:
        result = None
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
        except Error as e:
            print(f"The error {e} occured.")
        return result

    def write_query(
        self,
        query: str,
        parameters: Union[list[tuple], tuple, list[dict], dict, None] = None,
    ) -> int:
        try:
            if not parameters:
                self.cursor.execute(query)
            elif isinstance(parameters, list):
                self.cursor.executemany(query, parameters)
                return 0
            else:
                self.cursor.execute(query, parameters)
            return self.cursor.lastrowid
        except Error as e:
            print(f"The error {e} occured.")

    def script(self, sql_script: str):
        with self.connection as con:
            cur = con.cursor()
            cur.executescript(sql_script)


class TimeblockDB(DB):
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
