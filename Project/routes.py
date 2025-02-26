from flask import Flask,render_template,redirect,url_for,flash, request
from flask_login import login_user,login_required,current_user,logout_user
from Project import app,db,conn
from Project.forms import LogInForm,CitizenForm,PanchayatEmployeeForm,GovernmentForm,AdminForm
from Project.models import User

# Home Page
@app.route('/')
def base(): 
    return render_template('base.html')

# Log in to an existing user
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("Already loged in")
        return redirect(url_for('base'))
    
    form = LogInForm()

    if form.validate_on_submit():
        db.execute("""
                    SELECT *
                    FROM users
                    WHERE email = %s and role = %s;
                  """, [form.email.data,form.role.data])
        res = db.fetchall()
        if len(res):
            user = User(res[0])
            if user.password == form.password.data:
                login_user(user,remember=form.remember_me.data)
                flash('Logged in Successfully')
            else:
                flash("Wrong Password!! Try Again",'error') 
        else:
            flash("User not Found!! Try Again",'error')
    return render_template('login.html',form=form)

# Log out to an logged in User
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out Successfully')
    return redirect(url_for('login'))

# Register an user
@app.route('/register')
def register():
    return render_template('register.html')

# Register an user with the given role 
@app.route('/register_role/<role>',methods=['GET','POST'])
def register_role(role):
    if role == 'citizen':
        form = CitizenForm()
    elif role == 'panchayat_employee':
        form = PanchayatEmployeeForm()
    elif role == 'government':
        form = GovernmentForm()
    elif role == 'admin':
        form = AdminForm()
    else:
        flash('Invalid Role','error')
        return redirect(url_for('register'))
    
    if form.validate_on_submit():
        db.execute("""
                    SELECT id, email, password, role
                    FROM users
                    WHERE email = %s and role = %s; 
                """,[form.email.data,role])
        users = db.fetchall()
        if len(users):
            flash('This email and role already exits. Please sign in or Register with a different role','error')
            return redirect(url_for('register'))
        else:
            if role == 'citizen':
                db.execute("""
                           SELECT * 
                           from household
                           where household_id = %s;
                        """,[form.household_id.data])
                res = db.fetchall()
                if len(res) == 0:
                    db.execute("""
                            insert into household(household_id,address,income) values (%s,%s,%s);
                            """,[form.household_id.data,form.address.data,form.income.data])
                db.execute("""
                        SELECT case
                                when max(citizen_id) is not null then max(citizen_id)
                                else 0
                               end
                        from citizen;
                        """)
                res = db.fetchall()
                citizen_id = res[0][0] + 1
                db.execute("""
                        insert into citizen(citizen_id,name,gender,dob,household_id,educational_qualification) values (%s,%s,%s,%s,%s,%s);
                        """,[citizen_id,form.name.data,form.gender.data,form.dob.data,form.household_id.data,form.educational_qualification.data])
                db.execute("""
                        insert into users(email,password,citizen_id,role) values (%s,%s,%s,%s);
                        """,[form.email.data,form.password.data,citizen_id,role])
                conn.commit()
                flash('Registration Successful','Success')
                return redirect(url_for('login'))
            elif role == 'panchayat_employee':
                db.execute("""
                        SELECT *
                        from users
                        where email = %s and role = 'citizen';
                        """,[form.email.data])
                res = db.fetchall()
                if len(res) == 0:
                    flash('Please Register as a citizen before registering as a Panchayat Employee','error')
                    return redirect(url_for('register'))
                else:
                    user = User(res[0])
                    db.execute("""
                            insert into panchayat_employee(citizen_id,role) values (%s,%s);
                            """,[user.citizen_id,form.role.data])
                    db.execute("""
                        insert into users(email,password,role) values (%s,%s,%s);
                        """,[form.email.data,form.password.data,role])
                    conn.commit()
                    flash('Registration Successful','Success')
                    return redirect(url_for('login'))
            elif role == 'government':
                db.execute("""
                        SELECT *
                        from users
                        where email = %s and role = 'citizen';
                        """,[form.email.data])
                res = db.fetchall()
                if len(res) == 0:
                    flash('Please Register as a citizen before registering as a Government Monitor','error')
                    return redirect(url_for('register'))
                else:
                    user = User(res[0])
                    db.execute("""
                            insert into users(email,password,role) values (%s,%s,%s);
                            """,[form.email.data,form.password.data,role])
                    conn.commit()
                    flash('Registration Successful','Success')
                    return redirect(url_for('login'))
            elif role == 'admin':
                db.execute("""
                        SELECT *
                        from users
                        where email = %s and role = 'citizen';
                        """,[form.email.data])
                res = db.fetchall()
                if len(res) == 0:
                    flash('Please Register as a citizen before registering as an Admin','error')
                    return redirect(url_for('register'))
                else:
                    user = User(res[0])
                    db.execute("""
                            insert into users(email,password,role) values (%s,%s,%s);
                            """,[form.email.data,form.password.data,role])
                    conn.commit()
                    flash('Registration Successful','Success')
                    return redirect(url_for('login'))
            else:
                flash('Invalid Registration Role','error')
                return redirect(url_for('register'))
    else:
        print("Role Registration Error : ",form.errors)
    return render_template('register_role.html',form=form,role=role)

