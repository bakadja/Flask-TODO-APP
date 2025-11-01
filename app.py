from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query


app = Flask(__name__)
# creating the TinyDB database
db = TinyDB('db.json')


def get_next_id() -> int:
    """Return an integer identifier that is unique within the todo table."""
    todos = db.all()
    if not todos:
        return 1

    # TinyDB stores rows as dictionaries, so we defensively ignore rows missing the
    # "id" key or values that are not integers.
    used_ids = [todo.get("id") for todo in todos if isinstance(todo.get("id"), int)]
    if not used_ids:
        return 1

    return max(used_ids) + 1


@app.route("/")
def root():
    todo_list = db.all()
    return render_template('index.html',todo_list=todo_list)

@app.route("/add",methods=["POST"])
def add():
    #add new item
    title = request.form.get("title")
    db.insert({'id': get_next_id(), 'title': title, 'complete': False})
    return redirect(url_for("root"))

@app.route("/update",methods=["POST"])
def update():
    #update the todo titel
    todo_db = Query()
    newTest = request.form.get('inputField')
    todo_id =  request.form.get('hiddenField')
    db.update({"title": newTest},todo_db.id == int(todo_id))
    return redirect(url_for("root"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #delete the todo 
    todo_db = Query()
    db.remove(todo_db.id == todo_id)
    return redirect(url_for("root"))

@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    #mark complete
    todo_db = Query()
    db.update({"complete": True},todo_db.id == todo_id)
    return redirect(url_for("root"))
    

if __name__ == '__main__':
    app.run(debug=True)