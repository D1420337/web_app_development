from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理使用者註冊。
    GET: 渲染註冊表單。
    POST: 接收資料，建立 User，重導向至登入。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'student')
        
        error = None
        if not username:
            error = '請輸入使用者名稱。'
        elif not email:
            error = '請輸入電子郵件。'
        elif not password:
            error = '請輸入密碼。'
            
        if error is None:
            # 檢查 email 是否已註冊
            existing_user = User.get_by_email(email)
            if existing_user:
                error = f'電子郵件 {email} 已經註冊過了。'
            else:
                password_hash = generate_password_hash(password)
                user_id = User.create(username, email, password_hash, role)
                if user_id:
                    flash('註冊成功！請登入。', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    error = '註冊失敗，發生資料庫錯誤。'
                    
        flash(error, 'danger')
        
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理使用者登入。
    GET: 渲染登入表單。
    POST: 驗證帳密，設定 session，重導向至首頁。
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        error = None
        user = User.get_by_email(email)
        
        if user is None:
            error = '找不到該電子郵件的帳號。'
        elif not check_password_hash(user['password_hash'], password):
            error = '密碼錯誤。'
            
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('登入成功！', 'success')
            return redirect(url_for('book.index'))
            
        flash(error, 'danger')
        
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """
    處理登出，清除 session，重導向至首頁。
    """
    session.clear()
    flash('您已經成功登出。', 'info')
    return redirect(url_for('book.index'))
