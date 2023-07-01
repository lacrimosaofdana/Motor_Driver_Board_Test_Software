import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import current_user

app = Flask(__name__)

# app相关配置设置，根据实际情况修改
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:plokijQAZWSXEDC1009@127.0.0.1:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)


# 创建用户加载回调函数，接受用户 ID 作为参数
@login_manager.user_loader
def load_user(user_id):
    from motor_driver_board_test_software.models import User
    user = User.query.get(int(user_id))
    return user

# 设置login_manager的信息
login_manager.login_view = 'login'
login_manager.login_message = "请登录后进行操作"
login_manager.login_message_category = "success"


# 模板上下文处理函数，注入current_user
@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

from motor_driver_board_test_software import views, errors, commands
