'''
@Descripttion: 
@version: 
@Author: Zefeng Neo Zhu
@Date: 2020-07-24 15:42:50
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-24 16:53:35
'''


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


''' 定义用户登录表单 '''
# 定义的表单都需继承自FlaskForm
# 字段初始化时，第一个参数是设置label属性的
class LoginForm(FlaskForm):
    """
        用户登录表单
    """
    
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('remember me', default=False)

