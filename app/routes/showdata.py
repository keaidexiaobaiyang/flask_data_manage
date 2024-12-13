from flask import Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from app.models import Users,Productpnl

showdata_bp = Blueprint('showdata',__name__)

@showdata_bp.route('/showdata')
@login_required
def showdata():
    print(current_user.user_name)
    user=current_user.user_name
    if user == 'root':
        sp = Productpnl.query.all()
    else:
        sp = Productpnl.query.filter(Productpnl.店铺名称.ilike(f'%{user}%')).all()
    print(sp)
    return '<br>'.join([str(i) for i in sp])