from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
import functools
from app.models.user import User

bp = Blueprint('admin', __name__)

def admin_required(view):
    """自訂驗證是否為管理員的裝飾器"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None or session.get('role') != 'admin':
            abort(403) # 拒絕存取
        return view(**kwargs)
    return wrapped_view

@bp.route('/')
@admin_required
def dashboard():
    """
    後台管理儀表板
    """
    return render_template('admin/dashboard.html')

@bp.route('/users')
@admin_required
def users():
    """
    使用者管理列表
    """
    all_users = User.get_all()
    return render_template('admin/users.html', users=all_users)
