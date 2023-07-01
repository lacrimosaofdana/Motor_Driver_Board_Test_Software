from flask import render_template

from motor_driver_board_test_software import app

# 400错误界面
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


# 404错误界面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


# 500错误界面
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500