"""
Module for testing SQLite database functionality.

The following fixtures are imported from conftest.py:
    - tb_db: An empty TimeblockDB instance.
    - database: Creates a Database instance for testing.

This module contains the following tests:
    - test_timeblock_db: Check that TimeblockDB instance creates tables,
        reads and writes data.
    - test_repr: Test that __repr__ returns expected string.
    - test_not_using_with: Test error message when Database object
        is not used as context manager for queries.
    - test_write: Test write queries.
    - test_read: Test that DB can be read from.
    - test_read_params: Test read query with paramaters.
    - test_script: Test scripts.
    - test_error_msg: Corrupts DB file to test error messages.
    - test_add_action: Test add_action method.
"""


from contextlib import redirect_stdout
from io import StringIO

from constants import TEST_DB_PATH
from timeblock import sql
from timeblock.action import Action


def test_timeblock_db(tb_db: sql.TimeblockDB) -> None:
    """
    Check that TimeblockDB instance creates tables, reads and writes data.

    This test creates a TimeblockDB instance and checks the write_query
    and read_query methods.

    Each 'with' statement creates a new connection to the database and closes
    it after the block is complete. This checks that the class works when the
    SQLite file exists and data persists after the connection is closed.
    """
    with tb_db:
        assert (
            tb_db.write_query("INSERT INTO action(desc) VALUES ('test')") == 1
        )

    with tb_db:
        assert "test" in tb_db.read_query("SELECT * FROM action")[0]


def test_repr(database):
    """
    Test that __repr__ returns expected string representation of Database.

    Args:
        database (sql.Database): Database instance.
    """
    with database:
        assert repr(database) == f'DB("{TEST_DB_PATH}")'


def test_not_using_with() -> None:
    """
    Check for error message when instance isn't used as a context manager.

    Args:
        database (sql.Database): Database instance.
    """
    with_test_db = sql.Database(TEST_DB_PATH)
    for query in [
        (with_test_db.read_query, "SELECT * FROM customers"),
        (
            with_test_db.write_query,
            "INSERT INTO customers VALUES ('Ethan')",
        ),
    ]:
        func, query_str = query
        with redirect_stdout(StringIO()) as msg:
            func(query_str)
        assert "Error: no cursor, are you using 'with'?" in msg.getvalue()


def test_write(database):
    """
    Test that write_query method can insert data into database.

    This test creates a table, inserts data into it, and checks that the data
    was inserted correctly.

    Args:
        database (sql.Database): Database instance.
    """
    with database:
        assert database.write_query("CREATE TABLE customers(name)") == 0
        assert (
            "customers"
            in database.read_query(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )[0]
        )
        assert (
            database.write_query("INSERT INTO customers(name) VALUES ('Bob')")
            == 1
        )
        assert (
            database.write_query(
                "INSERT INTO customers VALUES (?)", ("George",)
            )
            == 2
        )
        assert (
            database.write_query(
                "INSERT INTO customers VALUES (:name)",
                {"name": "Jim"},
            )
            == 3
        )
        assert (
            database.write_query(
                "INSERT INTO customers VALUES (?)",
                [("John",), ("Doug",)],
            )
            == 3
        )
        assert (
            database.write_query(
                "INSERT INTO customers VALUES (:name)",
                [{"name": "Steve"}, {"name": "Joe"}],
            )
            == 3
        )
        assert database.read_query("SELECT * FROM customers") == [
            ("Bob",),
            ("George",),
            ("Jim",),
            ("John",),
            ("Doug",),
            ("Steve",),
            ("Joe",),
        ]


def test_read(database):
    """Test that DB can be read from."""
    with database:
        database.cursor.execute("CREATE TABLE customers(name)")
        database.cursor.execute("INSERT INTO customers VALUES ('Bob')")
        assert ("Bob",) in database.read_query("SELECT * FROM customers")
        assert [("Bob",)] == database.read_query(
            "SELECT * FROM customers WHERE name = ?", ("Bob",)
        )
        assert [("Bob",)] == database.read_query(
            "SELECT * FROM customers WHERE name = :name",
            {"name": "Bob"},
        )


def test_script(database):
    """
    Verify that script method can execute multiple queries.

    Args:
        database (sql.Database): Database instance.
    """
    with database:
        database.script(
            """
            CREATE TABLE customers(name);
            INSERT INTO customers VALUES ('Ralph');
            """
        )
        assert ("Ralph",) in database.cursor.execute("SELECT * FROM customers")


def test_error_msg(database):
    """
    Test that an error message is returned if the database is unreadable.

    The database file is corrupted by writing to it, then the read and write
    queries are tested to see if they return an error message.

    Args:
        database (sql.Database): Database instance.
    """
    with open(TEST_DB_PATH, "w", encoding="utf-8") as db_file:
        print("testing testing 1 2 3", file=db_file)
        db_file.write("testing testing 1 2 3")
    for query in [
        (database.read_query, "SELECT * FROM customers"),
        (
            database.write_query,
            "INSERT INTO customers VALUES ('Ethan')",
        ),
    ]:
        func, query_str = query
        with database, redirect_stdout(StringIO()) as msg:
            print("testing testing 1 2 3", file=msg)
            func(query_str)
        assert "Error:" in msg.getvalue()


def test_add_action(tb_db: sql.TimeblockDB) -> None:
    """
    Verify that add_action method inserts data into action table.

    Args:
        tb_db (sql.TimeblockDB): TimeblockDB instance.
    """
    with tb_db:
        action = Action("test")
        tb_db.add_action(action)
        assert "test" in tb_db.read_query("SELECT * FROM action")[0]
