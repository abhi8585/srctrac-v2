from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app import db


order_dummy_data = [
    {
    "id" : "1",
    "data" : {
        "status" : "success",
        "data" : [
        {
           
            "keg_name" : "Budweiser Premium Beer 30 Ltr",
            "stock_code" : "BDD13524",
            "total_keg" : "25"
        },
        {
           
            "keg_name" : "Bud Magnum Beer 30 Ltr",
            "stock_code" : "BWD1324",
            "total_keg" : "14"
        },
        {
           
            "keg_name" : "Hoegaarden Witbier 15 Ltr",
            "stock_code" : "HDD53524)",
            "total_keg" : "12"
        },
    ]
    }
},
{
    "id" : "2",
    "data" : {
        "status" : "success",
        "data" : [
        {
           
            "keg_name" : "Budweiser Premium Beer 30 Ltr",
            "stock_code" : "BDD13524",
            "total_keg" : "9"
        },
        {
           
            "keg_name" : "Bud Magnum Beer 30 Ltr",
            "stock_code" : "BWD1324",
            "total_keg" : "14"
        },
        {
           
            "keg_name" : "Hoegaarden Witbier 15 Ltr",
            "stock_code" : "HDD53524)",
            "total_keg" : "6"
        },
    ]
    }
}
]

# SerialNumber list
# shows a list of all the sales order.
class SalesOrderListResource(Resource):
    # date should be in "YYYY-MM-DD" format
    def get(self):
        if not request.args.get('order_date'):
            return dict(status="failed",message= "No order date provided"), 400
        else:
            order_date = request.args.get('order_date')
            order_date = str("".join(order_date.split("-")))
            print(order_date)
            if order_date == "20230416":
                so_numbers = [dict(so_numbers="QDSON"+ str(i), so_id=str(i)) for i in range(0,10)]
                return {"so_numbers": so_numbers}, 200
            else:
                return {"so_numbers" : []}, 200

class SalesOrderResource(Resource):
    def get(self):
        if not request.args.get('order_id'):
            return dict(status="failed",message= "No order id provided"), 400
        order_id = request.args.get('order_id')
        for so in order_dummy_data:
            if so['id'] == order_id:
                return dict(status=200,order_data=so['data']), 200
        return dict(status=200,order_data=[]), 200

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return {"status": "failed","message": "No input data provided"}, 400
            if not data.get("order_id"):
                return {"status": "failed","message": "Order id is required"}, 400
            if not data.get("stock_number"):
                return {"status": "failed","message": "Stock number is required"}, 400
            if not data.get("keg_uid"):
                return {"status": "failed","message": "UUID is required"}, 400
            return dict(status="success"), 200
        except Exception as e:
            print(e)
            return dict(status="failed"), 200

        

