from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import canteen
from app.utils import query_to_list

query = canteen.select()
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
    id = StringField('商铺编号', validators=[DataRequired(message='不能为空'), Length(4, message='长度不正确')])
    store_name = StringField('商铺名称', validators=[DataRequired(message='不能为空'), Length(0, 10, message='长度不正确')])
    store_telenum = StringField('联系电话',validators=[DataRequired(message='不能为空'), Length(0, 11, message='长度不正确')])
    store_state = BooleanField("营业状态", default=True)
    canteen_id = SelectField('所在食堂', choices=[(obj.__dict__['__data__']['id'],
                                               obj.__dict__['__data__']['canteen_name']) for obj in query])
    submit = SubmitField('提交')