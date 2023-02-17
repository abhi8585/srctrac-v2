from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# Roles List
# shows a list of all the roles
class RolesListResource(Resource):
    def get(self):
        conn = db.engine.connect()
        query = conn.execute("SELECT * FROM Role")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        if len(result) == 0:
            return {"message" : "No Role exists!"}, 400
        conn.close()
        return {"roles": result}, 200



class RoleResource(Resource):

    def get(self, role_id=None):
        if role_id is None:
            return {"message": "No role id provided"}, 400
        else:
            conn = db.engine.connect()
            query = conn.execute("SELECT * FROM Role where role_id = %s" % role_id)
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            if len(result) == 0:
                return {"message" : "Role does not exist!"}, 400
            conn.close()
            return {"user": result[0]}, 200


    def post(self):
        # Parse the request body
        data = request.get_json()
        # Validate the request data
        if not data:
            return {"message": "No input data provided"}, 400
        if not data.get("name"):
            return {"message": "Rolename is required"}, 400
        if not data.get("description"):
            return {"message": "Description is required"}, 400
        role_name, role_description = data.get("name").strip().rstrip().lstrip().lower(), data.get("description")
        print(role_name, role_description)
        # check if the role_name already exists
        role_query = "SELECT * FROM Role WHERE name = '{0}'".format(role_name)
        # print(role_query)
        conn = db.engine.connect()
        result = conn.execute(role_query)
        if result.fetchone():
            return { "message" : "Role already exists"}, 400
        role_insert_query = "INSERT INTO Role (name, description) VALUES (%s, %s)"
        result = conn.execute(role_insert_query, role_name, role_description)
        db.session.commit()
        conn.close()
        return {"message" : "role created", "role_id" : result.lastrowid}

    
    def delete(self, role_id):
        conn = db.engine.connect()
        delete_user_query = f"DELETE FROM Role WHERE role_id={role_id}"
        result = conn.execute(delete_user_query)
        db.session.commit()
        conn.close()
        if result.rowcount == 0:
            return {"message": f"No role found with ID {role_id}"}, 404
        return {"message": f"Role with ID {role_id} has been deleted"}, 200
            

    def put(self, role_id):
        if role_id is None:
            return {"message" : "No role id provided"}, 400
        conn = db.engine.connect()
        data = request.get_json()
        if data is None:
            return  {"message" : "no data is provided"}, 400
        # retreive user information to validate that updated information do not exist
        role_query = "select * from Role where role_id = '{0}'".format(role_id)
        role_result = conn.execute(role_query)
        # check if user exists 
        if role_result.rowcount == 0:
            return {"message": f"No role found with ID {role_id}"}, 404
        # proceed if the role exist
        role_info = [dict(zip(tuple(role_result.keys()), i)) for i in role_result.cursor][0]
        # check if the role name is same as previous
        update_query_array = []
        if data.get("name"):
            new_role_name = data.get("name")
            if new_role_name == role_info["name"]:
                return {"message" : "Role name already exists"}
            update_query_array.append("name = '{0}'".format(new_role_name))
        if data.get("description"):
            new_role_description = data.get("description")
            update_query_array.append("description = '{0}'".format(new_role_description))
        final_udpate_query = "update Role set {0} where role_id = {1}".format(",".join(update_query_array), role_id)
        conn.execute(final_udpate_query)
        db.session.commit()
        conn.close()
        return {"message" : "Role with ID {0} Modified successfully".format(role_id)}, 200


            
        


