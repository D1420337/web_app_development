from flask import Blueprint, render_template, request, redirect, url_for, flash, session

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """
    個人書櫃。
    GET: 取得該使用者的上架清單、預約狀態，渲染 dashboard.html。
    """
    pass

@user_bp.route('/request/<int:req_id>/action', methods=['POST'])
def handle_request(req_id):
    """
    賣家處理預約請求。
    POST: 接收 action (accept/reject)，更新 Request 與 Book 狀態。
    """
    pass

@user_bp.route('/book/<int:book_id>/request', methods=['POST'])
def make_request(book_id):
    """
    買家發送預約請求。
    POST: 建立 Request 紀錄，重導向至書籍詳情。
    """
    pass
