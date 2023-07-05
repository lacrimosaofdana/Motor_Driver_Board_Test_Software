from time import sleep
from flask import jsonify
from motor_driver_board_test_software import app, db
from motor_driver_board_test_software.models import test_result, configuration
from datetime import datetime
from flask_login import current_user
from pymodbus.client import ModbusSerialClient

def read_data():
    client1 = ModbusSerialClient(
        method='rtu',
        port='/dev/ttyUSB0',  # 串口号，请根据实际情况更改
        baudrate=9600,  # 波特率，请根据实际情况更改
        bytesize=8,  # 数据位，请根据实际情况更改
        parity='N',  # 校验位，请根据实际情况更改
        stopbits=1,  # 停止位，请根据实际情况更改
        timeout=1  # 超时时间，请根据实际情况更改
    )

    client2 = ModbusSerialClient(
        method='rtu',
        port='/dev/ttyUSB0',  # 串口号，请根据实际情况更改
        baudrate=9600,  # 波特率，请根据实际情况更改
        bytesize=8,  # 数据位，请根据实际情况更改
        parity='N',  # 校验位，请根据实际情况更改
        stopbits=1,  # 停止位，请根据实际情况更改
        timeout=1  # 超时时间，请根据实际情况更改
    )

    results = []
    # 连接到Modbus从机设备
    if client1.connect():
        # 读取寄存器
        addresses = [0xB9, 0xB6, 0xBD]  # 起始地址, [电流, 电压, 功率]
        count = 4  # 要读取的寄存器数量

        # 逐个发送指令并处理响应
        for address in addresses:
            try:
                result = client1.read_holding_registers(address, count, unit=1)
                if result.isError():
                    print("读取错误:", result)
                else:
                    print("读取结果:", result.registers)
                    results.append(result)
            except Exception as e:
                print("读取异常:", str(e))
    else:
        print("无法连接到Modbus从机设备")

    # 关闭连接
    client1.close()

    # 连接到Modbus从机设备
    if client2.connect():
        # 读取寄存器
        address = 0x98  # 起始地址, 频率
        count = 4  # 要读取的寄存器数量

        # 发送指令并处理响应
        try:
            result = client2.read_holding_registers(address, count, unit=1)
            if result.isError():
                print("读取错误:", result)
            else:
                print("读取结果:", result.registers)
                results.append(result)
        except Exception as e:
            print("读取异常:", str(e))
    else:
        print("无法连接到Modbus从机设备")

    # 关闭连接
    client2.close()
    return results


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
    # 发送命令并接收响应
    results = read_data()
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