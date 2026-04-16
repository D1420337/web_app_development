from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    註冊路由
    GET: 渲染 auth/register.html 表單
    POST: 接收 username, password，成功建立後重導向至登入頁面
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            password_hash = generate_password_hash(password)
            user_id = User.create(username, password_hash)
            if user_id:
                flash('註冊成功！請登入帳號。', 'success')
                return redirect(url_for('auth.login'))
            else:
                error = '該帳號已被使用，請更換其他帳號。'

        flash(error, 'danger')

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    登入路由
    GET: 渲染 auth/login.html 表單
    POST: 接收並驗證 username, password，成功時寫入 session 並重導向首頁
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        error = None

        if not username or not password:
            error = '請輸入帳號和密碼。'
        else:
            user = User.get_by_username(username)
            if user is None:
                error = '帳號或密碼錯誤。'
            elif not check_password_hash(user['password_hash'], password):
                error = '帳號或密碼錯誤。'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('登入成功！', 'success')
            return redirect(url_for('recipe.index'))

        flash(error, 'danger')

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """
    登出路由
    GET: 清除 session 資料並重導向至首頁
    """
    session.clear()
    flash('您已成功登出。', 'success')
    return redirect(url_for('recipe.index'))
