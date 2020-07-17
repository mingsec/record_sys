'''
@Descripttion: 
@version: 
@Author: Zefeng Neo Zhu
@Date: 2020-07-17 11:27:39
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-17 11:34:52
'''
import os

from flask import Flask, render_template


def create_app(test_config=None):
    """ 创建并配置应用
    """

    ''' 创建 Flask 实例 '''
    # __name__ 是当前 Python 模块的名称。应用需要知道在哪里设置路径， 使用 __name__ 是一个方便的方法。
    # instance_relative_config=True 告诉应用配置文件是相对于实例文件夹 <instance folder> 的相对路径。
    # 实例文件夹在 app 包的外面，用于存放本地数据（例如配置密钥和数据库），不应当提交到版本控制系统。
    app = Flask(__name__, instance_relative_config=True)

    # 设置应用的缺省配置
    # SECRET_KEY 是被 Flask 和扩展用于保证数据安全
    # --在开发过程中，为了方便可以设置为 'dev' ，但是在发布的时候应当使用一个随机值来重载它
    # DATABASE 数据库文件 <record_system.sqlite> 存放在路径，它位于 flask 用于存放实例的 app.instance_path 之内
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'record_system.sqlite'),
    )

    # 如果 config.py 存在的话, 使用 config.py 中的值来重载缺省配置
    # test_config实现测试和开发的配置分离，相互独立
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # os.makedirs可以确保实例文件夹 app.instance_path 存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    # 导入并注册数据库
    from . import db
    db.init_app(app)

    # 导入并注册 auth 蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    return app