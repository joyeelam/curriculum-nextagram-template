from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Image(BaseModel):
    image_url = pw.TextField(unique = True, null = False)
    image_caption = pw.TextField(null = True)
    user = pw.ForeignKeyField(User, backref="images", on_delete='CASCADE')
