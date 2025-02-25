from flask import Blueprint
employee_bp = Blueprint('employee',__name__,url_prefix='/employee', template_folder='templates')

@employee_bp.route('/')
def employee_base():
    return "Hello, Employee"

@employee_bp.route('/welfare_schemes')
def welfare_scheme():
    pass

@employee_bp.route('/vaccinations')
def vaccinations():
    pass
