from db import db

class ItemTags(db.Model):
    __tablename__="items_tags"

    id = db.Colum(db.Interger, primary_key = True)
    item_id = db.Colum(db.Interger, db.ForeignKey("items.id"))
    tag_id = db.Colum(db.Interger, db.ForeignKey("tags.id"))
    