#http://127.0.0.1:7001/
#Nama:Rizqi Amalia, Nim:19090031
#Nama:Khaepah,Nim:19090017

from flask import Flask
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "19090031",
    "secret-token-2": "19090017"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/')
@auth.login_required
def index():
    return "Anda login dengan nim, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run(debug = True, port=7001)
