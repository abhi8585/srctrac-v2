from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from app.models.user import User

class SkuResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')

    # def post(self):
    #     data = UserResource.parser.parse_args()

    #     user = User.query.filter_by(username=data['username']).first()
    #     if not user or not user.check_password(data['password']):
    #         return {'message': 'Invalid username or password'}, 401

    #     access_token = create_access_token(identity=user.id)
    #     return {'access_token': access_token}, 200

    # @jwt_required()
    def get(self):
        # user_id = get_jwt_identity()
        # user = User.query.get(user_id)

        return {'username': 'This is from the sku part'}, 200
