import os
import json

from flask import Flask, url_for, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity, timedelta

from resources.sensor import Sensor, SensorByName

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "chetan"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


# jwt = JWT(app, authenticate, identity_function)
# app.config["JWT_EXPIRATION_DELTA"] = timedelta(
#     seconds=1800
# )  # increasing Token Expiration period


# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#     print(
#         jsonify({"access_token": access_token.decode(
#             "utf-8"), "user_id": identity.id})
#     )
#     return jsonify(
#         {"access_token": access_token.decode("utf-8"), "user_id": identity.id}
#     )


api.add_resource(Sensor, "/api/v1/sensors")
api.add_resource(SensorByName, "/api/v1/sensors/<string:name>")


if __name__ == "__main__":
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
