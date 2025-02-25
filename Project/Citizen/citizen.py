from flask import Blueprint,render_template
from flask_login import login_required
citizen_bp = Blueprint('citizen',__name__,url_prefix='/citizen',template_folder='templates')

# Welfare Scheme (already benefitting, available/apply)
# Vaccination (already received, available)
# Taxes (File Income (monthly), Done, Due)
# Service Documents (apply for docs)

@citizen_bp.route('/')
@login_required
def base():
    return "Hello, Citizen"

@citizen_bp.route('/welfare_scheme')
@login_required
def welfare_scheme():
    return render_template('welfare_scheme.html')

@citizen_bp.route('/vaccination')
@login_required
def vaccination():
    return render_template('vaccination.html')

@citizen_bp.route('/taxes')
@login_required
def taxes():
    return render_template('taxes.html')

@citizen_bp.route('/service')
@login_required
def service():
    return render_template('service.html')