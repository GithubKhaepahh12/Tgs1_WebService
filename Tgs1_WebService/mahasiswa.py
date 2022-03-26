# Nama = Rizqi amalia, NIM = 19090031 
# Nama = Khaepah, NIM =19090017 

import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mahasiswa.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Mahasiswa(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<Title: {}>".format(self.title)

@app.route("/", methods=["GET"])
def index():
    mahasiswas = Mahasiswa.query.all()
    return render_template("home.html", mahasiswas=mahasiswas)

@app.route("/mahasiswas/create", methods=["POST"])
def create():
    if request.form:
        mahasiswa = Mahasiswa(title=request.form.get("title"))
        db.session.add(mahasiswa)
        db.session.commit()
    return redirect("/")

@app.route("/mahasiswas/<title>/edit", methods=["GET"])
def edit(title):
    mahasiswa = Mahasiswa.query.filter_by(title=title).first()
    mahasiswas = Mahasiswa.query.all()
    return render_template("edit.html", mahasiswa=mahasiswa, mahasiswas=mahasiswas)

@app.route("/mahasiswas/update", methods=["POST"])
def update():
    newtitle = request.form.get("newtitle")
    oldtitle = request.form.get("oldtitle")
    mahasiswa = Mahasiswa.query.filter_by(title=oldtitle).first()
    mahasiswa.title = newtitle
    db.session.commit()
    return redirect("/")
@app.route("/mahasiswas/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    mahasiswa = Mahasiswa.query.filter_by(title=title).first()
    db.session.delete(mahasiswa)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
   app.run(debug = True)
