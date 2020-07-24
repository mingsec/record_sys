'''
@Descripttion: 
@version: 
@Author: Zefeng Neo Zhu
@Date: 2020-07-24 15:33:00
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-24 17:17:49
'''


import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# CSRF_ENABLED 用于激活 跨站点请求伪造 保护
# SECRET_KEY 仅当 CSRF 激活的时候才需要，它用来建立一个加密的令牌，用于验证表单
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

# SQLALCHEMY_DATABASE_URI 是 Flask-SQLAlchemy 的数据库文件路径
# SQLALCHEMY_MIGRATE_REPO 是文件夹，用于存放 SQLAlchemy-migrate 数据文件
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance/record_system.SQLite')
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')