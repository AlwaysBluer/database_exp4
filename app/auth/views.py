from flask import render_template, redirect, request, url_for, flash
from . import auth
from .forms import LoginForm, CustomLoginForm
from app.models import User, user_info, canteen_manager_info, store_manager_info
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


@auth.route('/login', methods=['GET', 'POST'])
def custom_login(): #id, passwd登录
    form = CustomLoginForm()
    print(form.rememberme.data)
    if form.validate_on_submit():
        try:
            if form.user_type == 'user':#普通用户
                dynamic_model = user_info
            elif form.user_type == 'store_manager':#店铺管理
                dynamic_model = store_manager_info
            else:#食堂管理
                dynamic_model = canteen_manager_info
            model = dynamic_model.get(dynamic_model.id == form.username.data)
            if model.verify_password == form.password.data:
                login_user(model, form.rememberme.data)
                return redirect(request.args.get('next') or url_for('main.index'))
        except :
            flash('用户名或密码错误')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出登录')
    return redirect(url_for('auth.login'))
