#http://127.0.0.1:7002/
#Nama:Rizqi Amalia, Nim:19090031
#Nama:Khaepah,Nim:19090017

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "19090031": generate_password_hash("123"),
    "19090017": generate_password_hash("123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return "Anda login sebagai, {}".format(auth.current_user())

if __name__ == '__main__':
    app.run(debug = True, port=7002)
