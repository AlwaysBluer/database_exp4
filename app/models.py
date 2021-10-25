# -*- coding: utf-8 -*-

from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField, \
    DecimalField, ForeignKeyField, DateTimeField, TextField
import json
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
from flask import  session
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)


class BaseModel(Model):
    class Meta:
        database = db

    __mapper_args__ = {
        'polymorphic_identity': 'user_table',
    }
    def __str__(self):
        r = {}
        for k in self.__data__.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)




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
    #store_id作为外键，关联的是一个定义好的模型model的主键，

#user
class user_info(UserMixin, BaseModel):
    id = CharField(primary_key=True)
    user_name = CharField()
    user_state = BooleanField()
    user_passwd = CharField()
    user_telenum = CharField()
    user_type = CharField(default='user')
    def verify_password(self, raw_password):
        return self.user_passwd == raw_password

#
class deal(BaseModel):
    id = CharField(primary_key=True)
    is_finish = BooleanField()
    deal_state = BooleanField()
    deal_begin_time = DateTimeField(null = True)
    deal_finish_time = DateTimeField(null = True)
    user_id = ForeignKeyField(model=user_info, related_name='deals')
    store_id = ForeignKeyField(model=store, related_name='deals')

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

class store_manager_info(UserMixin, BaseModel):
    id = CharField(primary_key=True)
    user_name = CharField()
    user_state = BooleanField()
    user_passwd = CharField()
    user_telenum = CharField()
    user_type = CharField(default='store_manager')
    store_id = ForeignKeyField(store, related_name='store_managers')
    def verify_password(self, raw_password):
        return self.user_passwd == raw_password

class canteen_manager_info(UserMixin, BaseModel):
    id = CharField(primary_key=True)
    user_name = CharField()
    user_state = BooleanField()
    user_passwd = CharField()
    user_telenum = CharField()
    user_type = CharField(default='user')
    canteen_id = ForeignKeyField(canteen, related_name='canteen_managers')
    def verify_password(self, raw_password):
        return self.user_passwd == raw_password


providers = {'user': user_info,
             'canteen_manager': canteen_manager_info,
             'store_manager': store_manager_info}


@login_manager.user_loader
def load_user(id):
    # return User.get(User.id == id)
    login_type = session.get('login_type')
    if login_type == 'user':
        return user_info.get(user_info.id == id)
    elif login_type == 'canteen_manager':
        return canteen_manager_info.get(canteen_manager_info.id == id)
    else:
        return store_manager_info.get(store_manager_info.id == id)

# 建表
def create_table():
    db.connect()
    db.create_tables([CfgNotify, User, canteen, store, dish, dish_deal, deal, user_info, comment,
                        canteen_manager_info, store_manager_info])

#初始化
def init_table():
    canteen.create(id='001',canteen_name='荔园一食堂', canteen_state=True)
    canteen.create(id='002',canteen_name='荔园二食堂', canteen_state=True)
    store.create(id='0001', store_name='姐妹豆花', store_telenum='16786547612', store_state=True,
                 canteen_id='001')
    store.create(id='0002', store_name='过桥米线', store_telenum='16786589612', store_state=True,
                 canteen_id='002')
    store.create(id='0003', store_name='开饭啦', store_telenum='16786589612', store_state=True,
                 canteen_id='002')
    user_info.create(id='00001', user_state=True, user_name='jzj', user_telenum='19958760273',
                     user_passwd='12345', user_type='user')
    canteen_manager_info.create(id='00001', canteen_id='001',user_name='canteen_manager1',user_passwd='12345',user_telenum='17786569860',
                                user_state=True,user_type='canteen_manager')
    store_manager_info.create(id='00001', store_id='0001',user_name='store_manager1',user_passwd='12345',user_telenum='17786569860',
                                user_state=True,user_type='store_manager')
    dish.create(id='00001', dish_name='集美豆花', dish_price=15.0, is_on_sale=True,dish_state=True,
                store_id='0001')
    dish.create(id='00002', dish_name='米饭', dish_price=15.0, is_on_sale=True, dish_state=True,
                store_id='0002')
    # dict_ = {'store_state':True, 'store_id':'0005', 'store_name':'粤式烧腊', 'store_telenum':'17756548787', 'canteen_id':'0001'}
    # store.create(**dict_)

if __name__ == '__main__':
    create_table()
    init_table()
    # drop
    # table
    # canteen, canteen_manager_info, comment, deal, dish, dish_deal, store, store_manager_info, user_info;
