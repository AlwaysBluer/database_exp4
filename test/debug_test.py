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
def strID_increase(strID):
    value = int(strID) + 1
    strID = str(value)
    str_ = strID
    lenth = 5
    while len(str_) < lenth:
        if len(str_) >= lenth:
            return str_
        else:
            str_ = '0' + str_
    return str_

id_='1'
print(strID_increase(strID=id_))

