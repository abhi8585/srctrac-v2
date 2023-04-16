from flask_restful import Resource
from flask import request
from app import db
from app.services.utils import Utils

class UserRoleMappingResource(Resource):

    def post(self):
        utils_client = Utils()
        try:
            data = request.get_json()
            if not data:
                return {"message": "No input data provided"}, 400
            if not data.get("role_id"):
                return {"message": "role_id is required"}, 400
            if not data.get("user_id"):
                return {"message": "user_id is required"}, 400
            role_id, user_id = data.get("role_id").strip().rstrip().lstrip().lower(), data.get("user_id")
            # check if the role_name already exists
            role_query = f"SELECT * FROM UserRole where user_id = {user_id}"
            conn = db.engine.connect()
            result = conn.execute(role_query)
            if result.fetchone():
                return dict(status="failed", message=f"{user_id} mapped already"), 200
            role_insert_query = f"INSERT INTO UserRole (user_id, role_id) VALUES ({user_id}, {role_id})"
            result = conn.execute(role_insert_query)
            db.session.commit()
            utils_client.log_data(f"user {user_id} mapped to role {role_id}")
            conn.close()
            return dict(status="success",message=f"{user_id} mapped successfully"), 200
        except Exception as e:
            utils_client.log_data(f"error while mapping user to role")
            return dict(status="failed",message=f"error while mapping user to role"), 405