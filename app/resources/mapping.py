from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app import db


# SerialNumber list
# shows a list of all the serial number.
class SerialListResource(Resource):

    def get(self):
        serial_number_list = ["ABINB00"+ str(i) for i in range(0,10)]
        return {"serial_number_list": serial_number_list}, 200


class SerialMappingResource(Resource):

    def post(self):
        # Parse the request body
        data = request.get_json()
        # Validate the request data
        if not data:
            return {"message": "No input data provided"}, 400
        if not data.get("qr_number"):
            return {"message": "QR number is required"}, 400
        if not data.get("serial_number"):
            return {"message": "Serial number is required"}, 400
        return dict(status="success" ), 200



