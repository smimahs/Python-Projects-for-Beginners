from flask import Flask, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    detail = db.Column(db.Text)
    complete = db.Column(db.Boolean)


@app.route('/')
def home():
    todo_list = Todo.query.all()
    todo = []
    for t in todo_list:
        todo.append({"id":t.id,"title":t.title,"detail":t.detail,"complete":t.complete})
    return jsonify(todo)

@app.route("/add", methods=["POST"])
def add():
    try:
        title = request.form.get("title")
        detail = request.form.get("detail")
        new_todo = Todo(title=title,detail=detail, complete=False)
        db.session.add(new_todo)
        db.session.commit()
    except:
        pass
    return redirect("/")

@app.route("/update/<int:todo_id>")
def update(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        todo.complete = not todo.complete
        db.session.commit()
    except:
        pass
    return redirect("/")

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    try:
        todo = Todo.query.filter_by(id=todo_id).first()
        db.session.delete(todo)
        db.session.commit()
    except:
        pass
    return redirect("/")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)