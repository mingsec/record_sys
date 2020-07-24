'''
@Descripttion: 
@version: 
@Author: Zefeng Neo Zhu
@Date: 2020-07-24 16:02:51
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-24 17:04:47
'''


import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, database
from app.models import User

def make_shell_context():
    """
        shell上下文配置
    """
    
    return dict(app=app, database=database, User=User)

''' 创建应用 '''
app = create_app() 

''' 初始化 migrate '''
migrate = Migrate(app, database)

''' 初始化管理器 '''
# 添加 shell 命令
# 添加 db 命令，并与 MigrateCommand 绑定
manager = Manager(app)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()