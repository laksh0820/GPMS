from flask import Blueprint,render_template,flash,redirect,url_for,request
from flask_login import login_required,current_user
from Project.utils.db_utils import get_db_connection
from wtforms import SubmitField
from flask_wtf import FlaskForm
from datetime import datetime

citizen_bp = Blueprint('citizen',__name__,url_prefix='/citizen', template_folder='templates',static_folder='static')

class RequestForm(FlaskForm):
    submit = SubmitField('Enroll')

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
@verification_required
def base():
    return render_template('dashboard.html')

# Welfare Schemes
@citizen_bp.route('/welfare_scheme',methods=['GET','POST'])
@login_required
@citizen_required
@verification_required
def welfare_scheme():
    form = RequestForm()
    
    if request.method == 'GET':
        request_type = request.args.get('request_type')
        
        scheme_id = []
        scheme_title = []
        scheme_description = []
        enrollment_date = []
        
        if request_type == 'Active':
            conn = get_db_connection()
            db = conn.cursor()
            
            if current_user.role == 'citizen':
                db.execute("""
                    (SELECT scheme_id,name,description
                    from welfare_scheme)
                    except
                    (SELECT scheme_id,name,description
                    FROM welfare_scheme natural join scheme_enrollment);
                    """)
            elif current_user.role == 'admin':
                db.execute("""
                    (SELECT scheme_id,name,description
                    from welfare_scheme);
                    """)
            res = db.fetchall()
            
            scheme_id = [row[0] for row in res]
            scheme_title = [row[1] for row in res]
            scheme_description = [row[2] for row in res] 
            
            db.close()
            conn.close()
        else:
            conn = get_db_connection()
            db = conn.cursor()
            
            db.execute("""
                    SELECT scheme_id,name,description,enrollment_date
                    FROM welfare_scheme natural join scheme_enrollment
                    WHERE citizen_id = %s;
                    """,[current_user.citizen_id])
            res = db.fetchall()
            
            scheme_id = [row[0] for row in res]
            scheme_title = [row[1] for row in res]
            scheme_description = [row[2] for row in res] 
            enrollment_date = [row[3] for row in res]
            
            db.close()
            conn.close()
            
        return render_template('welfare_scheme.html',scheme_id=scheme_id,scheme_title=scheme_title,scheme_description=scheme_description,
                                                    enrollment_date=enrollment_date,request_type=request_type,form=form)
    else:
        if form.validate_on_submit():
            scheme_id = request.form.get('scheme_id')
            
            conn = get_db_connection()
            db = conn.cursor()
            
            db.execute("""
                    insert into scheme_enrollment(citizen_id,scheme_id,enrollment_date) values (%s,%s,%s);
                    """,[current_user.citizen_id,scheme_id,datetime.today().strftime('%Y-%m-%d')])

            conn.commit()
            
            db.execute("""
                    (SELECT scheme_id,name,description
                    from welfare_scheme)
                    except
                    (SELECT scheme_id,name,description
                     FROM welfare_scheme natural join scheme_enrollment);
                    """)
            res = db.fetchall()
            
            scheme_id = [row[0] for row in res]
            scheme_title = [row[1] for row in res]
            scheme_description = [row[2] for row in res] 
            
            db.close()
            conn.close()
            
        return render_template('welfare_scheme.html',scheme_id=scheme_id,scheme_title=scheme_title,scheme_description=scheme_description,
                                                    request_type='Active',form=form)

# Vaccinations 
@citizen_bp.route('/vaccination',methods=['GET','POST'])
@login_required
@citizen_required
@verification_required
def vaccination():
    form = RequestForm()
    
    if request.method == 'GET':
        request_type = request.args.get('request_type')
        
        vaccine_id = []
        vaccine_type = []
        centers = []
        date_administered = []
        
        if request_type == 'Active':
            conn = get_db_connection()
            db = conn.cursor()
            
            if current_user.role == 'citizen':
                db.execute("""
                            (SELECT vaccine_id,vaccine_type, centers
                            from vaccines)
                            except
                            (SELECT vaccine_id,vaccine_type, centers
                            FROM vaccines natural join vaccination);
                        """)
            else:
                db.execute("""
                            (SELECT vaccine_id,vaccine_type, centers
                            from vaccines);
                        """)
            
            res = db.fetchall()
            vaccine_id = [row[0] for row in res]
            vaccine_type = [row[1] for row in res]
            centers = [row[2] for row in res]
            
            db.close()
            conn.close()
        else:
            conn = get_db_connection()
            db = conn.cursor()
            
            db.execute("""
                        SELECT vaccine_id,vaccine_type, centers, date_administered
                        FROM vaccines natural join vaccination
                        WHERE citizen_id = %s;
                    """,[current_user.citizen_id])
            
            res = db.fetchall()
            vaccine_id = [row[0] for row in res]
            vaccine_type = [row[1] for row in res]
            centers = [row[2] for row in res]
            date_administered = [row[3] for row in res]
            
            db.close()
            conn.close()
        
        return render_template('vaccination.html',vaccine_id=vaccine_id,vaccine_type=vaccine_type,centers=centers,
                            date_administered=date_administered,request_type=request_type,form=form)
    else:
        if form.validate_on_submit():
            vaccine_id = request.form.get('vaccine_id')
            
            conn = get_db_connection()
            db = conn.cursor()
            
            db.execute("""
                       INSERT INTO Vaccination(citizen_id,vaccine_id,date_administered) values (%s,%s,%s);
                    """,[current_user.citizen_id,vaccine_id,datetime.today().strftime('%Y-%m-%d')])
            conn.commit()
            
            db.execute("""
                        (SELECT vaccine_id,vaccine_type, centers
                        from vaccines)
                        except
                        (SELECT vaccine_id,vaccine_type, centers
                        FROM vaccines natural join vaccination);
                    """)
            
            res = db.fetchall()
            vaccine_id = [row[0] for row in res]
            vaccine_type = [row[1] for row in res]
            centers = [row[2] for row in res]
            
            db.close()
            conn.close()
            
        return render_template('vaccination.html',vaccine_id=vaccine_id,vaccine_type=vaccine_type,centers=centers,
                                    request_type='Active',form=form)

# Taxes
@citizen_bp.route('/taxes')
@login_required
@citizen_required
@verification_required
def taxes():
    conn = get_db_connection()
    db = conn.cursor()
    
    db.execute("""
               SELECT type,tax_year,tax_month,amount_due,due_date,status
               FROM taxes
               WHERE citizen_id = %s;
            """,[current_user.citizen_id])
    
    res = db.fetchall()
    tax_type = [row[0] for row in res]
    tax_year = [row[1] for row in res]
    tax_month = [row[2] for row in res]
    amount_due = [row[3] for row in res]
    due_date = [row[4] for row in res]
    status = [row[5] for row in res]
    
    db.close()
    conn.close()
    return render_template('taxes.html',tax_type=tax_type,tax_year=tax_year,tax_month=tax_month,amount_due=amount_due,due_date=due_date,status=status)

# Services
@citizen_bp.route('/service',methods=['GET','POST'])
@login_required
@citizen_required
@verification_required
def service():
    form = RequestForm()
    
    if request.method == 'GET':
        request_type = request.args.get('request_type')
        
        doc_id = []
        issue_date = []
        doc_type = []
        description = []
        
        if request_type == 'Active':
            conn = get_db_connection()
            db = conn.cursor()
            
            if current_user.role == 'citizen':
                db.execute("""
                        (SELECT doc_id,doc_type,description
                        FROM service)
                        except
                        (SELECT doc_id,doc_type,description
                        FROM service natural join documents);
                        """)
            else:
                db.execute("""
                        (SELECT doc_id,doc_type,description
                        FROM service);
                        """)
                
            res = db.fetchall()
            doc_id = [row[0] for row in res]
            doc_type = [row[1] for row in res]
            description = [row[2] for row in res]
            
            db.close()
            conn.close()
        else:
            conn = get_db_connection()
            db = conn.cursor()
            
            db.execute("""
                    SELECT doc_id,issue_date,doc_type,description
                    FROM service natural join documents
                    WHERE citizen_id = %s;
                    """,[current_user.citizen_id])
            res = db.fetchall()
            doc_id = [row[0] for row in res]
            issue_date = [row[1] for row in res]
            doc_type = [row[2] for row in res]
            description = [row[3] for row in res]
            
            db.close()
            conn.close()
        
        return render_template('service.html',doc_id=doc_id,issue_date=issue_date,doc_type=doc_type,description=description,
                                            request_type=request_type,form=form)
    else:
        if form.validate_on_submit():
            doc_id = request.form.get('doc_id')
            
            conn = get_db_connection()
            db = conn.cursor()
            
            db.execute("""
                    INSERT INTO documents(citizen_id,doc_id,issue_date) values (%s,%s,%s);
                    """,[current_user.citizen_id,doc_id,datetime.today().strftime('%Y-%m-%d')])
            conn.commit()
            
            if current_user.role == 'citizen':
                db.execute("""
                        (SELECT doc_id,doc_type,description
                        FROM service)
                        except
                        (SELECT doc_id,doc_type,description
                        FROM service natural join documents);
                        """)
            else:
                db.execute("""
                        (SELECT doc_id,doc_type,description
                        FROM service);
                        """)
                
            res = db.fetchall()
            doc_id = [row[0] for row in res]
            doc_type = [row[1] for row in res]
            description = [row[2] for row in res]
            
            db.close()
            conn.close()
        
        return render_template('service.html',doc_id=doc_id,doc_type=doc_type,description=description,
                                            request_type='Active',form=form)
            