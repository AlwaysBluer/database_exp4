# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, \
    DecimalField, ForeignKeyField, DateTimeField, TextField
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self.__data__.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)

    def verify_password(self, raw_password):
        return self.password == raw_password

# 管理员工号
class User(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识

    def verify_password(self, raw_password):
        return self.password == raw_password


# 通知人配置
class CfgNotify(BaseModel):
    check_order = IntegerField()  # 排序
    notify_type = CharField()  # 通知类型：MAIL/SMS
    notify_name = CharField()  # 通知人姓名
    notify_number = CharField()  # 通知号码
    status = BooleanField(default=True)  # 生效失效标识

#食堂
class canteen(BaseModel):
    id = CharField(primary_key=True)
    canteen_name = CharField()
    canteen_state = BooleanField(default=True) #生效失效标识

#商铺
class store(BaseModel):
    id = CharField(primary_key=True)
    store_name = CharField()
    store_telenum = CharField()
    store_state = BooleanField(default=True)
    canteen_id = ForeignKeyField(canteen, related_name = "stores")#foreign key
    # each canteen can have many stores

#dish
class dish(BaseModel):
    id = CharField(primary_key=True)
    dish_name = CharField()
    dish_price = DecimalField()
    is_on_sale = BooleanField()
    dish_state = BooleanField()
    store_id = ForeignKeyField(store, related_name="dishes")
    #store_id作为外键，关联的是一个定义好的模型model，必须要写明白

#user
class user_info(BaseModel):
    id = CharField(primary_key=True)
    user_state = BooleanField()
    user_passwd = CharField()
    user_telenum = CharField()
    user_name = CharField()

#
class deal(BaseModel):
    id = CharField(primary_key=True)
    is_finish = BooleanField()
    deal_state = BooleanField()
    deal_begin_time = DateTimeField(null = True)
    deal_finish_time = DateTimeField(null = True)
    user_id = ForeignKeyField(model=user_info, related_name='deals')

#评价
class comment(BaseModel):
    id = CharField(primary_key=True)
    comment = TextField()
    score = IntegerField()
    user_id = ForeignKeyField(model=user_info, related_name='comments')
    dish_id = ForeignKeyField(model=dish, related_name='comments')

#菜品_订单
class dish_deal(BaseModel):
    dish_id = ForeignKeyField(model=dish, related_name='dish_deals')
    deal_id = ForeignKeyField(model=deal, related_name='dish_deals')

class store_manager_info(BaseModel):
    id = CharField(primary_key=True)
    store_id = ForeignKeyField(store, related_name='store_managers')
    store_manager_passwd = CharField()
    store_manager_state = BooleanField()
    store_manager_telenum = CharField()

class canteen_manager_info(BaseModel):
    id = CharField(primary_key=True)
    canteen_id = ForeignKeyField(canteen, related_name='canteen_managers')
    canteen_manager_passwd = CharField()
    canteen_manager_telenum = CharField()
    canteen_manager_state = BooleanField()

@login_manager.user_loader
def load_user(id):
    return User.get(User.id == int(id))



# 建表
def create_table():
    db.connect()
    db.create_tables([CfgNotify, User, canteen, store, dish, dish_deal, deal, user_info, comment,
                        canteen_manager_info, store_manager_info])

#初始化
def init_table():
    canteen.create(id='001',canteen_name='荔园一食堂', canteen_state=True)
    canteen.create(id='002',canteen_name='荔园二食堂', canteen_state=True)
    # store.create(store_id='0003', store_name='姐妹豆花', store_telenum='16786547612', store_state=True,
    #             canteen_id='0002')
    # store.create(store_id='0004', store_name='过桥米线', store_telenum='16786589612', store_state=True,
    #             canteen_id='0002')
    # dict_ = {'store_state':True, 'store_id':'0005', 'store_name':'粤式烧腊', 'store_telenum':'17756548787', 'canteen_id':'0001'}
    # store.create(**dict_)

if __name__ == '__main__':
    # create_table()
    init_table()
    # drop
    # table
    # canteen, canteen_manager_info, comment, deal, dish, dish_deal, store, store_manager_info, user_info;
