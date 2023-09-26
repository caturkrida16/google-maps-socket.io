# TASK BERFORE RUN THIS PROGRAM
"""
1. 
"""



### >>><<< ###
# Packages
## System
import os
import json
from datetime import datetime, timedelta

## PIP
from flask import Flask, jsonify, request, render_template, abort
from flask_socketio import SocketIO, emit, disconnect
import jwt
import pytz



### >>><<< ###
# Initialization
## Environment Variable

## Core
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins='*')
gmaps_key = ""
user = {
  "username": "admin",
  "password": "admin1234"
}



### >>><<< ###
# Core
## REST API
### Index
@app.route("/", methods=["GET"])
def index():
    socketio_host = "http://localhost:8080"
    imei_gps = ["ID001", "ID002"]
    access_token = ""
    return render_template("index.html", imei_gps=imei_gps, access_token=access_token, socketio_host=socketio_host, api_key=gmaps_key)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
   
    if (username == user["username"]):
        if (password == user["password"]):
            encoded = encode_jwt(user["username"])
            return jsonify(encoded)
        else:
            return abort(401)
    else:
        return abort(401)

@app.route("/verify_token", methods=["POST"])
def verify_token():
    decoded = verify_jwt(request.headers["accessToken"])
    
    if (decoded == 401):
        return abort(401)
    else:
        return jsonify(decoded)

## SocketIO
### Connect
@socketio.on("connect")
def connect():
    decoded = verify_jwt(request.headers["accessToken"])
    print(decoded)
    
    if (decoded == 401):
        disconnect()

### GPS Device
@socketio.on("gps_device")
def gps(data):
    emit("gps_website", data, broadcast=True)
    
## Function
### Encode JWT
def encode_jwt(username):
    data = {
        "aud": "localhost",
        "iss": "http://localhost:8080/login",
        "iat": datetime.now(pytz.timezone("Asia/Makassar")),
        "exp": datetime.now(pytz.timezone("Asia/Makassar")) + timedelta(hours=1),
        "username": username
    }
    encoded = jwt.encode(data, app.config["SECRET_KEY"], algorithm="HS256")
    return encoded

### Verify JWT
def verify_jwt(data):
    try:
        decoded = jwt.decode(data, app.config["SECRET_KEY"], audience="localhost", issuer="http://localhost:8080/login", algorithms="HS256")
        return decoded
    except jwt.ExpiredSignatureError:
        return 401  
    except jwt.InvalidAudienceError:
        return 401 
    except jwt.InvalidIssuerError:
        return 401
    except:
        return 401



### >>><<< ###
# APP Run
if (__name__ == "__main__"):
    socketio.run(app, host="0.0.0.0", port=8080, debug=True)
