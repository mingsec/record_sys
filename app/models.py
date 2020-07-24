'''
@Descripttion: 
@version: 
@Author: Zefeng Neo Zhu
@Date: 2020-07-24 16:00:22
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-24 17:14:50
'''

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
import json
import uuid

from app import database as db


# 定义 profile.json, 用于存储用户名和密码
PROFILE_FILE = "profiles.json"

class User(db.Model):
    """
        用户表
    """

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    password = db.Column(db.String(120), )

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    def __repr__(self):
        return f'<User { self.username }>'