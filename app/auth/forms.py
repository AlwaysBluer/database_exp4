from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64), ])
    password = PasswordField('密码', validators=[DataRequired()])
    rememberme = BooleanField('记住我')
    submit = SubmitField('提交')

class CustomLoginForm(FlaskForm):
    user_type = SelectField('用户类型', choices=[('user', '普通用户'), ('store_manager', '商铺管理'), ('canteen_manager', '食堂管理')])
    id = StringField('用户名', validators=[DataRequired(), Length(5,message='长度为5'), ])
    password = PasswordField('密码', validators=[DataRequired()])
    rememberme = BooleanField('记住我', default=False)
    submit = SubmitField('提交')
