from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField
from Project.utils.db_utils import get_db_connection

employee_bp = Blueprint('employee', __name__, url_prefix='/employee', template_folder = 'templates', static_folder='static')

class UpdateStatusForm(FlaskForm):
    submit = SubmitField('Mark as Paid')

class SaveForm(FlaskForm):
    submit = SubmitField('Save All')

def employee_required(inner_func):
    def wrapped_function_employee(*args,**kwargs):
        if (current_user.is_authenticated) and (current_user.role != 'employee' and current_user.role != 'admin'):
            flash("Please log in as Panchayat Employee to access this page",'error')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapped_function_employee.__name__ = inner_func.__name__
    return wrapped_function_employee

# Wrapper to ensure that the user in verified
def verification_required(inner_func):
    def wrapper(*args,**kwargs):
        if current_user.is_verified == False:
            flash("Please wait for 24 hours until Admin verifies you",'warning')
            return redirect(url_for('base'))
        return inner_func(*args,**kwargs)
    wrapper.__name__ = inner_func.__name__
    return wrapper

@employee_bp.route('/')
@login_required
@employee_required
@verification_required
def base():
    return render_template('employee_dashboard.html')

@employee_bp.route('/taxes', methods=['GET','POST'])
@login_required
@employee_required
@verification_required
def taxes():
    table = "Overdue Taxes"
    columns = ['ID', 'Name', 'Tax Type', 'Tax Month', 'Tax Year', 'Amount Due (Rs)', 'Due Date', 'Status']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT tax_id, name, type, tax_month, tax_year, amount_due, due_date, status
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
@employee_required
@verification_required
def welfare_schemes():
    table = "Current Welfare Schemes"
    columns = ['S. no.', 'Scheme Name', 'Description']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT *
                FROM Welfare_Scheme;
               """)

    form = SaveForm()
    if form.validate_on_submit():
        error = False
        # Process existing rows
        for key, value in request.form.items():
            if key.startswith('index_') and not key.startswith('index_new_') and not key.startswith('index_del_'):
                row_id = key.split('_')[1]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_{row_id}_{i}'))
                temp_list.append(request.form.get(key))
                try:
                    db.execute("""
                                UPDATE Welfare_Scheme
                                SET name = %s, description = %s
                                WHERE scheme_id = %s;
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        # Process new rows
        for key, value in request.form.items():
            if key.startswith('index_new_'):
                row_id = key.split('_')[2]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_new_{row_id}_{i}'))
                try:
                    db.execute("""
                                INSERT INTO Welfare_Scheme
                                VALUES (DEFAULT, %s, %s);
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True
        
        # Delete marked rows
        for key, value in request.form.items():
            if key.startswith('index_del_'):
                id = request.form.get(key)
                try:
                    db.execute("""
                                DELETE FROM Welfare_Scheme
                                WHERE scheme_id = %s;
                               """, [id])
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        db.close()
        conn.close()
        if error: flash("Invalid entries",'error')
        return redirect(url_for('employee.welfare_schemes'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Welfare Schemes', table_name = table, columns = columns, data = res, form = form)

@employee_bp.route('/vaccinations', methods=['GET','POST'])
@login_required
@employee_required
@verification_required
def vaccinations():
    table = "Available Vaccines"
    columns = ['S. no.', 'Vaccine Type', 'Centers']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT *
                FROM Vaccines;
               """)

    form = SaveForm()
    if form.validate_on_submit():
        error = False
        # Process existing rows
        for key, value in request.form.items():
            if key.startswith('index_') and not key.startswith('index_new_') and not key.startswith('index_del_'):
                row_id = key.split('_')[1]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_{row_id}_{i}'))
                temp_list.append(request.form.get(key))
                try:
                    db.execute("""
                                UPDATE Vaccines
                                SET vaccine_type = %s, centers = %s
                                WHERE vaccine_id = %s;
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        # Process new rows
        for key, value in request.form.items():
            if key.startswith('index_new_'):
                row_id = key.split('_')[2]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_new_{row_id}_{i}'))
                try:
                    db.execute("""
                                INSERT INTO Vaccines
                                VALUES (DEFAULT, %s, %s);
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True
        
        # Delete marked rows
        for key, value in request.form.items():
            if key.startswith('index_del_'):
                id = request.form.get(key)
                try:
                    db.execute("""
                                DELETE FROM Vaccines
                                WHERE vaccine_id = %s;
                               """, [id])
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        db.close()
        conn.close()
        if error: flash("Invalid entries",'error')
        return redirect(url_for('employee.vaccinations'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Vaccinations', table_name = table, columns = columns, data = res, form = form)

@employee_bp.route('/services', methods=['GET','POST'])
@login_required
@employee_required
@verification_required
def services():
    table = "Official Document Services"
    columns = ['S. no.', 'Document Type', 'Description']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT *
                FROM Service;
               """)

    form = SaveForm()
    if form.validate_on_submit():
        error = False
        # Process existing rows
        for key, value in request.form.items():
            if key.startswith('index_') and not key.startswith('index_new_') and not key.startswith('index_del_'):
                row_id = key.split('_')[1]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_{row_id}_{i}'))
                temp_list.append(request.form.get(key))
                try:
                    db.execute("""
                                UPDATE Service
                                SET doc_type = %s, description = %s
                                WHERE doc_id = %s;
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        # Process new rows
        for key, value in request.form.items():
            if key.startswith('index_new_'):
                row_id = key.split('_')[2]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_new_{row_id}_{i}'))
                try:
                    db.execute("""
                                INSERT INTO Service
                                VALUES (DEFAULT, %s, %s);
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True
        
        # Delete marked rows
        for key, value in request.form.items():
            if key.startswith('index_del_'):
                id = request.form.get(key)
                try:
                    db.execute("""
                                DELETE FROM Service
                                WHERE doc_id = %s;
                               """, [id])
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        db.close()
        conn.close()
        if error: flash("Invalid entries",'error')
        return redirect(url_for('employee.services'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Services', table_name = table, columns = columns, data = res, form = form)

@employee_bp.route('/expenditures', methods=['GET','POST'])
@login_required
@employee_required
@verification_required
def expenditures():
    table = "Panchayat Expenditures"
    columns = ['S. no.', 'Expense Type', 'Description']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT *
                FROM Expenditures;
               """)

    form = SaveForm()
    if form.validate_on_submit():
        error = False
        # Process existing rows
        for key, value in request.form.items():
            if key.startswith('index_') and not key.startswith('index_new_') and not key.startswith('index_del_'):
                row_id = key.split('_')[1]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_{row_id}_{i}'))
                temp_list.append(request.form.get(key))
                try:
                    db.execute("""
                                UPDATE Expenditures
                                SET expense_type = %s, description = %s
                                WHERE bill_id = %s;
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        # Process new rows
        for key, value in request.form.items():
            if key.startswith('index_new_'):
                row_id = key.split('_')[2]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_new_{row_id}_{i}'))
                try:
                    db.execute("""
                                INSERT INTO Expenditures
                                VALUES (DEFAULT, %s, %s);
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True
        
        # Delete marked rows
        for key, value in request.form.items():
            if key.startswith('index_del_'):
                id = request.form.get(key)
                try:
                    db.execute("""
                                DELETE FROM Expenditures
                                WHERE bill_id = %s;
                               """, [id])
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        db.close()
        conn.close()
        if error: flash("Invalid entries",'error')
        return redirect(url_for('employee.expenditures'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Expenditures', table_name = table, columns = columns, data = res, form = form)

@employee_bp.route('/assets', methods=['GET','POST'])
@login_required
@employee_required
@verification_required
def assets():
    table = "Panchayat Owned Assets"
    columns = ['S. no.', 'Asset Type', 'Location', 'Installation Date']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT *
                FROM Asset;
               """)

    form = SaveForm()
    if form.validate_on_submit():
        error = False
        # Process existing rows
        for key, value in request.form.items():
            if key.startswith('index_') and not key.startswith('index_new_') and not key.startswith('index_del_'):
                row_id = key.split('_')[1]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_{row_id}_{i}'))
                temp_list.append(request.form.get(key))
                try:
                    db.execute("""
                                UPDATE Asset
                                SET type = %s, location = %s, installation_date = %s
                                WHERE asset_id = %s;
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        # Process new rows
        for key, value in request.form.items():
            if key.startswith('index_new_'):
                row_id = key.split('_')[2]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_new_{row_id}_{i}'))
                try:
                    db.execute("""
                                INSERT INTO Asset
                                VALUES (DEFAULT, %s, %s, %s);
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True
        
        # Delete marked rows
        for key, value in request.form.items():
            if key.startswith('index_del_'):
                id = request.form.get(key)
                try:
                    db.execute("""
                                DELETE FROM Asset
                                WHERE asset_id = %s;
                               """, [id])
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        db.close()
        conn.close()
        if error: flash("Invalid entries",'error')
        return redirect(url_for('employee.assets'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Assets', table_name = table, columns = columns, data = res, form = form)

@employee_bp.route('/census', methods=['GET','POST'])
@login_required
@employee_required
@verification_required
def census():
    table = "Village Census Data"
    columns = ['S. no.', 'Year', 'Male Population', 'Female Population', 'Male Births', 'Female Births', 'Male Deaths', 'Female Deaths', 'Marriages']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT *
                FROM Census_Data;
               """)

    form = SaveForm()
    if form.validate_on_submit():
        error = False
        # Process existing rows
        for key, value in request.form.items():
            if key.startswith('index_') and not key.startswith('index_new_') and not key.startswith('index_del_'):
                row_id = key.split('_')[1]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_{row_id}_{i}'))
                temp_list.append(request.form.get(key))
                try:
                    db.execute("""
                                UPDATE Census_Data
                                SET year = %s, population_male = %s, population_female = %s, births_male = %s, births_female = %s, deaths_male = %s, deaths_female = %s, marriages = %s
                                WHERE data_id = %s;
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        # Process new rows
        for key, value in request.form.items():
            if key.startswith('index_new_'):
                row_id = key.split('_')[2]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_new_{row_id}_{i}'))
                try:
                    db.execute("""
                                INSERT INTO Census_Data
                                VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s);
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True
        
        # Delete marked rows
        for key, value in request.form.items():
            if key.startswith('index_del_'):
                id = request.form.get(key)
                try:
                    db.execute("""
                                DELETE FROM Census_Data
                                WHERE data_id = %s;
                               """, [id])
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        db.close()
        conn.close()
        if error: flash("Invalid entries",'error')
        return redirect(url_for('employee.census'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Census Records', table_name = table, columns = columns, data = res, form = form)

@employee_bp.route('/environment', methods=['GET','POST'])
@login_required
@employee_required
@verification_required
def environment():
    table = "Environmental Pollution Measures"
    columns = ['S. no.', 'Date', 'Air Quality Index', 'Water Quality', 'Sanitation']
    conn = get_db_connection()
    db = conn.cursor()
    db.execute("""
                SELECT *
                FROM Environmental_Data;
               """)

    form = SaveForm()
    if form.validate_on_submit():
        error = False
        # Process existing rows
        for key, value in request.form.items():
            if key.startswith('index_') and not key.startswith('index_new_') and not key.startswith('index_del_'):
                row_id = key.split('_')[1]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_{row_id}_{i}'))
                temp_list.append(request.form.get(key))
                try:
                    db.execute("""
                                UPDATE Environmental_Data
                                SET date = %s, air_quality_index = %s, water_quality = %s, sanitation = %s
                                WHERE data_id = %s;
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        # Process new rows
        for key, value in request.form.items():
            if key.startswith('index_new_'):
                row_id = key.split('_')[2]
                temp_list = []
                for i in range(2, len(columns) + 1):
                    temp_list.append(request.form.get(f'item_new_{row_id}_{i}'))
                try:
                    db.execute("""
                                INSERT INTO Environmental_Data
                                VALUES (DEFAULT, %s, %s, %s, %s);
                               """, temp_list)
                    conn.commit()
                except:
                    conn.rollback()
                    error = True
        
        # Delete marked rows
        for key, value in request.form.items():
            if key.startswith('index_del_'):
                id = request.form.get(key)
                try:
                    db.execute("""
                                DELETE FROM Environmental_Data
                                WHERE data_id = %s;
                               """, [id])
                    conn.commit()
                except:
                    conn.rollback()
                    error = True

        db.close()
        conn.close()
        if error: flash("Invalid entries",'error')
        return redirect(url_for('employee.environment'))
    
    res = db.fetchall()
    db.close()
    conn.close()
    return render_template('employee_content.html', page = 'Environmental Data', table_name = table, columns = columns, data = res, form = form)