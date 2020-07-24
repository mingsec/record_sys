# url_for() 函数会根据视图名称自动生成 URL 。
# 视图名称亦称为 【端点】，缺省情况下，端点名称与视图函数名称相同。
# 当使用蓝图的时候，蓝图的名称会添加到函数名称的前面。


import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from app import db, login_manager
from app.forms import LoginForm
from app.models import User


''' 定义蓝图 '''
# __name__ 用于确定蓝图在哪里定义的
# url_prefix 会自动在所有与该蓝图关联的 URL 前面添加 '/auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
    """
        从数据库加载用户
    """
    return User.query.get(int(id))

# @bp.route 关联了 URL /register 和 register 视图函数，
# 当 flask 收到一个指向 /auth/register 的请求时就会调用 register 视图并把其返回值作为响应
@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
        用户注册

        当用户初始访问 auth/register 时，或者注册出错时，显示一个注册表单。
    """

    # 如果用户提交了表单，那么 request.method 将会是 'POST', 并开始验证用户的输入内容
    # request.form 是一个特殊类型的 dict ，其映射了提交表单的键和值
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        # 验证 username 和 password 是否为空
        # 通过查询数据库检查是否有查询结果返回来验证 username 是否已被注册
        # --db.execute 使用了带有 '?' 占位符的 SQL 查询语句，占位符可以代替后面的元组参数中相应的值
        # --使用占位符的好处是会自动帮你转义输入值，以抵御 SQL 注入攻击
        # --fetchone() 根据查询返回一个记录行，如果查询没有结果，则返回 None
        if not username:
            error = "请输入用户名。"
        elif not password:
            error = "请输入密码。" 
        elif db.execute('SELECT id FROM auth_user WHERE username = ?', (username,)).fetchone() is not None:
            error = f"用户名 { username } 已经被注册过了，请换一个用户名。"

        # 如果验证成功，那么在数据库中插入新用户数据
        # --为了安全原因，不能把密码明文储存在数据库中，通过使用 generate_password_hash() 生成安全的哈希值并储存到数据库中
        # 使用 db.commit() 保存修改数据
        # 用户数据保存后将转到登录页面
        # --url_for() 根据登录视图的名称生成相应的 URL，使用url_for的的好处是如果以后需要修改该视图相应的 URL ，那么不用修改所有涉及到 URL 的代码
        # --redirect() 为生成的 URL 生成一个重定向响应。
        if error is None:
            db.execute('INSERT INTO auth_user (username, password) VALUES (?, ?)', (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))

        # 如果验证失败，那么会向用户显示一个出错信息
        # flash() 用于储存在渲染模块时可以调用的信息
        flash(error)

    # render_template() 会渲染一个包含 HTML 的模板。
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
        用户登录

        当用户初始访问 auth/login 时，显示一个登录表单。
    """

    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('homepage'))

    form = LoginForm()

    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data

        login_user(username)

        flask.flash('Logged in successfully.')

        return redirect(url_for('homepage'))
       
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    '''
    用户注销

    把用户 id 从 session 中移除，后继请求中不再载入用户。
    '''

    session.clear()

    return redirect(url_for('index'))

# bp.before_app_request() 会注册一个在视图函数之前运行的函数，不论其 URL 是什么
@bp.before_app_request
def load_logged_in_user():
    ''' 
    获取用户数据

    检查用户 id 是否已经储存在 session 中，如果存在则从数据库中获取用户数据，然后储存在 g.user 中。
    '''

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

def login_required(view):
    '''
    用户登录装饰器
    
    用户登录系统以后才能进行新增、编辑和删除记录等操作。
    该函数会检查用户是否已载入；如果已载入，那么就继续正常执行原视图；否则就重定向到登录页面。
    '''

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

