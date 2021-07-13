from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Follow(BaseModel):
    creator = pw.ForeignKeyField(User)
    follower = pw.ForeignKeyField(User)
    approval_status = pw.BooleanField(default=False)
