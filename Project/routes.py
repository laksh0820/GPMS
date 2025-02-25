from flask import Flask,render_template,redirect,url_for,flash
from flask_login import login_user,login_required,current_user,logout_user
from Project import app,db
from Project.forms import LogInForm
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
                    SELECT user_id, password, type
                    FROM users
                    WHERE user_id = %s;
                  """, [form.UserID.data])
        user = User(db.fetchall()[0])
        if user:
            login_user(user,remember=form.remember_me.data)
            flash('Logged in Successfully')
        else:
            flash("User not Found!! Try Again",'error')
    return render_template('login.html',form=form)