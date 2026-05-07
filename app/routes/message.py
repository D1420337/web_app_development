from flask import Blueprint, render_template, request, redirect, url_for, flash, session

message_bp = Blueprint('message', __name__)

@message_bp.route('/book/<int:book_id>/message', methods=['POST'])
def add_message(book_id):
    """
    在書籍頁面新增公開留言。
    POST: 建立 Message 紀錄，重導向至書籍詳情頁。
    """
    pass

@message_bp.route('/message/<int:target_user_id>', methods=['GET'])
def private_messages(target_user_id):
    """
    私訊對話頁面。
    GET: 取得與 target_user_id 的私訊紀錄，渲染 messages.html。
    """
    pass

@message_bp.route('/message/<int:target_user_id>/send', methods=['POST'])
def send_private_message(target_user_id):
    """
    傳送私訊。
    POST: 建立私訊 Message 紀錄，重導向回對話頁面。
    """
    pass
