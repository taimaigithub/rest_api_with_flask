import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError 

from db import items
from db import db
from models import ItemModel

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}


    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        # There's  more validation to do here!
        # Like making sure price is a number, and also both items are optional
        # Difficult to do with an if statement...
    
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating an item is not implemented.")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}
    @blp.arguments(ItemSchema)
    def post(self,item_data):
        
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message=f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        

    
@blp.arguments(ItemSchema)
@blp.response(201, ItemSchema)
def post (seft, item_data):
    item = ItemModel(**item_data)
    try: 
        db.session.add(item)
        db.session.commit()
    except SQLAlchemyError:
        abort(400, message= "an error occurred while inserting the item")
def put(self, item_data, item_id):
    item = ItemModel.query.get(item_id)
    if item:
        item.price = item_data["price"]
        item.name = item_data["name"]
    else:
        item = ItemModel(id=item_id, **item_data)

    db.session.add(item)
    db.session.commit()

@blp.response(200, ItemSchema(many=True))
def get(self):
    return ItemModel.query.all()
    return item