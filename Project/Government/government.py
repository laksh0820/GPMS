from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user,login_required,current_user,logout_user
from flask_wtf import FlaskForm
government_bp = Blueprint('government',__name__,url_prefix='/government', template_folder='templates')

@government_bp.route('/')
@login_required
# @government_monitor_required
def base():
    return render_template('government_dashboard.html')

