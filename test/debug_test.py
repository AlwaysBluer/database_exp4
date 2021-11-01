from app.models import User
from app.models import CfgNotify, deal
from peewee import Model
from app.utils import query_to_list
from datetime import datetime

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

query = deal.select().order_by(deal.id.desc())
query = query_to_list(query)
obj = query[0]
print(obj['id'])

