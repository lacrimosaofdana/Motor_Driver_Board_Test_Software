import click
from motor_driver_board_test_software import app, db
from motor_driver_board_test_software.models import User

# 创建管理员账号
@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    db.create_all()

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        click.echo('用户名已存在')
    else:
        click.echo('创建用户...')
        user = User(username=username, admin_status=True)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')