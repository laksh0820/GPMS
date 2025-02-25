from flask import Blueprint
citizen_bp = Blueprint('citizen',__name__,url_prefix='/citizen')

@citizen_bp.route('/')
def citizen_base():
    return "Hello, Citizen"

# Welfare Scheme (already benefitting, available/apply)
# Vaccination (already received, available)
# Taxes (File Income (monthly), Done, Due)
# Service Documents (apply for docs)

@citizen_bp.route('/welfare_scheme')
def welfare_scheme():
    pass

@citizen_bp.route('/vaccination')
def vaccination():
    pass

@citizen_bp.route('/taxes')
def taxes():
    pass

@citizen_bp.route('/service')
def service():
    pass