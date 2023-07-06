from time import sleep
from flask import jsonify
from motor_driver_board_test_software import app, db
from motor_driver_board_test_software.models import test_result, configuration, modbus_data
from datetime import datetime
from flask_login import current_user
from pymodbus.client import ModbusSerialClient

def read_data(console_data):
    client = ModbusSerialClient(
        port = console_data.port_data,  # 串口号，请根据实际情况更改
        baudrate = console_data.baudrate,  # 波特率，请根据实际情况更改
        bytesize = console_data.bytesize,  # 数据位，请根据实际情况更改
        parity = console_data.parity,  # 校验位，请根据实际情况更改
        stopbits = console_data.stopbits,  # 停止位，请根据实际情况更改
    )
    
    result = 0

    # 连接到Modbus从机设备
    client.connect()

    try:
        test_result = client.read_holding_registers(console_data.address, count=console_data.count, slave=console_data.slave_address)
        if test_result.isError():
            print("读取错误:", test_result)
        else:
            print("读取结果:", test_result.registers)
            result = test_result.registers
    except Exception as e:
        print("读取异常:", str(e))
    
    # 关闭连接
    client.close()
    return result

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
@app.route('/board_test/<string:console>', methods=['POST'])
def board_test(console):
    # 发送命令并接收响应
    consoles = []
    if console == 'Console 1':
        consoles.append(modbus_data.query.get(1))
        consoles.append(modbus_data.query.get(2))
        consoles.append(modbus_data.query.get(3))
        consoles.append(modbus_data.query.get(4))
    else:
        consoles.append(modbus_data.query.get(5))
        consoles.append(modbus_data.query.get(6))
        consoles.append(modbus_data.query.get(7))
        consoles.append(modbus_data.query.get(8))

    results = []
    for console_data in consoles:
        result = read_data(console_data)
        results += result
    final_test_result.ecurrent = results[0]
    final_test_result.voltage = results[1]
    final_test_result.epower = results[2]
    final_test_result.rev = results[3]
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