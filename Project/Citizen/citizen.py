from flask import Blueprint,render_template,flash,redirect,url_for,request
from flask_login import login_required,current_user
from Project.utils.db_utils import get_db_connection

citizen_bp = Blueprint('citizen',__name__,url_prefix='/citizen', template_folder='templates',static_folder='static')

# Wrapper to ensure only citizen can access the page
def citizen_required(inner_func):
    def wrapped_function_citizen(*args,**kwargs):
        if (current_user.is_authenticated) and (current_user.role != 'citizen' and current_user.role != 'admin'):
            flash("Please log in as Citizen to access this page",'error')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapped_function_citizen.__name__ = inner_func.__name__
    return wrapped_function_citizen

# Wrapper to ensure that the user in verified
def verification_required(inner_func):
    def wrapper(*args,**kwargs):
        if current_user.is_verified == False:
            flash("Please wait for 24 hours until Admin verifies you",'warning')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapper.__name__ = inner_func.__name__
    return wrapper

# Dashboard for citizen
@citizen_bp.route('/')
@login_required
@citizen_required
# @verification_required
def base():
    return render_template('dashboard.html')

# Welfare Schemes
@citizen_bp.route('/welfare_scheme')
@login_required
@citizen_required
# @verification_required
def welfare_scheme():
    request_type = request.args.get('request_type')
    
    scheme_title = []
    scheme_description = []
    enrollment_date = []
    
    if request_type == 'Active':
        conn = get_db_connection()
        db = conn.cursor()
        
        db.execute("""
                SELECT name,description
                from welfare_scheme;
                """)
        res = db.fetchall()
        
        scheme_title = [row[0] for row in res]
        scheme_description = [row[1] for row in res] 
        
        db.close()
        conn.close()
    else:
        conn = get_db_connection()
        db = conn.cursor()
        
        db.execute("""
                SELECT name,description,enrollment_date
                FROM welfare_scheme natural join scheme_enrollment
                WHERE citizen_id = %s;
                """,[current_user.citizen_id])
        res = db.fetchall()
        
        scheme_title = [row[0] for row in res]
        scheme_description = [row[1] for row in res] 
        enrollment_date = [row[2] for row in res]
        
        db.close()
        conn.close()
        
    return render_template('welfare_scheme.html',scheme_title=scheme_title,scheme_description=scheme_description,
                                                enrollment_date=enrollment_date,request_type=request_type)

# Vaccinations 
@citizen_bp.route('/vaccination')
@login_required
@citizen_required
# @verification_required
def vaccination():
    request_type = request.args.get('request_type')
    
    vaccine_type = []
    centers = []
    date_administered = []
    
    if request_type == 'Active':
        conn = get_db_connection()
        db = conn.cursor()
        
        db.execute("""
                    SELECT vaccine_type, centers
                    from vaccines;
                """)
        
        res = db.fetchall()
        vaccine_type = [row[0] for row in res]
        center = [row[1] for row in res]
        
        db.close()
        conn.close()
    else:
        conn = get_db_connection()
        db = conn.cursor()
        
        db.execute("""
                    SELECT vaccine_type, centers, date_administered
                    FROM vaccines natural join vaccination
                    WHERE citizen_id = %s;
                """,[current_user.citizen_id])
        
        res = db.fetchall()
        vaccine_type = [row[0] for row in res]
        centers = [row[1] for row in res]
        date_administered = [row[2] for row in res]
        
        db.close()
        conn.close()
    
    return render_template('vaccination.html',vaccine_type=vaccine_type,centers=centers,
                           date_administered=date_administered,request_type=request_type)

# Taxes
@citizen_bp.route('/taxes')
@login_required
@citizen_required
# @verification_required
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
# @verification_required
def service():
    conn = get_db_connection()
    db = conn.cursor()
    
    db.execute("""
               SELECT issue_date,doc_type,description
               FROM service natural join documents
               WHERE citizen_id = %s;
            """,[current_user.citizen_id])
    res = db.fetchall()
    issue_date = [row[0] for row in res]
    doc_type = [row[1] for row in res]
    description = [row[2] for row in res]
    
    db.close()
    conn.close()
    return render_template('service.html',issue_date=issue_date,doc_type=doc_type,description=description)