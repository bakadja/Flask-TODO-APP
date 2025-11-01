import os
from typing import Any, Dict

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    g,
    current_app,
)
from tinydb import TinyDB


def create_app(test_config: Dict[str, Any] | None = None) -> Flask:
    """Application factory for the TODO app."""

    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        TODO_DB_PATH=os.environ.get(
            "TODO_DB_PATH", os.path.join(app.root_path, "db.json")
        ),
    )

    if test_config is not None:
        app.config.update(test_config)

    @app.teardown_appcontext
    def close_db(_: BaseException | None) -> None:
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def index() -> str:
        todo_list = [
            {**todo, "id": todo.doc_id}
            for todo in get_db().all()
        ]
        return render_template("index.html", todo_list=todo_list)

    @app.route("/add", methods=["POST"])
    def add_todo() -> Any:
        title = (request.form.get("title", "") or "").strip()
        if not title:
            flash("Please provide a title for the to-do item.", "error")
            return redirect(url_for("index"))

        get_db().insert({"title": title, "complete": False})
        flash("Added a new to-do item.", "success")
        return redirect(url_for("index"))

    @app.route("/update", methods=["POST"])
    def update_todo() -> Any:
        raw_id = request.form.get("todo_id", "")
        new_title = (request.form.get("title", "") or "").strip()

        todo_id = _parse_doc_id(raw_id)
        if todo_id is None:
            flash("Invalid to-do identifier.", "error")
            return redirect(url_for("index"))

        if not new_title:
            flash("Please provide a title for the to-do item.", "error")
            return redirect(url_for("index"))

        db = get_db()
        if db.contains(doc_id=todo_id):
            db.update({"title": new_title}, doc_ids=[todo_id])
            flash("Updated the to-do item.", "success")
        else:
            flash("Unable to find the requested to-do item.", "error")
        return redirect(url_for("index"))

    @app.route("/delete/<int:todo_id>", methods=["POST"])
    def delete_todo(todo_id: int) -> Any:
        db = get_db()
        if db.contains(doc_id=todo_id):
            db.remove(doc_ids=[todo_id])
            flash("Deleted the to-do item.", "success")
        else:
            flash("Unable to find the requested to-do item.", "error")
        return redirect(url_for("index"))

    @app.route("/complete/<int:todo_id>", methods=["POST"])
    def complete_todo(todo_id: int) -> Any:
        db = get_db()
        if db.contains(doc_id=todo_id):
            db.update({"complete": True}, doc_ids=[todo_id])
            flash("Marked the to-do item as complete.", "success")
        else:
            flash("Unable to find the requested to-do item.", "error")
        return redirect(url_for("index"))

    return app


def _parse_doc_id(raw_id: str | None) -> int | None:
    try:
        return int(raw_id)
    except (TypeError, ValueError):
        return None


def get_db() -> TinyDB:
    if "db" not in g:
        g.db = TinyDB(current_app.config["TODO_DB_PATH"])
    return g.db


def main() -> None:
    app = create_app()
    debug_flag = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(debug=debug_flag)


if __name__ == "__main__":
    main()
