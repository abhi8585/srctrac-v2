from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app import db
from app.services.utils import Utils


def get_user_role(conn,user_id, util_client):
        util_client.log_data(f"get user_id : {user_id} to get role ")
        role_name = None
        user_role_query = f"SELECT * FROM UserRole where user_id = {user_id}" 
        user_role_result = conn.execute(user_role_query)
        user_role_result = [dict(zip(tuple(user_role_result.keys()), i)) for i in user_role_result.cursor]
        util_client.log_data(f"get role data {user_role_result} for user : {user_id}")
        if len(user_role_result) > 0:
            role_info = user_role_result[0]
            util_client.log_data(f"get role id {role_info['role_id']} for user : {user_id}")
            role_name_query = f"SELECT * FROM Role where role_id = {role_info['role_id']}" 
            role_result = conn.execute(role_name_query)
            role_result = [dict(zip(tuple(role_result.keys()), i)) for i in role_result.cursor]
            if len(role_result) > 0:
                role_name = role_result[0]['name']
                return role_name
        return role_name


class LoginResource(Resource):

    def get(self):
        util_client = Utils()
        try:
            util_client.log_data(f"login request")
            is_psw_correct = False
            util_client = Utils()
            if not request.args.get('username'):
                return {"message": "User Name is required"}, 400
            if not request.args.get('password'):
                return {"message": "User Password is required"}, 400
            user_name, user_psw = request.args.get('username'), request.args.get('password')
            util_client.log_data(f"login request for user {user_name}")
            user_query = f"select * from User where username = '{user_name}'"
            conn = db.engine.connect()
            user_result = conn.execute(user_query)
            user_result = [dict(zip(tuple(user_result.keys()), i)) for i in user_result.cursor]
            if len(user_result) > 0:
                util_client.log_data(f"successfully fetched user")
                user_result = user_result[0]
                is_psw_correct = check_password_hash(user_result['password'], user_psw)
                if is_psw_correct:
                    util_client.log_data(f"user authenticated successfully")
                    user_role = get_user_role(conn, user_result['user_id'], util_client)
                    if user_role is None:
                        user_role = ""
                    return dict(status="success", user_id=user_result['user_id'],user_email=user_result['email'],
                                user_name=user_result['username'], user_token=create_access_token(user_result['user_id']),
                                user_role=user_role), 200
                else:
                    util_client.log_data(f"user authentication failed")
                    return dict(status="success", user_id=str(),user_email=str()), 200
            else:
                return dict(status="failed", message="no user exist", user_id=str(),user_email=str()), 200
        except Exception as e:
            util_client.log_data(e)
            return dict(status="success", user_id=str(),user_email=str()), 405

    # def post(self):
    #     try:
    #         is_psw_correct = False
    #         # Parse the request body
    #         data = request.get_json()
    #         # Validate the request data
    #         if not data:
    #             return {"message": "No input data provided"}, 400
    #         if not data.get("user_name"):
    #             return {"message": "User Name is required"}, 400
    #         if not data.get("user_psw"):
    #             return {"message": "User password is required"}, 400
    #         user_name, user_psw = data.get("user_name"), data.get("user_psw")
    #         user_query = f"select * from User where username = '{user_name}'"
    #         conn = db.engine.connect()
    #         user_result = conn.execute(user_query)
    #         user_result = [dict(zip(tuple(user_result.keys()), i)) for i in user_result.cursor]
    #         if len(user_result) > 0:
    #             user_result = user_result[0]
    #             is_psw_correct = check_password_hash(user_result['password'], user_psw)
    #         else:
    #             return dict(status="success", user_id=str(),user_email=str()), 200
    #         if is_psw_correct:
    #             if 'admin' in user_name:
    #                 user_role = 'admin'
    #             if 'ware' in user_name:
    #                 user_role = 'warehouse'
    #             return dict(status="success", user_id=user_result['user_id'],user_email=user_result['email'],
    #                     user_token=create_access_token(user_result['user_id']),user_role='admin'), 200
    #         else:
    #             return dict(status="failed", user_id=str(),user_email=str()), 401
    #     except Exception as e:
    #         print(e)
    #         return dict(status="success", user_id=str(),user_email=str()), 405