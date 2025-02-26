from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,login_required,current_user,logout_user
from flask_wtf import FlaskForm
government_bp = Blueprint('government',__name__,url_prefix='/government', template_folder='templates')

def government_monitor_required(inner_func):
    def wrapped_function_government_monitor(*args,**kwargs):
        if current_user.is_authenticated and current_user.role != 'government' and current_user.role != 'admin':
            flash("Please log in as Government Monitor to access this page",'error')
            return redirect(url_for(f'{current_user.role}.base'))
        return inner_func(*args,**kwargs)
    wrapped_function_government_monitor.__name__ = inner_func.__name__
    return wrapped_function_government_monitor

@government_bp.route('/')
@login_required
@government_monitor_required
def base():
    return render_template('dashboard.html')

@government_bp.route('/agricultural_data')
@login_required
@government_monitor_required
def agricultural_data():
    pass

@government_bp.route('/vaccination')
@login_required
@government_monitor_required
def vaccination():
    pass

@government_bp.route('/census_data')
@login_required
@government_monitor_required
def census_data():
    pass

@government_bp.route('/environmental_data')
@login_required
@government_monitor_required
def environmental_data():
    pass