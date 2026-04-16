from flask import Blueprint, render_template, request, redirect, url_for, flash

bp = Blueprint('recipe', __name__)

@bp.route('/')
@bp.route('/recipes')
def index():
    """
    首頁 / 食譜總覽路由
    GET: 取得食譜清單並渲染至 index.html
    """
    pass

@bp.route('/recipes/search')
def search():
    """
    食譜搜尋路由
    GET: 根據 URL 參數 `q` 搜尋食譜，並攜帶結果渲染至 index.html
    """
    pass

@bp.route('/recipes/new', methods=('GET', 'POST'))
def create():
    """
    新增食譜路由
    需要驗證登入。
    GET: 呈現空白的 form.html 表單
    POST: 接收表單內容並儲存入資料庫，成功後重導向至該食譜的詳情頁
    """
    pass

@bp.route('/recipes/<int:recipe_id>')
def detail(recipe_id):
    """
    食譜詳情路由
    GET: 依據 recipe_id 取得單一食譜資料並渲染於 detail.html
    若找不到該ID則返回 404
    """
    pass

@bp.route('/recipes/<int:recipe_id>/edit', methods=('GET', 'POST'))
def update(recipe_id):
    """
    編輯食譜路由
    需要驗證登入以及檢查該食譜是否屬於目前使用者或為管理員。
    GET: 渲染 form.html 並將原有食譜資料預填至表單中
    POST: 接收更新後的資料並寫入資料庫，成功後重導向至食譜詳情頁
    """
    pass

@bp.route('/recipes/<int:recipe_id>/delete', methods=('POST',))
def delete(recipe_id):
    """
    刪除食譜路由
    需要驗證登入與作者權限。
    POST: 自資料庫中刪除該紀錄，完成後重導向至首頁
    """
    pass
