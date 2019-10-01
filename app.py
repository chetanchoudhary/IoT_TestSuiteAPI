import os
import json

from flask_cors import CORS
from flask import Flask, url_for, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager
from resources.sensor import Sensor, SensorByName, UpdateSensorRange, UpdateSensorFrequency, UpdateSensorTimeInterval
from resources.user import UserLogin, UserRegister

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "chetan"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


api.add_resource(Sensor, "/api/v1/sensors")
api.add_resource(SensorByName, "/api/v1/sensors/<string:name>")
api.add_resource(UpdateSensorRange, "/api/v1/sensors/<string:name>/range")
api.add_resource(UpdateSensorFrequency,
                 "/api/v1/sensors/<string:name>/frequency")
api.add_resource(UpdateSensorTimeInterval,
                 "/api/v1/sensors/<string:name>/timeInterval")
api.add_resource(UserRegister, "/api/v1/user")
api.add_resource(UserLogin, "/api/v1/auth")

if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
