import os
import sys
import pymysql
import threading
import click
from time import sleep
from datetime import datetime
from flask import Flask, render_template, flash, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:plokijQAZWSXEDC1009@127.0.0.1:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user


login_manager.login_view = 'login'
# login_manager.login_message = 'Your custom message'

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, admin_status=True)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')


class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, default=1)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    admin_status = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class configuration:
    def __init__(self, ammeter_low, ammeter_high, voltmeter_low, voltmeter_high, wattmeter_low, wattmeter_high, tachometer_low, tachometer_high):
        self.al = ammeter_low
        self.ah = ammeter_high
        self.vl = voltmeter_low
        self.vh = voltmeter_high
        self.wl = wattmeter_low
        self.wh = wattmeter_high
        self.tl = tachometer_low
        self.th = tachometer_high

test_config = configuration(1, 2, 1, 2, 1, 2, 1, 2)


class test_result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.String(40), primary_key=True)  # 主键
    ecurrent = db.Column(db.Float, default=0.0)
    voltage = db.Column(db.Float, default=0.0)
    epower = db.Column(db.Float, default=0.0)
    rev = db.Column(db.Float, default=0.0)
    validate = db.Column(db.Float, default=0.0)
    test_time = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self, id, ecurrent=0, voltage=0, epower=0, rev=0, validate=True):
    #     self.id = id
    #     self.ecurrent = ecurrent
    #     self.voltage = voltage
    #     self.epower = epower
    #     self.rev = rev
    #     self.validate = validate

    def to_dict(self):
        return {
            'id': self.id,
            'ecurrent': self.ecurrent,
            'voltage': self.voltage,
            'epower': self.epower,
            'rev': self.rev,
            'validate': '是' if self.validate else '否',
            'test_time': self.test_time,
        }

final_test_result = test_result(id = 'abc')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('请重新输入', 'danger')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功', 'success')
            return redirect(url_for('index'))

        flash('无效用户名或者密码', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'success')
    return redirect(url_for('login'))


@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    if request.method == 'POST':
        ip_ammeter_low = request.form.get('ammeter_low')
        ip_ammeter_high = request.form.get('ammeter_high')
        ip_voltmeter_low = request.form.get('voltmeter_low')
        ip_voltmeter_high = request.form.get('voltmeter_high')
        ip_wattmeter_low = request.form.get('wattmeter_low')
        ip_wattmeter_high = request.form.get('wattmeter_high')
        ip_tachometer_low = request.form.get('tachometer_low')
        ip_tachometer_high = request.form.get('tachometer_high')
        if ip_tachometer_high < ip_tachometer_low:
            flash('无效配置', 'danger')
        elif ip_wattmeter_high < ip_wattmeter_low:
            flash('无效配置', 'danger')
        elif ip_voltmeter_high < ip_voltmeter_low:
            flash('无效配置', 'danger')
        elif ip_ammeter_high < ip_ammeter_low:
            flash('无效配置', 'danger')
        else:
            flash('配置更新', 'success')
            global test_config
            test_config = configuration(ip_ammeter_low, ip_ammeter_high, ip_voltmeter_low, ip_voltmeter_high, ip_wattmeter_low, ip_wattmeter_high, ip_tachometer_low, ip_tachometer_high)
        return redirect(url_for('config'))

    return render_template('config.html', test_config=test_config)

@app.route('/qrcode', methods=['POST'])
@login_required
def qrcode():
    # 在这里运行你的程序
    # 当你的程序完成后，你可以将结果返回给前端
    sleep(5)
    result = 'abc1234567'
    global final_test_result
    final_test_result = test_result(id = result)
    return jsonify(result)

@app.route('/board_test', methods=['POST'])
@login_required
def board_test():
    # 在这里运行你的程序
    # 当你的程序完成后，你可以将结果返回给前端
    sleep(5)
    db.session.merge(final_test_result)
    db.session.commit()
    result = final_test_result.to_dict()
    return jsonify(result)

@app.route('/testing_devices', methods=['GET', 'POST'])
def testing_devices():
    return render_template('testing_devices.html')


@app.route('/display_results', methods=['GET', 'POST'])
def display_results():
    all_test_results = test_result.query.all()
    return render_template('display_results.html', results=all_test_results)

@app.route('/display_results/search', methods=['POST'])
def search():
    id = request.form['id']

    if not test_result.query.get(id):
        flash('搜索无结果！', 'danger')
        return redirect(url_for('display_results'))  # 重定向回对应的编辑页面

    search_item = test_result.query.get_or_404(id)
    return render_template('research_results.html', result=search_item)  # 重定向回主页

@app.route('/display_results/delete/<string:id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(id):
    deleted_item = test_result.query.get_or_404(id)  # 获取电影记录
    db.session.delete(deleted_item)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('删除成功！', 'success')
    return redirect(url_for('display_results'))  # 重定向回主页

if __name__ == '__main__':
    app.run(debug=True)
