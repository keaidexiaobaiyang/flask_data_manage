from flask import Blueprint, render_template,request,jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from app.models import users,Productpnl,get_all_children
from sqlalchemy import and_
import datetime
import requests as rq
import json

managehome_bp = Blueprint('managehome',__name__)

@managehome_bp.route('/managehome')
@login_required
def managehome():
    return render_template('managehome.html')


@managehome_bp.route('/managehome/getusertree',methods=['GET','POST'])
@login_required
def getusertree():
    if request.method == 'GET':
        name = current_user.user_name
        data,data_len=get_all_children(users,name)
        print(data_len)
        result_data={
            "code": 0,
            "msg": "",
            "count": len(data_len),
            "data": [data]
        }
        jsondata=json.dumps(result_data,ensure_ascii=False)
        print(jsondata)
        return jsondata


