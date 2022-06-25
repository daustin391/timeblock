""" Tests for SQLite3 database
"""
# pylint: disable=redefined-outer-name
import os
from contextlib import redirect_stdout
from io import StringIO
from pytest import main, fixture
from timeblock import sql


@fixture(scope="session")
def db():
    """Creates DB instance for tests"""
    yield sql.Database("test.sql")
    os.remove("test.sql")


@fixture
def tb_db():
    """Creates Timeblock Database sublass instance for tests"""
    yield sql.TimeblockDB("tb_test.sql")
    os.remove("tb_test.sql")


def test_timeblock_db(tb_db):
    """Tests that specific Timeblock DB subclass works"""
    with tb_db:
        assert (
            tb_db.write_query(
                "INSERT INTO action(desc) VALUES ('test')"
            )
            == 1
        )
    # 2nd 'with' tests that 'check_for_db' works when db exists
    with tb_db:
        assert (
            "test" in tb_db.read_query("SELECT * FROM action")[0]
        )


def test_repr(db):
    """Test that __repr__ returns expected string"""
    assert db.__repr__() == 'DB("test.sql")'


def test_not_using_with(db):
    """Test error message when Database object
    is not used as context manager for queries"""
    for query in [
        (db.read_query, "SELECT * FROM customers"),
        (
            db.write_query,
            "INSERT INTO customers VALUES ('Ethan')",
        ),
    ]:
        func, query_str = query
        with redirect_stdout(StringIO()) as msg:
            func(query_str)
        assert (
            "Error: no cursor, are you using 'with'?"
            in msg.getvalue()
        )


def test_write(db):
    """Test write queries"""
    with db:
        assert db.write_query("CREATE TABLE customers(name)") == 0
        assert (
            db.write_query(
                "INSERT INTO customers(name) VALUES ('Bob')"
            )
            == 1
        )
        assert (
            db.write_query(
                "INSERT INTO customers VALUES (?)", ("George",)
            )
            == 2
        )
        assert (
            db.write_query(
                "INSERT INTO customers VALUES (:name)",
                {"name": "Jim"},
            )
            == 3
        )
        assert (
            db.write_query(
                "INSERT INTO customers VALUES (?)",
                [("John",), ("Doug",)],
            )
            == 3
        )
        assert (
            db.write_query(
                "INSERT INTO customers VALUES (:name)",
                [{"name": "Steve"}, {"name": "Joe"}],
            )
            == 3
        )


def test_read(db):
    """Test that DB can be read from"""
    with db:
        assert ("Bob",) in db.read_query(
            "SELECT * FROM customers"
        )


def test_read_params(db):
    """Test read query with paramaters"""
    with db:
        assert [("Bob",)] == db.read_query(
            "SELECT * FROM customers WHERE name = ?", ("Bob",)
        )
        assert [("Bob",)] == db.read_query(
            "SELECT * FROM customers WHERE name = :name",
            {"name": "Bob"},
        )


def test_script(db):
    """Test scripts"""
    with db:
        db.script(
            """
        SELECT * FROM customers;
        INSERT INTO customers VALUES ('Ralph');
        """
        )
        assert ("Ralph",) in db.read_query(
            "SELECT * FROM customers"
        )


def test_error_msg(db):
    """Corrupts DB file to test error messages"""
    with open("test.sql", "w", encoding="utf-8") as db_file:
        db_file.write("testing testing 1 2 3")
    for query in [
        (db.read_query, "SELECT * FROM customers"),
        (
            db.write_query,
            "INSERT INTO customers VALUES ('Ethan')",
        ),
    ]:
        func, query_str = query
        with db, redirect_stdout(StringIO()) as msg:
            func(query_str)
        assert "Error:" in msg.getvalue()


if __name__ == "__main__":  # pragma: no cover
    main()
