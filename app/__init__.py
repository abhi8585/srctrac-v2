from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    api = Api(app)

    # Import and register the API resources here
    from app.resources.user import UserResource, UserListResource
    from app.resources.sku import SkuResource

    # Route for UserResource resource's POST request
    api.add_resource(UserResource, '/register')
    # Route for UserResource resource's GET request
    # api.add_resource(UserResource, '/user/<int:user_id>')
    api.add_resource(UserResource, '/user/<string:user_id>', endpoint='get_user_registration')
    # Route for UserListResource GET request to retreive all user list
    api.add_resource(UserListResource, '/user')
    api.add_resource(SkuResource, '/sku')


   # -------API registration for not serialized product resource
    from app.resources.product import ProductResource, ProductListResource
    #endpoint registration || ProductResource || GET List || GET ID
    api.add_resource(ProductResource,'/product/<string:product_id>')
    api.add_resource(ProductListResource, '/product')
     # endpoint registration || ProductResource || POST
    api.add_resource(ProductResource,'/createproduct',endpoint='create_product_registration')

    # -------API registration for product serialized resource

    from app.resources.product import SerializedProductResource, SerializedProductListResource
    # endpoint registration || SerializedProductResource || GET List || GET ID
    api.add_resource(SerializedProductResource,'/seproduct/<string:product_id>')
    api.add_resource(SerializedProductListResource, '/seproduct')
    # endpoint registration || SerializedProductResource || POST
    api.add_resource(SerializedProductResource,'/createseproduct',endpoint='create_seproduct_registration')

    
    # -------API registration for role resource
    from app.resources.role import RolesListResource, RoleResource
    # endpoint registration || RolesListResource || GET List
    api.add_resource(RolesListResource, '/roles')
    # endpoint registration || RoleResource || GET ID
    api.add_resource(RoleResource,'/roles/<string:role_id>')
    # endpoint registration || RoleResource || POST  || Create new role
    api.add_resource(RoleResource,'/createrole',endpoint='create_role_registration')
    

    # -------API registration for permission resource
    from app.resources.permission import PermissionListResource, PermissionResource
    # endpoint registration || PermissionListResource || GET List
    api.add_resource(PermissionListResource, '/permissions')
    # endpoint registration || RoleResource || GET ID
    api.add_resource(PermissionResource,'/permissions/<string:permission_id>')
    # # endpoint registration || PermissionResource || POST  || Create new permission
    api.add_resource(PermissionResource,'/createpermission',endpoint='create_permission_registration')

    
    # -------API registration for permission resource
    from app.resources.sample import SampleResource
    api.add_resource(SampleResource, '/sample')

    # -------API registration for permission resource
    from app.resources.authentication import LoginResource
    api.add_resource(LoginResource, '/login')


    # -------API registration for serial number resource
    from app.resources.mapping import SerialListResource, SerialMappingResource
    api.add_resource(SerialListResource, '/senumbers')
    api.add_resource(SerialMappingResource, '/semapping')

    # -------API registration for sales order resouce
    from app.resources.sales_order import SalesOrderListResource, SalesOrderResource
    api.add_resource(SalesOrderListResource, '/sorders')
    api.add_resource(SalesOrderResource, '/sorder')

    api.add_resource(SalesOrderResource,'/morder',endpoint='map_keg')


    # -------API registration for user role mapping
    from app.resources.user_role_mapping import UserRoleMappingResource
    api.add_resource(UserRoleMappingResource, '/urmap')

    # endpoint registration || PermissionResource || POST  || Create new permission

    

    return app
