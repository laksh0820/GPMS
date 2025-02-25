from flask import Blueprint, render_template
government_bp = Blueprint('government',__name__,url_prefix='/government', template_folder='templates')

@government_bp.route('/')
def govenrment_base():
    return render_template('government_dashboard.html')
    return "Hello, Government Monitor"
