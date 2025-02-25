from flask import Blueprint
employee_bp = Blueprint('employee',__name__,url_prefix='/employee')

@employee_bp.route('/')
def employee_base():
    return "Hello, Employee"