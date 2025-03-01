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

# Dashboard for admin
@admin_bp.route('/')
@login_required
@admin_required
def base():
    return render_template('admin_dashboard.html')

# Approve users
@admin_bp.route('/approve')
@login_required
@admin_required
def approve():
    conn = get_db_connection()
    db = conn.cursor()
    
    db.execute("""
            SELECT email,id,role
            FROM users
            WHERE is_verified = FALSE;
            """)
    res = db.fetchall()
    
    email = [row[0] for row in res]
    user_id = [row[1] for row in res]
    role = [row[2] for row in res]
    
    db.close()
    
    return render_template('approve.html',email=email,user_id=user_id,role=role)

# Handle the post request for approving users
@admin_bp.route('/approve',methods=['POST'])
@login_required
@admin_required
def approve_post():
    conn = get_db_connection()
    db = conn.cursor()
    
    id = request.form['user_id']
    action = request.form['action']
    
    if action == 'Reject':
        db.execute("""
                    DELETE FROM users
                    WHERE id = %s;
                    """,[id])
        
    else:
        db.execute("""
                    UPDATE users
                    SET is_verified = TRUE
                    WHERE id = %s;
                    """,[id])
    
    conn.commit()
    db.close()
    conn.close()
    
    if action=='Approve':
        flash("Approved Successfully")
    else:
        flash("Rejected Successfully")
        
    
    return redirect(url_for('admin.approve'))