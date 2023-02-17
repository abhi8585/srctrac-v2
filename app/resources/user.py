from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class UserResource(Resource):
    def post(self):
        # Parse the request body
        data = request.get_json()

        # Validate the request data
        if not data:
            return {"message": "No input data provided"}, 400
        if not data.get("username"):
            return {"message": "Username is required"}, 400
        if not data.get("password"):
            return {"message": "Password is required"}, 400
        if not data.get("email"):
            return {"message": "Email is required"}, 400

        # Check if the email already exists in the database

        email_query = "SELECT * FROM User WHERE email = '{0}'".format(data["email"])
        result = db.engine.execute(email_query)
        row = result.fetchone()
        if row:
            return {"message": "Useremail already exists"}, 400

        # Hash the password
        hashed_password = generate_password_hash(data["password"], method="sha256")

        # Insert the new user into the database

        query = "INSERT INTO User (username, email, password) VALUES (%s, %s, %s)"
        db.engine.execute(query, data['username'], data['email'], hashed_password)
        db.session.commit()

        # Generate a JWT for the new user
        result = db.engine.execute(email_query)
        row = result.fetchone()
        jwt_token = create_access_token(identity=row['user_id'])

        # Close the database connection
        db.engine.dispose()

        # Return the JWT to the client
        return {"access_token": jwt_token}, 201


    def get(self, user_id=None):
        if user_id is None:
            return {"message": "No user id provided"}, 400
        else:
            conn = db.engine.connect()
            query = conn.execute("SELECT * FROM User WHERE user_id = %s" % user_id)
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            if len(result) == 0:
                return {"message" : "User does not exist!"}
            conn.close()
            return {"user": result[0]}, 200

    def delete(self, user_id):
        conn = db.engine.connect()
        delete_user_query = f"DELETE FROM User WHERE user_id={user_id}"
        result = conn.execute(delete_user_query)
        conn.close()
        if result.rowcount == 0:
            return {"message": f"No user found with ID {user_id}"}, 404
        return {"message": f"User with ID {user_id} has been deleted"}, 200


    def put(self, user_id):
        conn = db.engine.connect()
        data = request.get_json()
        # retreive user information to validate that updated information do not exist
        user_query = "select * from user where user_id = '{0}'".format(user_id)
        user_result = conn.execute(user_query)
        # check if user exists 
        if user_result.rowcount == 0:
            return {"message": f"No user found with ID {user_id}"}, 404
        # # proceed if the user exist
        user_info = [dict(zip(tuple(user_result.keys()), i)) for i in user_result.cursor][0]
        # print(type(result['password']))
        if not data:
            return {"message": "No input data provided"}, 400
        update_query_array = []
        if data.get("username"):
            new_username = data.get("username")
        #     # check if the updated username already exists
            user_query = "SELECT * FROM User where username = '{0}'".format(new_username)
            result = conn.execute(user_query)
            if result.rowcount > 0:
                return {"message" : "Given Username already exists"}, 400
            # add code to update the select query 
            update_query_array.append("username = '{0}'".format(new_username))
        # check if the user is using same password again
        if data.get("password"):
            new_password = data.get("password")
            if check_password_hash(user_info['password'], new_password):
                return {"message" : "Please use different password"}
            # add code to update the select query 
            new_hash_password = generate_password_hash(new_password, method="sha256")
            update_query_array.append("password = '{0}'".format(new_hash_password))
        # check if the given email already exists
        if data.get("email"):
            # print("need to update email")
            new_email = data.get("email")
            email_query = "select * from User where email = '{0}'".format(new_email)
            email_result = conn.execute(email_query)
            if email_result.rowcount > 0:
                return {"message" : "Given Email already exists"}, 400
            # add code to update the select query 
            update_query_array.append("email = '{0}'".format(new_email))
        final_udpate_query = "update User set {0} where user_id = {1}".format(",".join(update_query_array), user_id)
        conn.execute(final_udpate_query)
        db.session.commit()
        conn.close()
        return {"message" : "User with ID {0} Modified successfully".format(user_id)}, 200
        
            
        


# UserList
# shows a list of all the users, and lets you POST to add new tasks
class UserListResource(Resource):
    def get(self):
        conn = db.engine.connect()
        query = conn.execute("SELECT * FROM User")
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        conn.close()
        return {"users": result}, 200