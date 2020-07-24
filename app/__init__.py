'''
@Descripttion: 
@version: 
@Author: Zefeng Neo Zhu
@Date: 2020-07-17 11:27:39
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-24 17:25:02
'''
import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


''' 创建数据库 ''' 
database = SQLAlchemy()

''' 创建用户认证管理 '''
login_manager = LoginManager()

def create_app():
    """
        创建并配置应用
    """

    ''' 创建 Flask 实例 '''
    # __name__ 是当前 Python 模块的名称。应用需要知道在哪里设置路径， 使用 __name__ 是一个方便的方法。
    # instance_relative_config=True 告诉应用配置文件是相对于实例文件夹 <instance folder> 的相对路径。
    # 实例文件夹在 app 包的外面，用于存放本地数据（例如配置密钥和数据库），不应当提交到版本控制系统。
    app = Flask(__name__, instance_relative_config=True)

    ''' 加载软件的配置文件 '''
    app.config.from_object('config')
    
    ''' 创建实例文件夹 <instance folder>  '''
    # os.makedirs可以确保实例文件夹 app.instance_path 存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    ''' 初始化设置 '''
    # 初始化数据库
    database.init_app(app)

    # 初始化用户权证管理
    login_manager.init_app(app)
    
    ''' 注册蓝图 '''
    # 导入并注册 auth 蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    ''' 软件首页 '''
    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    return app