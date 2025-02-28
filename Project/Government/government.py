from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user,login_required,current_user,logout_user
from flask_wtf import FlaskForm
from Project.utils.db_utils import get_db_connection
government_bp = Blueprint('government',__name__,url_prefix='/government', template_folder='templates', static_folder='static')

def government_monitor_required(inner_func):
    def wrapped_function_government_monitor(*args,**kwargs):
        if current_user.is_authenticated and current_user.role != 'government' and current_user.role != 'admin':
            flash("Please log in as Government Monitor to access this page",'error')
            return redirect(url_for(f'{current_user.role}.base'))
        return inner_func(*args,**kwargs)
    wrapped_function_government_monitor.__name__ = inner_func.__name__
    return wrapped_function_government_monitor

@government_bp.route('/refresh_agricultural_data')
@login_required
@government_monitor_required
def refresh_agricultural_data():
    conn = get_db_connection()
    db = conn.cursor()

    # Gather Information of Land covered by each crop type and Average Land covered by each crop type
    db.execute("""
                SELECT crop_type, avg(area_acres), sum(area_acres)
                FROM land_record
                GROUP BY crop_type;
            """)
    res = db.fetchall()

    # Extracting relevant information
    crop_type = [row[0] for row in res]
    avg_area_acres = [row[1] for row in res]
    total_area_acres = [row[2] for row in res]


    # Gather Information of Average Land covered by a citizen in the village
    db.execute("""
                SELECT avg(area_acres)
                FROM land_record;
            """)
    res = db.fetchall()
    avg_area_acres_per_citizen = res[0][0]
    

    # Gather Information of average income of a farmer in the village
    db.execute("""
                SELECT avg(income)
                FROM citizen JOIN land_record USING (citizen_id);
                """)
    res = db.fetchall()
    avg_income_per_farmer = res[0][0]


    db.close()
    conn.close()

    return jsonify({'crop_type':crop_type,
                    'avg_area_acres':avg_area_acres,
                    'total_area_acres':total_area_acres,
                    'avg_area_acres_per_citizen':avg_area_acres_per_citizen,
                    'avg_income_per_farmer':avg_income_per_farmer})
    


@government_bp.route('/')
@login_required
@government_monitor_required
def base():
    conn = get_db_connection()
    db = conn.cursor()

    # Gather Information of Land covered by each crop type and Average Land covered by each crop type
    db.execute("""
                SELECT crop_type, avg(area_acres), sum(area_acres)
                FROM land_record
                GROUP BY crop_type;
                """)
    res = db.fetchall()

    # Extracting relevant information
    crop_type = [row[0] for row in res]
    avg_area_acres = [row[1] for row in res]
    total_area_acres = [row[2] for row in res]


    # Gather Information of Average Land covered by a citizen in the village
    db.execute("""
                SELECT avg(area_acres)
                FROM land_record;
                """)
    res = db.fetchall()
    avg_area_acres_per_citizen = res[0][0]
    

    # Gather Information of average income of a farmer in the village
    db.execute("""
                SELECT avg(income)
                FROM citizen JOIN land_record USING (citizen_id);
                """)
    res = db.fetchall()
    avg_income_per_farmer = res[0][0]

    db.close()
    conn.close()

    return render_template('Government/dashboard.html', 
                           crop_type=crop_type, 
                           avg_area_acres=avg_area_acres, 
                           total_area_acres=total_area_acres, 
                           avg_area_acres_per_citizen=avg_area_acres_per_citizen,
                           avg_income_per_farmer=avg_income_per_farmer)