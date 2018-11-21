from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..entities import members as mem
from .. import utilities


class User(Resource):

    @staticmethod
    @jwt_required
    def get():

        current_member_id = get_jwt_identity()

        if current_member_id is None:
            return {
                "status": 404,
                "message": "Unauthorized Access. Cannot perform action"
            }, 404

        try:
            profile = mem.Members.get_member(current_member_id)

            print(profile)

            return {
                "status": 200,
                "member_id": profile.id,
                "email": profile.email,
                "call_sign": profile.call_sign,
                "join_date": str(profile.join_date)
            }, 200

        except Exception as e:
            return {
                "status": 404,
                "message": "an error occurred while retrieving a member's profile"
            }, 404

    @staticmethod
    def post():
        print('Create New User')
        parser = reqparse.RequestParser()
        parser.add_argument('email', help='This field cannot be blank', required=True)
        parser.add_argument('call_sign', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)

        args = parser.parse_args()

        user = mem.Members.get(email=args['email'])

        if user is not None:

            response = {
                "status": 400,
                "message": "User with email {} already exists.".format(user.email)
            }
            return response, 400

        user = mem.Members.save_member(args['email'], args['call_sign'], args['password'])

        token = utilities.TokenCreator(user.id)

        response = {
            "status": 200,
            "message": "New user with email {} created.".format(args['email']),
            "access_token": token.getAccessToken()
        }

        return response, 201

    @staticmethod
    def put(member_id):
       pass

    @staticmethod
    def delete(member_id):
        pass


class UserLogin(Resource):
    @staticmethod
    def post():
        print('Login Attempt')
        parser = reqparse.RequestParser()
        parser.add_argument('email', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)

        data = parser.parse_args();
        email = data['email']
        user = mem.Members.get(email=email)

        if user is not None and \
                email == user.email and sha256.verify(data['password'], user.password):

                token = utilities.TokenCreator(user.id)

                return {
                        "status": 200,
                        "message": 'Login successful.',
                        "access_token": token.getAccessToken(),
                        "refresh_token": token.getRefreshToken(),
                    }, 200

        else:

            return {
                "status": 400,
                "message": "Invalid username or password."
            }
