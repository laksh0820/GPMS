from flask import Blueprint,render_template,flash,redirect,url_for,request
from flask_login import login_required,current_user
from Project.utils.db_utils import get_db_connection

admin_bp = Blueprint('admin',__name__,url_prefix='/admin',template_folder='templates',static_folder='static')


# Wrapper to ensure only admin can access the page
def admin_required(inner_func):
    def wrapped_function_admin(*args,**kwargs):
        if (current_user.is_authenticated) and (current_user.role != 'admin'):
            flash("Please log in as admin to access this page",'error')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapped_function_admin.__name__ = inner_func.__name__
    return wrapped_function_admin

# Wrapper to ensure that the user in verified
def verification_required(inner_func):
    def wrapper(*args,**kwargs):
        if current_user.is_verified == False:
            flash("Please wait for 24 hours until Admin verifies you",'warning')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapper.__name__ = inner_func.__name__
    return wrapper




# Dashboard for admin
@admin_bp.route('/')
@login_required
@admin_required
def base():
    return render_template('admin_dashboard.html')


# Approve users
@login_required
@admin_required
@admin_bp.route('/approve')
def approve():
    conn = get_db_connection()
    db = conn.cursor()
    
    db.execute("""
            SELECT email,citizen_id,role
            FROM users
            WHERE is_verified = FALSE;
            """)
    res = db.fetchall()
    
    email = [row[0] for row in res]
    citizen_id = [row[1] for row in res]
    role = [row[2] for row in res]
    
    db.close()
    
    return render_template('approve.html',email=email,citizen_id=citizen_id,role=role)