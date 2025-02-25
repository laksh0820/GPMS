from flask import Blueprint
employee_bp = Blueprint('employee',__name__,url_prefix='/employee')

@employee_bp.route('/')
def employee_base():
    return "Hello, Employee"

@employee_bp.route('/welfare_schemes')
def welfare_scheme():
    pass

@employee_bp.route('/vaccinations',method=['GET','POST'])
def vaccinations():
    pass
