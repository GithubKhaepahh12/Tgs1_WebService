import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import jsonify
import json 
import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "mahasiswa.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Mahasiswa(db.Model):

    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    def toJson(self):
        return {"title": self.title}

    def __repr__(self):
        return json.dumps(self.__dict__)

@app.after_request
def add_header(response):
    response.headers['X-Expires-At'] = datetime.datetime.now() + datetime.timedelta(days=1, hours=3)
    response.headers['X-Api-Name'] = 'W/S mahasiswa'
    return response

#http://127.0.0.1:4000/mahasiswas 
# Nama = Rizqi amalia, NIM = 19090031 
# Nama = Khaepah, NIM =19090017 
@app.route("/mahasiswas", methods=["GET"])
def index():
    mahasiswas = Mahasiswa.query.all()
    array_mahasiswas = []
    for mahasiswa in mahasiswas:
        dict_mahasiswas = {}
        dict_mahasiswas.update({"title": mahasiswa.title})
        array_mahasiswas.append(dict_mahasiswas)
    return jsonify(array_mahasiswas), 200, {'content-type':'application/json'}        

# http://127.0.0.1:4000/mahasiswas/create
# Nama = Rizqi amalia, NIM = 19090031 
# Nama = Khaepah, NIM =19090017 
@app.route("/mahasiswas/create", methods=["POST"])
def create():
    req = request.json
    mahasiswa = Mahasiswa(title=req['title'])
    db.session.add(mahasiswa)
    db.session.commit()
    return jsonify(mahasiswa.toJson()), 201, {'content-type':'application/json'}        

#http://127.0.0.1:4000/mahasiswas/Mahasiswa-A
@app.route("/mahasiswas/<title>", methods=["GET"])
def show(title):
    mahasiswa = Mahasiswa.query.filter_by(title=title).first()
    if(mahasiswa==None):
        return {"msg": "Mahasiswa cant be found"}, 404
    else:
        return jsonify(mahasiswa.toJson()), 200, {'content-type':'application/json'}

# http://127.0.0.1:4000/mahasiswas/update  
# Nama = Rizqi amalia, NIM = 19090031 
# Nama = Khaepah, NIM =19090017  
# HTTP/1.0 400 BAD REQUEST
# Content-Type: application/json
# Content-Length: 37
# X-Expires-At: 2022-03-11 03:41:51.433542
# X-Api-Name: W/S mahasiswa
# Server: Werkzeug/0.16.1 Python/3.8.10
# Date: Wed, 09 Mar 2022 17:41:51 GMT

# {
#   "msg": "Error parsing request"
# }
# http://127.0.0.1:4000/mahasiswas/update 
# Nama = Rizqi amalia, NIM = 19090031 
# Nama = Khaepah, NIM =19090017 
@app.route("/mahasiswas/update", methods=["POST"])
def update():
    try:
        req = request.json
        mahasiswa = Mahasiswa.query.filter_by(title=req['oldtitle']).first()
        if(mahasiswa==None):
            return {"msg": "Mahasiswa cant be found"}, 404
        else:
            mahasiswa.title = req['newtitle']
            db.session.commit()
            if(mahasiswa.title!= req['oldtitle']):
                return {"msg": "Mahasiswa updated"}, 200
            else:
                return {"msg": "Mahasiswa failed to update"}, 400
    except:
        return {"msg": "Error parsing request"}, 400

@app.route("/mahasiswas/delete", methods=["DELETE"])
def delete():
    title = request.json['title']
    mahasiswa = Mahasiswa.query.filter_by(title=title).first()
    if(mahasiswa==None):
        return {"msg": "Mahasiswa cant be found"}, 404
    else: 
        db.session.delete(mahasiswa)
        db.session.commit()
        mahasiswa = Mahasiswa.query.filter_by(title=title).first()
        if(mahasiswa==None):
            return {"msg": "Succesfully deleted"}, 400
        else:
            return {"msg": "Failed to delete"}, 404

if __name__ == '__main__':
   app.run(debug = True, port=4000)
