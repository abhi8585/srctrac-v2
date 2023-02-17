from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

# from app.services.database import DatabaseOperations


# Roles List
# shows a list of all the roles
class SampleResource(Resource):

    def get(self):
        # conn = db.engine.connect()
        # query = conn.execute("select * from  permission")
        # result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        # if len(result) == 0:
        #     return {"message" : "No Permission exists!"}, 400
        # conn.close()
        return {"message":'hello world'}, 200
