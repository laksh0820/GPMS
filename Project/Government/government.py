from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,login_required,current_user,logout_user
from flask_wtf import FlaskForm
government_bp = Blueprint('government',__name__,url_prefix='/government', template_folder='templates')

def government_monitor_required(inner_func):
    def wrapped_function_government_monitor(*args,**kwargs):
        if (current_user.role != 'government' and current_user.role != 'admin'):
            flash("Please log in as Government Monitor to access this page",'error')
            return redirect(url_for(f'{current_user.role}.base'))
            print ("User not logged in as Government Monitor")
        return inner_func(*args,**kwargs)
    wrapped_function_government_monitor.__name__ = inner_func.__name__
    return wrapped_function_government_monitor

@government_bp.route('/')
@login_required
# @government_monitor_required
def base():
    return render_template('government_dashboard.html')

