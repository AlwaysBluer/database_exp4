from app.models import User
from app.models import CfgNotify
from peewee import Model
from app.utils import query_to_list
from datetime import datetime
# query = CfgNotify.select()
# query_list = [(obj.__dict__['__data__']['id'], obj.__dict__['__data__']['notify_name']) for obj in query]
# # for obj in query:
# #     print(obj.__dict__['__data__'])
# #     obj_dict = obj.__dict__['__data__']
# #     query_list.append((obj_dict['id'],obj_dict['notify_name']))
# print(query_list)
datetime_ = datetime.now().strftime('%Y-%m-%d %H:%M')
print(datetime_)



