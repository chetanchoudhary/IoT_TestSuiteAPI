from flask_restful import reqparse, Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import UserModel


class UserRegister(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('email', type=str, required=True,
                             help="Please provide correct Email Address.")
    user_parser.add_argument(
        'password', type=str, required=True, help="Please provide correct Password.")
    user_parser.add_argument('email', type=str, required=True,
                             help="Please provide correct Email Address.")
    user_parser.add_argument(
        'access', type=str, required=True, help="By Default normal.")
    user_parser.add_argument('email', type=str, required=True,
                             help="Please provide correct Email Address.")
    user_parser.add_argument(
        'firstName', type=str, required=True, help="Please provide your First Name.")
    user_parser.add_argument(
        'lastName', type=str, required=True, help="Please provide your Last Name.")
    user_parser.add_argument(
        'contactNumber', type=str, required=True, help="Please provide your Mobile Number.")

    def post(self):
        data = self.user_parser.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "A user with this E-mail already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created Successfully."}, 201


class UserLogin(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument('email', type=str, required=True,
                             help="Please provide correct Email Address.")
    user_parser.add_argument(
        'password', type=str, required=True, help="Please provide correct Password.")

    def post(self):
        data = self.user_parser.parse_args()
        user = UserModel.find_by_email(data["email"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "message": "Sign-in successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        return {"message": "Invalid Credentials"}, 401
