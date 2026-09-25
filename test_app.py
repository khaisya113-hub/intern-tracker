import os
import sqlite3
import pytest
import database

# Use a separate test database so real tasks.db stays untouched
TEST_DB = "test_tasks.db"


@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """Before each test: point database.py at a fresh test DB."""
    monkeypatch.setattr(database, "DB_NAME", TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    database.init_db()
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_and_get_task():
    database.add_task("Test task", "Test description")
    tasks = database.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0][1] == "Test task"
    assert tasks[0][3] == "pending"


def test_update_status():
    database.add_task("Task A", "desc")
    task_id = database.get_all_tasks()[0][0]
    database.update_task_status(task_id, "done")
    assert database.get_task(task_id)[3] == "done"


def test_delete_task():
    database.add_task("Task to delete", "desc")
    task_id = database.get_all_tasks()[0][0]
    database.delete_task(task_id)
    assert len(database.get_all_tasks()) == 0


def test_empty_description_allowed():
    database.add_task("Title only", None)
    tasks = database.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0][2] is None


def test_multiple_tasks_ordered_newest_first():
    database.add_task("First", "")
    database.add_task("Second", "")
    database.add_task("Third", "")
    titles = [t[1] for t in database.get_all_tasks()]
    assert titles == ["Third", "Second", "First"]