import sqlite3

# g 是一个特殊对象，独立于每一个请求。
# --在处理请求过程中，它可以用于储存可能多个函数都会用到的数据。
# --把连接储存于其中，可以多次使用，而不用在同一个请求中每次调用 get_db 时都创建一个新的连接
# current_app 也是一个特殊对象，该对象指向处理请求的 flask 应用
# --使用了应用工厂后，在其余的代码中就不会出现应用对象。
# --当应用创建后，在处理一个请求时， get_db 会被调用。这样就需要使用 current_app 
import click
from flask import g
from flask import current_app
from flask.cli import with_appcontext

def get_db():
    '''连接数据库'''

    # sqlite3.connect() 建立一个数据库连接，该连接指向配置中的 DATABASE 指定的文件
    # sqlite3.Row 告诉连接返回类似于字典的行，这样可以通过列名称来操作数据
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    '''关闭数据库'''
    
    #通过检查 g.db 来确定连接是否已经建立。如果连接已建立，那么就关闭连接
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    '''初始化数据库'''

    # open_resource() 打开一个文件，该文件名是相对于 flaskr 包的
    # get_db 返回一个数据库连接，用于执行打开的文件中的命令
    db = get_db()
    with current_app.open_resource('record_system.sql') as f:
        db.executescript(f.read().decode('utf8'))

# click.command() 定义一个名为 init-db 命令行，它调用 init_db 函数，并为用户显示一个成功的消息
@click.command('init-db')
@with_appcontext
def init_db_command():
    """清除已存在的数据，并创建新的表"""

    init_db()
    click.echo('Initialized the database...')

def init_app(app):
    '''用于在应用实例中注册函数，否则无法使用'''

    # app.teardown_appcontext() 告诉 flask 在返回响应后进行清理的时候调用此函数
    # app.cli.add_command() 添加一个新的可以与 flask 一起工作的命令
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)