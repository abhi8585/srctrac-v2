from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import json
from datetime import datetime
import copy


class SerializedProductResource(Resource):

    def get(self, product_id=None):
        if product_id is None:
            return {"message": "No product id provided"}, 400
        else:
            conn = db.engine.connect()
            query = conn.execute("""SELECT product_id,
                                        name,
                                        created_at,
                                        description
                                        FROM products
                                    WHERE product_id = %s
                                    and is_serialized = 1
                                    and attributes is NULL""" % product_id)
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            if len(result) == 0:
                return {"message" : "Product does not exist!"}
            conn.close()
            product_object = copy.deepcopy(result)[0]  
            # product_object['attributes'] = json.loads(product_object['attributes'])
            product_object['created_at'] = product_object['created_at'].strftime("%Y-%m-%d")
            # product_object['updated_at'] = product_object['updated_at'].strftime("%Y-%m-%d")
            return jsonify(dict(product=product_object), 200)

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        if not data.get("name"):
            return {"message": "Productname is required"}, 400
        if not data.get("description"):
            return {"message" : "Product description is required"}, 400
        product_name = data.get("name")
        product_description = data.get("description")
        conn = db.engine.connect()
        query = "INSERT INTO products (name, description, is_serialized) VALUES (%s, %s, %s)"
        # result = db.engine.execute(query, product_name, product_description, True)
        result = conn.execute(query, product_name, product_description, True) 
        db.session.commit()
        return {"message" : "product created", "product_id" : result.lastrowid}



# SerializedProductList
class SerializedProductListResource(Resource):
    def get(self):
        conn = db.engine.connect()
        query = conn.execute("""select product_id,
                                    name,
                                    description
                                    from products where is_serialized = 1
                                and attributes is null;
                            """)
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        if len(result) == 0:
            return { "message" : "No product found!"}
        product_list_object = copy.deepcopy(result)
        # for product_object in product_list_object:
        #     product_object['attributes'] = json.loads(product_object['attributes'])
        return jsonify(dict(product=product_list_object), 200)

# ----------------- Code ends here for serialized product resource ------------

class ProductResource(Resource):

    def get(self, product_id=None):
        if product_id is None:
            return {"message": "No product id provided"}, 400
        else:
            conn = db.engine.connect()
            query = conn.execute("""SELECT product_id,
                                        name,
                                        created_at,
                                        description,
                                        attributes
                                        FROM products
                                    WHERE product_id = %s
                                    and is_serialized = 0
                                    and attributes is not NULL""" % product_id)
            result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
            if len(result) == 0:
                return {"message" : "Product does not exist!"}
            conn.close()
            product_object = copy.deepcopy(result)[0]  
            product_object['attributes'] = json.loads(product_object['attributes'])
            product_object['created_at'] = product_object['created_at'].strftime("%Y-%m-%d")
            # product_object['updated_at'] = product_object['updated_at'].strftime("%Y-%m-%d")
            return jsonify(dict(product=product_object), 200)

    def post(self):
        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        if not data.get("name"):
            return {"message": "Productname is required"}, 400
        if not data.get("description"):
            return {"message" : "Product description is required"}, 400
        if not data.get("attributes"):
            return {"message" : "Product attributes is required"}, 400
        product_name = data.get("name")
        product_description = data.get("description")
        product_attributes = data.get("attributes")
        print(type(json.dumps(product_attributes)))
        conn = db.engine.connect()
        query = "INSERT INTO products (name, description, is_serialized, attributes) VALUES (%s, %s, %s, %s)"
        # result = db.engine.execute(query, product_name, product_description, True)
        result = conn.execute(query, product_name, product_description, False, json.dumps(product_attributes))
        db.session.commit()
        return {"message" : "product created", "product_id" : result.lastrowid}



# ProductList
class ProductListResource(Resource):
    def get(self):
        conn = db.engine.connect()
        query = conn.execute("""select product_id,
                                    name,
                                    description,
                                    attributes
                                    from products where is_serialized = 0
                                and attributes is not null;
                            """)
        result = [dict(zip(tuple(query.keys()), i)) for i in query.cursor]
        if len(result) == 0:
            return { "message" : "No product found!"}
        product_list_object = copy.deepcopy(result)
        for product_object in product_list_object:
            product_object['attributes'] = json.loads(product_object['attributes'])
        return jsonify(dict(product=product_list_object), 200)