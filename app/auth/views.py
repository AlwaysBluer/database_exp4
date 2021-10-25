from flask import render_template, redirect, request, url_for, flash, session, abort
from . import auth
from .forms import LoginForm, CustomLoginForm
from app.models import User, user_info, canteen_manager_info, store_manager_info, providers
from flask_login import login_user, logout_user, login_required



@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    print(form.rememberme.data)
    if form.validate_on_submit():
        try:
            user = User.get(User.username == form.username.data)
            if user.verify_password(form.password.data):
                login_user(user, form.rememberme.data)
                return redirect(request.args.get('next') or url_for('main.index'))
            else:
                flash('用户名或密码错误')
        except :
            flash('用户名或密码错误')

    return render_template('auth/login.html', form=form)


@auth.route('/custom_login', methods=['GET', 'POST'])
def custom_login(): #id, passwd登录
    form = CustomLoginForm()
    print(form.rememberme.data)
    if form.validate_on_submit():
        # try:
            if form.user_type.data == 'user':  # 普通用户
                dynamic_model = user_info

            elif form.user_type.data == 'store_manager':  # 店铺管理
                dynamic_model = store_manager_info

            else:  # 食堂管理
                dynamic_model = canteen_manager_info

            model = dynamic_model.get(dynamic_model.id == form.id.data)
            if model.verify_password(form.password.data):
                callback(form.user_type.data)
                login_user(model, form.rememberme.data)
            return redirect(request.args.get('next') or url_for('main.index'))  # 测试用
        # except :
        #     flash('用户名或密码错误')
    return render_template('auth/login.html', form=form)


@auth.route('/callback/<provider_name>')
def callback(provider_name):
    if provider_name not in providers.keys():
        abort(404)
    session['login_type'] = provider_name


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('login_type', None)
    flash('您已退出登录')
    return redirect(url_for('auth.custom_login'))
