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
            "draught_code" : "PINA618",
            "outlet_name" : "Gold Wings Hotel",
            "area" : "kolara",
            "kegs_data" : [
                {
                    "keg_beer_name" : "BUD",
                    "keg_beer_capacity" : "30",
                    "keg_quantity" : "6",
                    "order_item_id" : "1"
                },
                {
                    "keg_beer_name" : "HOG",
                    "keg_beer_capacity" : "15",
                    "keg_quantity" : "4",
                    "order_item_id" : "2"
                } 
            ],
            "total_kegs" : "10",
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
            "draught_code" : "SSAE358",
            "outlet_name" : "MJ Bar",
            "area" : "kolara",
            "kegs_data" : [
                {
                    "keg_beer_name" : "BUD",
                    "keg_beer_capacity" : "30",
                    "keg_quantity" : "12",
                    "order_item_id" : "1"
                },
                {
                    "keg_beer_name" : "MAG",
                    "keg_beer_capacity" : "30",
                    "keg_quantity" : "18",
                    "order_item_id" : "2"
                } 
            ],
            "total_kegs" : "30",
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
            so_numbers = [dict(so_numbers="QDSON"+ str(i), so_id=str(i)) for i in range(0,10)]
            return {"so_numbers": so_numbers}, 200


class SalesOrderResource(Resource):
    def get(self, order_id = None):
        if not request.args.get('order_id'):
            return dict(status="failed",message= "No order id provided"), 400
        order_id = request.args.get('order_id')
        for so in order_dummy_data:
            if so['id'] == order_id:
                return dict(status=200,order_data=so['data']), 200
        return dict(status=200,order_data=[]), 200
        
