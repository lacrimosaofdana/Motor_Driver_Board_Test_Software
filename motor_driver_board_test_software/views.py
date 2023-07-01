from flask import render_template, flash, request, url_for
from werkzeug.utils import redirect
from flask_login import login_user, login_required, logout_user
from motor_driver_board_test_software import app, db
from motor_driver_board_test_software.models import User, configuration, test_result

# 主页
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# 登录界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = bool(request.form.get('remember'))

        if not username or not password:
            flash('请重新输入', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()

        if user and user.validate_password(password):
            login_user(user, remember=remember)
            flash('登录成功', 'success')
            return redirect(url_for('index'))

        flash('无效用户名或者密码', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')

# 注册界面
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']

        if not username or not password or not repassword:
            flash('无效用户名或者密码', 'danger')
            return redirect(url_for('signup'))

        if password != repassword:
            flash('密码不一致', 'danger')
            return redirect(url_for('signup'))

        if len(username) > 20:
            flash('用户名长度不能超过20个字符', 'danger')
            return redirect(url_for('signup'))

        if len(password) > 128:
            flash('密码长度不能超过128个字符', 'danger')
            return redirect(url_for('signup'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('用户名已存在', 'danger')
            return redirect(url_for('signup'))

        user = User(username=username, admin_status=False)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('用户创建成功，已登录', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html')

# 登出，会返回主页
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已登出', 'success')
    return redirect(url_for('index'))


# 配置界面
@app.route('/config', methods=['GET', 'POST'])
@login_required
def config():
    test_config = configuration.query.first()
    if request.method == 'POST':
        ip_ammeter_low = request.form.get('ammeter_low')
        ip_ammeter_high = request.form.get('ammeter_high')
        ip_voltmeter_low = request.form.get('voltmeter_low')
        ip_voltmeter_high = request.form.get('voltmeter_high')
        ip_wattmeter_low = request.form.get('wattmeter_low')
        ip_wattmeter_high = request.form.get('wattmeter_high')
        ip_tachometer_low = request.form.get('tachometer_low')
        ip_tachometer_high = request.form.get('tachometer_high')

        # 确保必须为浮点型
        try:
            ip_ammeter_low = float(ip_ammeter_low)
            ip_ammeter_high = float(ip_ammeter_high)
            ip_voltmeter_low = float(ip_voltmeter_low)
            ip_voltmeter_high = float(ip_voltmeter_high)
            ip_wattmeter_low = float(ip_wattmeter_low)
            ip_wattmeter_high = float(ip_wattmeter_high)
            ip_tachometer_low = float(ip_tachometer_low)
            ip_tachometer_high = float(ip_tachometer_high)
        except ValueError:
            flash('无效配置，必须为浮点数', 'danger')
            return redirect(url_for('config'))

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
            test_config.al = ip_ammeter_low
            test_config.ah = ip_ammeter_high
            test_config.vl = ip_voltmeter_low
            test_config.vh = ip_voltmeter_high
            test_config.wl = ip_wattmeter_low
            test_config.wh = ip_wattmeter_high
            test_config.tl = ip_tachometer_low
            test_config.th = ip_tachometer_high
            db.session.add(test_config)
            db.session.commit()
        return redirect(url_for('config'))

    return render_template('config.html', test_config=test_config)

# 测试界面
@app.route('/testing_devices', methods=['GET', 'POST'])
@login_required
def testing_devices():
    return render_template('testing_devices.html')


# 记录展示界面
@app.route('/display_results', methods=['GET', 'POST'])
@login_required
def display_results():
    all_test_results = test_result.query.all()
    return render_template('display_results.html', results=all_test_results)


# 搜索记录
@app.route('/display_results/search', methods=['POST'])
def search():
    id = request.form['id']

    if not test_result.query.get(id):
        flash('搜索无结果', 'danger')
        return redirect(url_for('display_results'))  # 重定向默认界面

    search_item = test_result.query.get_or_404(id)
    return render_template('research_results.html', result=search_item)


# 删除记录，需要管理员权限
@app.route('/display_results/delete/<string:id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(id):
    deleted_item = test_result.query.get_or_404(id)  # 获取电影记录
    db.session.delete(deleted_item)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('删除成功', 'success')
    return redirect(url_for('display_results'))  # 重定向

from motor_driver_board_test_software import test