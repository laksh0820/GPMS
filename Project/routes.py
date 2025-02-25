from flask import Flask,render_template,redirect,url_for,flash, request
from flask_login import login_user,login_required,current_user,logout_user
from Project import app,db,conn
from Project.forms import LogInForm,CitizenForm,UserForm
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
                    SELECT user_id, password, role
                    FROM user
                    WHERE user_id = %s;
                  """, [form.UserID.data])
        user = User(db.fetchall()[0])
        if user:
            login_user(user,remember=form.remember_me.data)
            flash('Logged in Successfully')
        else:
            flash("User not Found!! Try Again",'error')
    return render_template('login.html',form=form)

# Register an user
@app.route('/register')
def register():
    return render_template('register.html')

# Register an user with the given role 
@app.route('/register_role/<role>',methods=['GET','POST'])
def register_role(role):
    form = CitizenForm()
    if form.validate_on_submit():
        db.execute("""
                    SELECT id, email, password, role
                    FROM users
                    WHERE email = %s; 
                """,[form.email.data])
        users = db.fetchall()
        if len(users):
            flash('This email already exits. Please sign in','error')
        else:
            if role == 'citizen':
                db.execute("""
                        insert into household(household_id,address,income) values (%s,%s,%s);
                        """,[form.household_id.data,form.address.data,form.income.data])
                db.execute("""
                        SELECT count(*)
                        from citizen;
                        """)
                citizen_id = len(db.fetchall()) + 1
                db.execute("""
                        insert into citizen(citizen_id,name,gender,dob,household_id,educational_qualification) values (%s,%s,%s,%s,%s,%s);
                        """,[citizen_id,form.name.data,form.gender.data,form.dob.data,form.household_id.data,form.educational_qualification.data])
                db.execute("""
                        insert into users(email,password,citizen_id,role) values (%s,%s,%s,%s);
                        """,[form.email.data,form.password.data,citizen_id,role])
                conn.commit()
            else:
                db.execute("""
                        insert into users(email,password,role) values (%s,%s,%s);
                        """,[form.email.data,form.password.data,role])
                conn.commit()
    else:
        print(form.errors)
    return render_template('register_role.html',form=form,role=role)

