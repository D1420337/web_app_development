from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.recipe import Recipe
import functools

bp = Blueprint('recipe', __name__)

def login_required(view):
    """自訂驗證是否已登入的裝飾器"""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            flash('此操作需要登入。', 'danger')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/')
@bp.route('/recipes')
def index():
    """
    首頁 / 食譜總覽路由
    GET: 取得食譜清單並渲染至 index.html
    """
    recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes, search_query="")

@bp.route('/recipes/search')
def search():
    """
    食譜搜尋路由
    GET: 根據 URL 參數 `q` 搜尋食譜，並攜帶結果渲染至 index.html
    """
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('recipe.index'))
    
    recipes = Recipe.search(query)
    return render_template('index.html', recipes=recipes, search_query=query)

@bp.route('/recipes/new', methods=('GET', 'POST'))
@login_required
def create():
    """
    新增食譜路由
    GET: 呈現空白的 form.html 表單
    POST: 接收表單內容並儲存入資料庫，成功後重導向至該食譜的詳情頁
    """
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        image_url = request.form.get('image_url', '')

        error = None
        if not title:
            error = 'Title is required.'
        elif not ingredients:
            error = 'Ingredients are required.'
        elif not steps:
            error = 'Steps are required.'

        if error is None:
            recipe_id = Recipe.create(session['user_id'], title, description, ingredients, steps, image_url)
            if recipe_id:
                flash('食譜成功新增！', 'success')
                return redirect(url_for('recipe.detail', recipe_id=recipe_id))
            else:
                error = '新增過程發生錯誤，請稍後再試。'
                
        flash(error, 'danger')

    return render_template('form.html', recipe=None)

@bp.route('/recipes/<int:recipe_id>')
def detail(recipe_id):
    """
    食譜詳情路由
    GET: 依據 recipe_id 取得單一食譜資料並渲染於 detail.html
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))
        
    return render_template('detail.html', recipe=recipe)

@bp.route('/recipes/<int:recipe_id>/edit', methods=('GET', 'POST'))
@login_required
def update(recipe_id):
    """
    編輯食譜路由
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))

    # 權限檢查：只有原作者或管理員可以編輯
    if recipe['user_id'] != session['user_id'] and session.get('role') != 'admin':
        flash('您沒有權限編輯此食譜。', 'danger')
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description', '')
        ingredients = request.form.get('ingredients')
        steps = request.form.get('steps')
        image_url = request.form.get('image_url', '')

        error = None
        if not title:
            error = 'Title is required.'
        elif not ingredients:
            error = 'Ingredients are required.'
        elif not steps:
            error = 'Steps are required.'

        if error is None:
            success = Recipe.update(recipe_id, title, description, ingredients, steps, image_url)
            if success:
                flash('食譜成功更新！', 'success')
                return redirect(url_for('recipe.detail', recipe_id=recipe_id))
            else:
                error = '更新過程發生錯誤，請稍後再試。'

        flash(error, 'danger')

    return render_template('form.html', recipe=recipe)

@bp.route('/recipes/<int:recipe_id>/delete', methods=('POST',))
@login_required
def delete(recipe_id):
    """
    刪除食譜路由
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))

    # 權限檢查：只有原作者或管理員可以刪除
    if recipe['user_id'] != session['user_id'] and session.get('role') != 'admin':
        flash('您沒有權限刪除此食譜。', 'danger')
        return redirect(url_for('recipe.detail', recipe_id=recipe_id))
        
    success = Recipe.delete(recipe_id)
    if success:
        flash('食譜已成功刪除。', 'success')
    else:
        flash('刪除過程發生錯誤，請稍後再試。', 'danger')
        
    return redirect(url_for('recipe.index'))
