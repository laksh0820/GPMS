from flask import Blueprint
citizen_bp = Blueprint('citizen',__name__,url_prefix='/citizen')

@citizen_bp.route('/')
def citizen_base():
    return "Hello, Citizen"