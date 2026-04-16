# This file makes app/routes/ a python package.
from .auth import bp as auth_bp
from .recipe import bp as recipe_bp
from .admin import bp as admin_bp

def register_blueprints(app):
    """
    註冊所有的路由模組到 Flask application 中
    """
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipe_bp)  # 沒有 URL prefix 這樣食譜就能在根目錄 / 呈現
    app.register_blueprint(admin_bp, url_prefix='/admin')
