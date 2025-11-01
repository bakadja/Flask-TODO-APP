from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB


app = Flask(__name__)
# creating the TinyDB database
db = TinyDB('db.json')
@app.route("/")
def root():
    # TinyDB exposes the ``doc_id`` attribute for each document. We surface it as the
    # ``id`` field expected by the templates without storing a potentially stale value
    # in the database. This keeps identifiers stable across refreshes while relying on
    # TinyDB's internal, thread-safe ID generation.
    todo_list = [{**todo, "id": todo.doc_id} for todo in db.all()]
    return render_template('index.html',todo_list=todo_list)

@app.route("/add",methods=["POST"])
def add():
    #add new item
    title = request.form.get("title")
    db.insert({'title': title, 'complete': False})
    return redirect(url_for("root"))

@app.route("/update",methods=["POST"])
def update():
    #update the todo titel
    newTest = request.form.get('inputField')
    todo_id =  request.form.get('hiddenField')
    db.update({"title": newTest}, doc_ids=[int(todo_id)])
    return redirect(url_for("root"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    #delete the todo
    db.remove(doc_ids=[todo_id])
    return redirect(url_for("root"))

@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    #mark complete
    db.update({"complete": True},doc_ids=[todo_id])
    return redirect(url_for("root"))
    

if __name__ == '__main__':
    app.run(debug=True)