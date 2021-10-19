from app.models import User
from app.models import CfgNotify
from peewee import Model
query = CfgNotify.select()
print(query.__dict__)

