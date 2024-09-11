import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


from db import db
from models import StoreModel

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}, 200
@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}
    @blp.arguments(StoreSchema)
    def post(cls, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
@blp.response(200, StoreSchema(many=True))
def get(self):
    return StoreModel.query.all()

class StoreModel(db.Model):
    __tablename__ = "stores"
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")

@blp.arguments(StoreSchema)
@blp.response(201, StoreSchema)
def post(seft, store_data):
        store = StoreModel(**store_data)
        try: 
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message= "a store with that name already exists.")
        except SQLAIchemyError:
            abort(500, message = " an error occurred creating the store")

        return store