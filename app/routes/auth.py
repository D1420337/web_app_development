from flask import Blueprint, render_template, request, redirect, url_for, flash, session

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    註冊路由
    GET: 渲染 auth/register.html 表單
    POST: 接收 username, password，成功建立後重導向至登入頁面
    """
    pass

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    登入路由
    GET: 渲染 auth/login.html 表單
    POST: 接收並驗證 username, password，成功時寫入 session 並重導向首頁
    """
    pass

@bp.route('/logout')
def logout():
    """
    登出路由
    GET: 清除 session 資料並重導向至首頁
    """
    pass
