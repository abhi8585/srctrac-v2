from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

from app.services.database import DatabaseOperations


# Roles List
# shows a list of all the roles
class PermissionListResource(Resource):

    def get(self):
        conn = db.engine.connect()
        query = conn.execute("select * from  permission")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        if len(result) == 0:
            return {"message" : "No Permission exists!"}, 400
        conn.close()
        return {"permissions": result}, 200



class PermissionResource(Resource):

    def get(self, permission_id=None):
        if permission_id is None:
            return {"message": "No permission id is provided"}, 400
        else:
            conn = db.engine.connect()
            query = conn.execute("SELECT * FROM permission where permission_id = %s" % permission_id)
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            if len(result) == 0:
                return {"message" : "Permission does not exist!"}, 400
            conn.close()
            return {"permission": result[0]}, 200


    def post(self):
        # Parse the request body
        data = request.get_json()
        # Validate the request data
        if not data:
            return {"message": "No input data provided"}, 400
        if not data.get("name"):
            return {"message": "Permission Name is required"}, 400
        if not data.get("description"):
            return {"message": "Permission Description is required"}, 400
        permission_name, permission_description = data.get("name").strip().rstrip().lstrip().lower(), data.get("description")
        # print(permission_name, permission_description)
        # check if the role_name already exists
        permission_query = "SELECT * FROM permission WHERE name = '{0}'".format(permission_name)
        conn = db.engine.connect()
        result = conn.execute(permission_query)
        if result.fetchone():
            return { "message" : "Permission already exists"}, 400
        permission_insert_query = "INSERT INTO permission (name, description) VALUES (%s, %s)"
        result = conn.execute(permission_insert_query, permission_name, permission_description)
        db.session.commit()
        conn.close()
        return {"message" : "permission created", "permission_id" : result.lastrowid}

    
    def delete(self, permission_id):
        conn = db.engine.connect()
        delete_user_query = f"delete from permission where permission_id={permission_id}"
        result = conn.execute(delete_user_query)
        db.session.commit()
        conn.close()
        if result.rowcount == 0:
            return {"message": f"No permission found with ID {permission_id}"}, 404
        return {"message": f"Role with ID {permission_id} has been deleted"}, 200
            

    def put(self, permission_id):
        if permission_id is None:
            return {"message" : "No permission id provided"}, 400
        conn = db.engine.connect()
        data = request.get_json()
        if data is None:
            return  {"message" : "no data is provided"}, 400
        if not data.get("name"):
            return {"message" : "no permission name is provided"}, 400

        # retreive user information to validate that updated information do not exist
        permission_query = "select * from permission where permission_id = '{0}'".format(permission_id)
        permission_result = conn.execute(permission_query)
        # check if user exists 
        if permission_result.rowcount == 0:
            return {"message": f"No permission found with ID {permission_id}"}, 404
        # proceed if the role exist
        permission_info = [dict(zip(tuple(permission_result.keys()), i)) for i in permission_result.cursor][0]
        # check if the role name is same as previous
        update_query_array = []
        if data.get("name"):
            new_permission_name = data.get("name")
            if new_permission_name == permission_info["name"]:
                return {"message" : "Permission name already exists"}
            update_query_array.append("name = '{0}'".format(new_permission_name))
        if data.get("description"):
            new_permission_description = data.get("description")
            update_query_array.append("description = '{0}'".format(new_permission_description))
        final_udpate_query = "update permission set {0} where permission_id = {1}".format(",".join(update_query_array), permission_id)
        conn.execute(final_udpate_query)
        db.session.commit()
        conn.close()
        return {"message" : "Permission with ID {0} Modified successfully".format(permission_id)}, 200


            
        


