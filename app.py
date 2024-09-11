# import uuid
# from flask import Flask, request
# from db import stores, items
# from flask_smorest import abort


# app = Flask(__name__)

# stores = [{"name": "My store ", "item": [{"name":"my item", "price": 16}]}]


# @app.post('/store')
# def create_store():
#     store_data = request.get_json()
#     if 'name' not in store_data:
#         abort(
#             400, 
#             message = " bad request. Ensure 'name' is included in the JSON payload " 
#         )
#     for store in stores.values():
#         if store_data['name']== store['name']:
#             abort (400, message = f" store already exists ")
#     store_id = uuid.uuid4().hex
#     store = {**store_data, 'id':store_id}
#     store[store_id]= store
#     return store

# # @app.post('/store')
# # def create_store():
# #     store_data = request.get_json()
# #     if 'name' not in store_data:
# #         abort(400, message="Yêu cầu không hợp lệ. Đảm bảo 'name' có trong payload JSON.")
    
# #     for store in stores.values():
# #         if store_data['name'] == store['name']:
# #             abort(400, message="Cửa hàng đã tồn tại.")
    
# #     store_id = uuid.uuid4().hex
# #     store = {**store_data, 'id': store_id, 'items': []}
# #     stores[store_id] = store
# #     return store, 201


# @app.post('/item')
# def create_item():
#     item_data = request.get_json()
#     if (
#         'price' not in item_data
#         or 'store_id' not in item_data
#         or 'name' not in item_data
#     ):
#         abort (
#             400,
#             message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#         )
#     for item in items.values():
#         if (
#             item_data['name'] == item['name']
#             and item_data['store_id'] == item['store_id']

#         ):
#             abort(400, message = f' item already exitst')
#     item_id = uuid.uuid4().hex
#     item = {**item_data, 'id':item_id}
#     items[item_id]= item
#     stores[item_data['store_id']]['items'].append(item)
#     return item

# @app.get('/store/<string:store_id>')
# def get_store(store_id):
#     try:
#         # Here you might also want to add the items in this store
#         # We'll do that later on in the course
#         return stores[store_id]
#     except KeyError:
#         abort(404, message="Store not found.")

 

# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="Item not found.")

# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}


# @app.delete('/item/<string:item_id>')
# def delete_item (item_id):
#     try:
#         item = items.pop(item_id)
#         store_id = item['store_id']
#         stores[store_id]['items'] = [i for i in stores[store_id]['items'] if i['id'] != item_id]
#         return {"message": "Đã xóa mặt hàng."}, 200
#     except KeyError:
#         abort(404, message="Không tìm thấy mặt hàng.")

# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     # There's  more validation to do here!
#     # Like making sure price is a number, and also both items are optional
#     # You should also prevent keys that aren't 'price' or 'name' to be passed
#     # Difficult to do with an if statement...
#     if "price" not in item_data or "name" not in item_data:
#         abort(
#             400,
#             message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
#         )
#     try:
#         item = items[item_id]
#         item |= item_data

#         return item
#     except KeyError:
#         abort(404, message="Item not found.")


# @app.delete("/store/<string:store_id>")
# def delete_store(store_id):
#     try:
#         del stores[store_id]
#         return {"message": "Store deleted."}
#     except KeyError:
#         abort(404, message="Store not found.")


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')

from flask import Flask
from flask_smorest import Api
from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    api = Api(app)

    with app.app_context():
        db.create_all()
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_bluprint(TagBlueprint)
    return app
