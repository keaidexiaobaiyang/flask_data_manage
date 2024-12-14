from flask import Blueprint, render_template,request,jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from app.models import Users,Productpnl

showdata_bp = Blueprint('showdata',__name__)

@showdata_bp.route('/showdata')
@login_required
def showdata():
    return render_template('showdata.html')

@showdata_bp.route('/getdata',methods=['POST','GET'])
def getdata():
    if request.method == 'POST':
        pass
    else:
        sp_data = Productpnl.query.filter(Productpnl.店铺名称.like(f'%{current_user.user_name}%')).all()
        result_data={
            "code": 0,
            "msg": "",
            "count": 1000,
            "data": [i.to_dict() for i in sp_data[-600:]]
        }
        data = jsonify(result_data)
        print(data)
        return data
