from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

bp = Blueprint('admin', __name__)

@bp.route('/')
def dashboard():
    """
    後台管理儀表板
    需要驗證 session 與使用者權限(role == 'admin')，否則拋出 403 錯誤
    GET: 呈現 admin/dashboard.html
    """
    pass

@bp.route('/users')
def users():
    """
    使用者管理列表
    需要驗證 session 與管理者權限(role == 'admin')，否則拋出 403 錯誤
    GET: 從資料庫取得所有使用者紀錄，並渲染 admin/users.html
    """
    pass
