from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染註冊表單。
    POST: 接收資料，建立 User，重導向至登入。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染登入表單。
    POST: 驗證帳密，設定 session，重導向至首頁。
    """
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    處理登出，清除 session，重導向至首頁。
    """
    pass
