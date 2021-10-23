from flask import Flask
from flask_login import LoginManager
from conf.config import config
import logging
from logging.config import fileConfig
import os

login_manager = LoginManager()
login_manager.session_protection = 'strong'
#如果当login_required没有登录的时候，那么会通过login_view跳转到login函数
login_manager.login_view = 'auth.login'
fileConfig(r"C:\Users\jqf13\Desktop\flask-adminlte-scaffold\conf\log-app.conf")

def get_logger(name):
    return logging.getLogger(name)


def get_basedir():
    return os.path.abspath(os.path.dirname(__file__))


def get_config():
    return config[os.getenv('FLASK_CONFIG') or 'default']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

