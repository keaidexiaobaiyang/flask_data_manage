from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app.extensions import login_manager

main_bp=Blueprint('main',__name__)

@main_bp.route('/')
def re_index():
    return redirect(url_for('login.login'))

@main_bp.route('/home')
@login_required
def index():
    print(current_user)
    return render_template('main.html',user=current_user)


@main_bp.route('/warning/<string:data>')
def warning(data):
    return render_template('warning.html',warning_data=data)