from components import Components

comps = Components()

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"

# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE
class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thing = db.Column(db.String(250), unique=True, nullable=False)
    date = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

db.create_all()

@app.route("/", methods=['GET', 'POST'])
def load():
    db.session.query(Thing).filter(Thing.date != comps.date).delete()
    db.session.commit()

    all_things = Thing.query.order_by(Thing.id).all()

    return render_template("index.html", date=comps.date, things=all_things)


@app.route("/insert", methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        thing = str(request.form.get("thing"))
        to_do = Thing(thing=thing, date=comps.date, completed=False)

        try:
            db.session.add(to_do)
            db.session.commit()

        except:
            return redirect(url_for("load"))

        return redirect(url_for("load"))

@app.route("/update/<int:thing_id>")
def update(thing_id):
    try:
        thing = Thing.query.get(thing_id)

        if thing.completed is False:
            thing.completed = True
            db.session.commit()

        else:
            thing.completed = False
            db.session.commit()

        return redirect(url_for("load"))

    except:
        return redirect(url_for("load"))

@app.route("/delete/<int:thing_id>")
def delete(thing_id):
    try:
        to_delete = Thing.query.get(thing_id)

        db.session.delete(to_delete)
        db.session.commit()

    except:
        return redirect(url_for("load"))

    return redirect(url_for("load"))

if __name__ == "__main__":
    app.run(debug=True)