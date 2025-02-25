from flask import Blueprint
government_bp = Blueprint('government',__name__,url_prefix='/government',template_folder='templates')

@government_bp.route('/')
def govenrment_base():
    return "Hello, Government Monitor"
