from flask import Blueprint,render_template,flash,redirect,url_for
from flask_login import login_required,current_user
from Project.utils.db_utils import get_db_connection

citizen_bp = Blueprint('citizen',__name__,url_prefix='/citizen', template_folder='templates')

def citizen_required(inner_func):
    def wrapped_function_citizen(*args,**kwargs):
        if (current_user.is_authenticated) and (current_user.role != 'citizen' and current_user.role != 'admin'):
            flash("Please log in as Citizen to access this page",'error')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapped_function_citizen.__name__ = inner_func.__name__
    return wrapped_function_citizen

# Dashboard for citizen
@citizen_bp.route('/')
@login_required
@citizen_required
def base():
    return render_template('dashboard.html')

# Welfare Schemes
@citizen_bp.route('/welfare_scheme')
@login_required
@citizen_required
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

# Vaccinations 
@citizen_bp.route('/vaccination')
@login_required
@citizen_required
def vaccination():
    conn = get_db_connection()
    db = conn.cursor()
    
    db.execute("""
                SELECT vaccine_type, date_administered
                from vaccination
                where citizen_id = %s;
            """,[current_user.citizen_id])
    
    res = db.fetchall()
    vaccination_type = [row[0] for row in res]
    date_administered = [row[1] for row in res]
    
    db.close()
    conn.close()
    return render_template('vaccination.html',vaccination_type=vaccination_type,date_administered=date_administered)

# Taxes
@citizen_bp.route('/taxes')
@login_required
@citizen_required
def taxes():
    conn = get_db_connection()
    db = conn.cursor()
    
    db.execute("""
               SELECT type,tax_year,amount_due,due_date,status
               FROM taxes
               WHERE citizen_id = %s;
            """,[current_user.citizen_id])
    
    res = db.fetchall()
    tax_type = [row[0] for row in res]
    tax_year = [row[1] for row in res]
    amount_due = [row[2] for row in res]
    due_date = [row[3] for row in res]
    status = [row[4] for row in res]
    
    db.close()
    conn.close()
    return render_template('taxes.html',tax_type=tax_type,tax_year=tax_year,amount_due=amount_due,due_date=due_date,status=status)

# Services
@citizen_bp.route('/service')
@login_required
@citizen_required
def service():
    return render_template('service.html')