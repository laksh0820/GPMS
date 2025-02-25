from flask import Blueprint,redirect,url_for

admin_bp = Blueprint('admin',__name__,url_prefix='/admin')

@admin_bp.route('/')
def admin_base():
    return "Hello, System Admin"
