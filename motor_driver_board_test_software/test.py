from time import sleep
from flask import jsonify
from motor_driver_board_test_software import app, db
from motor_driver_board_test_software.models import test_result, configuration
from datetime import datetime
from flask_login import current_user

# 扫描二维码读取条码信息
# 当你的程序完成后，你可以将结果返回给前端
@app.route('/qrcode/<string:console>', methods=['POST'])
def qrcode(console):
    sleep(5)
    result = 'abc1234567'
    global final_test_result
    final_test_result = test_result(id = result, test_time=datetime.now(), test_user=current_user.username, test_console=console)
    return jsonify(result)


# 开始测试，使用modbus rtu协议读取参数
# 当你的程序完成后，你可以将结果返回给前端
@app.route('/board_test', methods=['POST'])
def board_test():
    sleep(5)
    final_test_result.ecurrent = 1
    final_test_result.voltage = 1
    final_test_result.epower = 1
    final_test_result.rev = 1
    test_config = configuration.query.first()
    if (test_config.al <= final_test_result.ecurrent <= test_config.ah and
        test_config.vl <= final_test_result.voltage <= test_config.vh and
        test_config.wl <= final_test_result.epower <= test_config.wh and
        test_config.tl <= final_test_result.rev <= test_config.th):
        final_test_result.validate = True
    else:
        final_test_result.validate = False
    db.session.merge(final_test_result)
    db.session.commit()
    result = final_test_result.to_dict()
    return jsonify(result)