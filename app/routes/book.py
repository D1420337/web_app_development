from flask import Blueprint, render_template, request, redirect, url_for, flash, session

book_bp = Blueprint('book', __name__)

@book_bp.route('/', methods=['GET'])
def index():
    """
    首頁/書籍列表。
    GET: 取得所有上架書籍，支援搜尋與過濾，渲染 index.html。
    """
    pass

@book_bp.route('/book/create', methods=['GET', 'POST'])
def create():
    """
    新增書籍上架。
    GET: 渲染上架表單。
    POST: 接收表單資料，呼叫 Book.create()，重導向至個人書櫃。
    """
    pass

@book_bp.route('/book/<int:book_id>', methods=['GET'])
def detail(book_id):
    """
    書籍詳細資訊。
    GET: 根據 book_id 取得書籍與留言，渲染 detail.html。
    """
    pass

@book_bp.route('/book/<int:book_id>/edit', methods=['GET', 'POST'])
def edit(book_id):
    """
    編輯書籍。
    GET: 顯示編輯表單。
    POST: 更新書籍資料，重導向至詳情頁。
    需驗證是否為擁有者。
    """
    pass

@book_bp.route('/book/<int:book_id>/delete', methods=['POST'])
def delete(book_id):
    """
    刪除書籍。
    POST: 刪除書籍，重導向至個人書櫃。
    需驗證是否為擁有者。
    """
    pass
