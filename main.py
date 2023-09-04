from typing import Dict, Any

from flask import Flask, redirect, url_for, render_template, request
from pony import orm
from pony.orm import db_session

app = Flask(__name__)
db = orm.Database()


class Trip(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    item = orm.Required(str, unique=True)
    amount = orm.Required(int)
    description = orm.Optional(str, 50)
    packed = orm.Optional(bool)


db.bind(provider='sqlite', filename="listPA.sqlite.sqlite", create_db=True)
db.generate_mapping(create_tables=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        it = request.form.get('item')
        am = request.form.get('amount')
        de = request.form.get('description')
        db_add(it, am, de)
        return redirect(url_for('create'))
    else:
        return render_template("list.html")


@app.route("/view", methods=["GET", "POST"])
def view():
    with orm.db_session:
        try:
            pack_list = Trip.select()
            return render_template("view.html", data=pack_list)
        except Exception as e:
            response = {"response": "failure", "error": str(e)}
            return response


@app.route('/edit/<int:item_id>', methods=["GET", "POST"])
def edit(item_id):
    with orm.db_session:
        item = Trip.get(id=item_id)
        if request.method == "POST":
            item.item = request.form['item']
            item.amount = request.form['amount']
            item.description = request.form['description']
            item.packed = request.form['packed']
            try:
                db.commit()
                return redirect("/view")
            except Exception as e:
                response = {"response": "failure", "error": str(e)}
                return response
        else:
            return render_template("edit.html", item=item)


@app.route('/delete/<int:item_id>')
def delete(item_id):
    with orm.db_session:
        try:
            list = Trip.get(id=item_id)
            Trip.delete(list)
            db.commit()
            return redirect(url_for('view'))
        except Exception as e:
            response = {"response": "failure", "error": str(e)}
            return response


@db_session
def db_add(item, amount, description=None, packed=False):
    try:
        Trip(item=item, amount=amount, description=description, packed=packed)
        response = {"response":"success"}
        return response
    except Exception as e:
        return {"response":"failure","error":str(e)}


if __name__ == "__main__":
    app.run(debug=True, port=8000)
