from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from Project.utils.db_utils import get_db_connection

# Flask-WTF form for updating status
class UpdateStatusForm(FlaskForm):
    submit = SubmitField('Mark as Paid')

employee_bp = Blueprint('employee', __name__, url_prefix='/employee', template_folder = 'templates')

@employee_bp.route('/')
@login_required
def employee_base():
    return render_template('employee_dashboard.html')

@employee_bp.route('/taxes', methods=['GET','POST'])
@login_required
def taxes():
    # check current_user type == employee
    table = "Overdue Taxes"
    columns = ['ID', 'Name', 'Tax Type', 'Tax Year', 'Amount Due (Rs)', 'Due Date', 'Status']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT tax_id, name, type, tax_year, amount_due, due_date, status
                FROM Taxes JOIN Citizen ON Taxes.citizen_id = Citizen.citizen_id
                WHERE status = 'Unpaid' AND due_date < CURRENT_DATE;
               """)
    
    form = UpdateStatusForm()
    if form.validate_on_submit():
        tax_id = request.form.get('tax_id')
        db.execute("""
                    UPDATE Taxes
                    SET status = 'Paid'
                    WHERE tax_id = %s;
                   """, [tax_id])
        conn.commit()
        db.close()
        conn.close()
        return redirect(url_for('employee.taxes'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Taxes', table_name = table, columns = columns, data = res, form = form)

@employee_bp.route('/welfare_schemes', methods=['GET','POST'])
@login_required
def welfare_schemes():
    # check current_user type == employee
    table = "Current Welfare Schemes"
    columns = ['Scheme Name', 'Description']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT name, description
                FROM Welfare_Scheme;
               """)
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Welfare Schemes', table_name = table, columns = columns, data = res)

@employee_bp.route('/vaccinations', methods=['GET','POST'])
@login_required
def vaccinations():
    # check current_user type == employee
    table = "Administered Vaccines"
    columns = ['Vaccine Type']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT DISTINCT vaccine_type
                FROM Vaccination;
               """)
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Vaccinations', table_name = table, columns = columns, data = res)

@employee_bp.route('/services', methods=['GET','POST'])
@login_required
def services():
    # check current_user type == employee
    table = ""
    columns = ['', '']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
               """)
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Services', table_name = table, columns = columns, data = res)

@employee_bp.route('/expenditures', methods=['GET','POST'])
@login_required
def expenditures():
    # check current_user type == employee
    table = ""
    columns = ['', '']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
               """)
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Expenditures', table_name = table, columns = columns, data = res)

@employee_bp.route('/assets', methods=['GET','POST'])
@login_required
def assets():
    # check current_user type == employee
    table = ""
    columns = ['', '']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
               """)
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Assets', table_name = table, columns = columns, data = res)

@employee_bp.route('/agriculture', methods=['GET','POST'])
@login_required
def agriculture():
    # check current_user type == employee
    table = ""
    columns = ['', '']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
               """)
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Agricultural Data', table_name = table, columns = columns, data = res)

@employee_bp.route('/census', methods=['GET','POST'])
@login_required
def census():
    # check current_user type == employee
    table = ""
    columns = ['', '']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
               """)
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Census Records', table_name = table, columns = columns, data = res)

@employee_bp.route('/environment', methods=['GET','POST'])
@login_required
def environment():
    # check current_user type == employee
    table = ""
    columns = ['', '']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
               """)
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Environmental Data', table_name = table, columns = columns, data = res)