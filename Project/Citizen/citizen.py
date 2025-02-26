from flask import Blueprint,render_template
from flask_login import login_required
from Project.utils.db_utils import get_db_connection

citizen_bp = Blueprint('citizen',__name__,url_prefix='/citizen', template_folder='templates')

# Welfare Scheme (already benefitting, available/apply)
# Vaccination (already received, available)
# Taxes (File Income (monthly), Done, Due)
# Service Documents (apply for docs)

@citizen_bp.route('/')
@login_required
def base():
    return render_template('dashboard.html')

@citizen_bp.route('/welfare_scheme')
@login_required
def welfare_scheme():
    conn = get_db_connection()
    db = conn.cursor()
    
    db.execute("""
               SELECT * 
               from welfare_scheme;
            """)
    res = db.fetchall()
    
    scheme_title = [row[1] for row in res]
    scheme_description = [row[2] for row in res] 
    
    db.close()
    conn.close()
    return render_template('welfare_scheme.html',scheme_title=scheme_title,scheme_description=scheme_description)

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