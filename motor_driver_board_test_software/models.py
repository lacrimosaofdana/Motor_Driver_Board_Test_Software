from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from motor_driver_board_test_software import db


# 用户类
class User(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    admin_status = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 配置类
class configuration(db.Model):
    __tablename__ = 'configuration'
    id = db.Column(db.Integer, primary_key=True, default=1)
    al = db.Column(db.Float, default=0.0)
    ah = db.Column(db.Float, default=0.0)
    vl = db.Column(db.Float, default=0.0)
    vh = db.Column(db.Float, default=0.0)
    wl = db.Column(db.Float, default=0.0)
    wh = db.Column(db.Float, default=0.0)
    tl = db.Column(db.Float, default=0.0)
    th = db.Column(db.Float, default=0.0)


# 测量表参数类
class modbus_data(db.Model):
    __tablename__ = 'modbus_data'
    id = db.Column(db.Integer, primary_key=True)
    port_data = db.Column(db.String(40))
    baudrate = db.Column(db.Float, default=9600)
    bytesize = db.Column(db.Integer, default=8)
    parity = db.Column(db.String(20), default='N')
    stopbits = db.Column(db.Integer, default=1)
    address = db.Column(db.Integer)
    count = db.Column(db.Integer, default=4)
    slave_address = db.Column(db.Integer)

# 测试结果类
class test_result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.String(40), primary_key=True)  # 主键
    ecurrent = db.Column(db.Float, default=0.0)
    voltage = db.Column(db.Float, default=0.0)
    epower = db.Column(db.Float, default=0.0)
    rev = db.Column(db.Float, default=0.0)
    validate = db.Column(db.Float, default=0.0)
    test_user = db.Column(db.String(20))
    test_console = db.Column(db.String(20))
    test_time = db.Column(db.DateTime)


    # 将结果转换为字典
    def to_dict(self):
        return {
            'id': self.id,
            'ecurrent': self.ecurrent,
            'voltage': self.voltage,
            'epower': self.epower,
            'rev': self.rev,
            'validate': True if self.validate else False,
            'test_time': self.test_time,
        }