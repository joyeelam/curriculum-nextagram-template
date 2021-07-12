from models.base_model import BaseModel
from models.image import Image
import peewee as pw

class Donation(BaseModel):
    amount = pw.IntegerField(null = False)
    image = pw.ForeignKeyField(Image, backref="donations", on_delete="CASCADE")
