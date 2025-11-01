import pathlib
import sys

import pytest


ROOT_DIR = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

pytest.importorskip("flask")

from app import create_app, get_db


@pytest.fixture
def app(tmp_path):
    db_path = tmp_path / "test_db.json"

    app = create_app(
        {
            "TESTING": True,
            "TODO_DB_PATH": str(db_path),
            "SECRET_KEY": "test",
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def _read_all_tasks(app):
    with app.app_context():
        db = get_db()
        tasks = []
        for task in db.all():
            task_dict = dict(task)
            task_dict["doc_id"] = task.doc_id
            tasks.append(task_dict)
        return tasks


def test_index_loads_successfully(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"To Do List" in response.data


def test_add_task(client, app):
    response = client.post("/add", data={"title": "Test Task"}, follow_redirects=True)

    assert response.status_code == 200
    tasks = _read_all_tasks(app)
    assert any(task["title"] == "Test Task" for task in tasks)


def test_delete_task(client, app):
    with app.app_context():
        db = get_db()
        task_id = db.insert({"title": "Task to delete", "complete": False})

    response = client.post(f"/delete/{task_id}", follow_redirects=True)

    assert response.status_code == 200
    tasks = _read_all_tasks(app)
    assert not any(task["doc_id"] == task_id for task in tasks)
