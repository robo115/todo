import flask
from flask import Flask, request, redirect, url_for
from models import db, List

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def index():  # put application's code here
    return flask.render_template("index.html")


@app.route("/todolist", methods=["GET", "POST"])
def todolist():
    db.session.query(List).order_by(List.status)
    if request.method == "POST":
        item = request.form["item"]
        task = List(item=item)

        db.session.add(task)
        db.session.commit()
    to_list = db.session.execute(db.select(List)).scalars().all()
    to_list_order = db.session.query(List).order_by(List.status)
    return flask.render_template("list.html", to_list=to_list_order, to_list_all=to_list)


@app.route("/delete", methods=["POST"])
def delete():
    task_id = request.form["id"]

    task = db.get_or_404(List, task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("todolist"))


@app.route("/finished", methods=["POST"])
def finished():
    task_id = request.form["id"]

    task = db.get_or_404(List, task_id)
    task.status = True
    db.session.commit()

    return redirect(url_for("todolist"))


@app.route('/not_done', methods=['POST'])
def not_done():
    task_id = request.form["id"]

    task = db.get_or_404(List, task_id)
    task.status = False
    db.session.commit()

    return redirect(url_for("todolist"))


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    if request.method == "POST":
        task_id = request.form['id']
        task = db.get_or_404(List, task_id)
        return flask.render_template('edit.html', task=task)
    else:
        return flask.render_template('edit.html')


@app.route('/finished_edit', methods=['POST'])
def finished_edit():
    item = request.form['item']
    task_id = request.form['id']

    task = db.get_or_404(List, task_id)
    task.item = item
    db.session.commit()

    return redirect(url_for('todolist'))


if __name__ == "__main__":
    app.run()
