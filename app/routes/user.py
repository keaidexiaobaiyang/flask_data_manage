from flask import Blueprint, render_template,request,jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from app.models import users,Productpnl,get_all_children
from sqlalchemy import and_,or_
import datetime
import pandas as pd
userhome_bp = Blueprint('userhome',__name__)

@userhome_bp.route('/userhome')
#@login_required
def userhome():
    #user_name=current_user.user_name
    user_name='ng'
    return render_template('user_home.html',user_name=user_name)

@userhome_bp.route('/userhome/getdata',methods=['GET','POST'])
#@login_required
def userhome_data():
    if request.method == 'GET':
        today = datetime.date.today()
        start_day= today-datetime.timedelta(days=30)
        user_name=current_user.user_name
        _,data_len = get_all_children(users, user_name)
        need_condition=[]
        for i in data_len:
            need_condition.append(Productpnl.店铺名称.like(f'%{i}%'))
        data = Productpnl.query.filter(and_(
            or_(*need_condition),
            Productpnl.日期 >= start_day,
            Productpnl.日期 < today
        )).all()

        df=pd.DataFrame([i.to_dict() for i in data])
        print(df)
        df['日期']=df['日期'].apply(lambda x:datetime.datetime.strptime(x,'%Y-%m-%d'))
        df['日期'] = pd.to_datetime(df['日期']).dt.date
        my_dict=[]
        for i in df.groupby('店铺名称'):
            temp_dict = {}
            temp_dict['店铺名称'] = i[0]
            temp_dict['昨日收入'] = round(i[1]['单日盈亏'][i[1]['日期'] == today-datetime.timedelta(days=1)].sum(),2)
            temp_dict['本周收入'] = round(i[1]['单日盈亏'][i[1]['日期'] > today-datetime.timedelta(days=7)].sum(),2)
            temp_dict['本月收入'] = round(i[1]['单日盈亏'][i[1]['日期'] > today-datetime.timedelta(days=30)].sum(),2)
            my_dict.append(temp_dict)
        print(my_dict)
        result_data={
            "code": 0,
            "msg": "",
            "count": len(my_dict),
            "data": my_dict
        }
        data = jsonify(result_data)
        return data

@userhome_bp.route('/userhome/getshopdata',methods=['GET','POST'])
def userhome_getshopdata():
    if request.method == 'GET':
        need_type=request.args.get('type')
        user_name=current_user.user_name
        _,data_len = get_all_children(users, user_name)
        need_condition=[]
        print(data_len)
        for i in data_len:
            need_condition.append(Productpnl.店铺名称.like(f'%{i}%'))
        data = Productpnl.query.filter(and_(
            or_(*need_condition),
            Productpnl.日期 >= datetime.date.today() - datetime.timedelta(days=30),
        )).all()
        df = pd.DataFrame([i.to_dict() for i in data])
        my_dict={}
        for i in df.groupby('店铺名称'):
            my_dict[i[0]]=round(i[1]['单日盈亏'].sum() ,2)
        print(my_dict)
        if need_type == '1':
            temp_list=[]
            for i,j in my_dict.items():
                if j > 0:
                    temp_dict={}
                    temp_dict['value']=j
                    temp_dict['name']=i
                    temp_list.append(temp_dict)
                else:
                    temp_dict={}
                    temp_dict['value']=0
                    temp_dict['name']=i
                    temp_list.append(temp_dict)
            print(temp_list)
            json_data=jsonify(temp_list)
        else:
            temp_list=[]
            for i,j in my_dict.items():
                if j <= 0:
                    temp_dict={}
                    temp_dict['value']=-j
                    temp_dict['name']=i
                    temp_list.append(temp_dict)
                else:
                    temp_dict={}
                    temp_dict['value']=0
                    temp_dict['name']=i
                    temp_list.append(temp_dict)
            print(temp_list)
            json_data=jsonify(temp_list)
        print(json_data)
    return json_data



