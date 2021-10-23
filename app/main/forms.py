from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField,\
                    TextAreaField, HiddenField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import canteen, store, user_info
from app.utils import query_to_list
from datetime import datetime



class CfgNotifyForm(FlaskForm):
    check_order = StringField('排序', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_type = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],
                              validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_name = StringField('通知人姓名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_number = StringField('通知号码', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')


class StoreForm(FlaskForm):
    query = canteen.select()
    id = StringField('商铺编号', validators=[DataRequired(message='不能为空'), Length(4, message='长度为4')])
    store_name = StringField('商铺名称', validators=[DataRequired(message='不能为空'), Length(0, 10, message='长度不正确')])
    store_telenum = StringField('联系电话',validators=[DataRequired(message='不能为空'), Length(0, 11, message='长度不正确')])
    store_state = BooleanField("营业状态", default=True)
    canteen_id = SelectField('所在食堂', choices=[(obj.__dict__['__data__']['id'],
                                               obj.__dict__['__data__']['canteen_name']) for obj in query])
    submit = SubmitField('提交')

class DishForm(FlaskForm):
    query = store.select()
    id = StringField('菜品编号', validators=[DataRequired(message='不能为空'), Length(5, message='长度为5')])
    dish_name = StringField('菜品名称', validators=[DataRequired(message='不能为空'), Length(0, 10, message='长度不正确')])
    dish_price = StringField('菜品价格', validators=[DataRequired(message='不能为空'), Length(2, message='长度为2')])
    is_on_sale = BooleanField("是否在售", default=True)
    dish_state = BooleanField("菜品还在吗", default=True)
    store_id = SelectField('所属商铺', choices=[(obj.__dict__['__data__']['id'],
                                               obj.__dict__['__data__']['store_name']) for obj in query])
    submit = SubmitField('提交')

class UserForm(FlaskForm):
    id = StringField('用户id', validators=[DataRequired(message='不能为空'), Length(5, message='长度为5')])
    user_name = StringField('用户昵称', validators=[DataRequired(message='不能为空'), Length(0, 10, message='长度10以内')])
    user_passwd = PasswordField('密码', validators=[DataRequired(message='不能为空'), Length(0, 20, message='20以内')])
    user_telenum = StringField('电话号码', validators=[DataRequired(message='不能为空'), Length(11, message='格式不对')])
    user_state = BooleanField("用户状态", default=True)
    submit = SubmitField('提交')

class DealForm(FlaskForm):
    query = user_info.select()
    id = StringField('订单编号', validators=[DataRequired(message='不能为空'), Length(7, message='长度为7')])
    is_finish = BooleanField("是否完成", default=False)
    deal_state = BooleanField("订单状态", default=True)
    deal_begin_time = DateTimeField('开始时间',default =datetime.now())
    deal_finish_time = DateTimeField('结束时间', default = datetime.now())
    # user_id = StringField('用户编号', validators=[DataRequired(message='不能为空'), Length(5, message='长度为5')])
    user_id = SelectField('所属用户', choices=[(obj.__dict__['__data__']['id'],
                                               obj.__dict__['__data__']['user_name']) for obj in query])
    submit = SubmitField('提交')