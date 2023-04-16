from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app import db

class LoginResource(Resource):

    def post(self):
        try:
            is_psw_correct = False
            # Parse the request body
            data = request.get_json()
            # Validate the request data
            if not data:
                return {"message": "No input data provided"}, 400
            if not data.get("user_name"):
                return {"message": "User Name is required"}, 400
            if not data.get("user_psw"):
                return {"message": "User password is required"}, 400
            user_name, user_psw = data.get("user_name"), data.get("user_psw")
            user_query = f"select * from User where username = '{user_name}'"
            conn = db.engine.connect()
            user_result = conn.execute(user_query)
            user_result = [dict(zip(tuple(user_result.keys()), i)) for i in user_result.cursor]
            if len(user_result) > 0:
                is_psw_correct = check_password_hash(user_result['password'], user_psw)
            else:
                return dict(status="success", user_id=str(),user_email=str()), 200
            if is_psw_correct:
                if 'admin' in user_name:
                    user_role = "admin"
                if "ware" in user_name:
                    user_role = "warehouse"
                return dict(status="success", user_id=user_result['user_id'],user_email=user_result['email'],
                        user_token=create_access_token(user_result['user_id']),user_role=user_role), 200
            else:
                return dict(status="failed", user_id=str(),user_email=str()), 401
        except Exception as e:
            print(e)
            return dict(status="success", user_id=str(),user_email=str()), 405