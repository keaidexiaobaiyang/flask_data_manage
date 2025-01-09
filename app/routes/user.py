from flask import Blueprint, render_template,request,jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user,logout_user
from app.models import users,Productpnl,get_all_children,all_shop,all_users_logs,get_user_log,db
from sqlalchemy import and_,or_,inspect
import datetime
import pandas as pd
import json
userhome_bp = Blueprint('userhome',__name__)

#个人中心
@userhome_bp.route('/userhome')
#@login_required
def userhome():
    return render_template('个人中心界面/userhome.html', user=current_user)

#个人信息
@userhome_bp.route('/userhome/userdata')
@login_required
def user_data():
    user_los_name=current_user.user_name+'个人日志'
    inspector = inspect(db.engine)
    print(user_los_name,inspector)
    if not inspector.has_table(user_los_name):
        userlogs=None
    else:
        if user_los_name in all_users_logs.keys():
            userlogs=[i.to_dict() for i in all_users_logs[user_los_name].query.all()]
            #userlogs='在初始表中'
        else:
            userlogs=[i.to_dict() for i in get_user_log(current_user.user_name).query.all()]
            #userlogs = '不在初始表'
    print(userlogs,all_users_logs)
    return render_template('个人中心界面/个人信息.html',userlogs=userlogs,user=current_user.user_name)

@userhome_bp.route('/userhome/userchangepassword',methods=['POST'])
@login_required
def change_password():
    data=request.get_data()
    data=json.loads(data)
    print(data)
    print(current_user.user_name)
    sql_password=users.query.filter(users.user_name==current_user.user_name).first().to_dict()['user_password']
    old_password=data['oldpassword']
    if old_password == sql_password:
        try:
            user_to_update = users.query.filter(users.user_name==current_user.user_name).first()
            user_to_update.user_password = data['newpassword']
            db.session.commit()
            logout_user()
            return jsonify('成功，请刷新界面重新登录')
        except Exception as e:
            return jsonify(f'失败{e}')
    else:
        return jsonify('失败,密码错误')

@userhome_bp.route('/userhome/userdata/createuserlog',methods=['GET','POST'])
def createuserlog():
    if request.method=='POST':
        inspector = inspect(db.engine)
        user_los_name = current_user.user_name + '个人日志'
        print(user_los_name,inspector)
        if not inspector.has_table(user_los_name):
            user_log_table=get_user_log(current_user.user_name)
            table1=user_log_table(date=datetime.date.today(),title='创建日志',logdata='首次创建自己的日志',
                                  createtime=datetime.datetime.now(),status='公开',comment='初始化第一条',level=2)
            try:
                db.session.add(table1)
                db.session.commit()
                return jsonify({'status': 'success', 'message': f'{user_los_name}初始化成功'}), 200
            except Exception as e:
                db.session.rollback()  # 发生异常时回滚
                print(f"An error occurred: {e}")
                return jsonify({'status': 'error', 'message': f'{user_los_name}初始化失败'}), 200
        else:
            print('表格已经存在')
            return jsonify({'status': 'error', 'message': f'{user_los_name}表格已存在'}),200
#商品信息
@userhome_bp.route('/userhome/pruductdata')
#@login_required
def pruduct_data():
    return render_template('个人中心界面/商品信息.html',user=current_user)

#店铺信息
@userhome_bp.route('/userhome/shopdata2')
#@login_required
def shop_data2():
    return render_template('个人中心界面/店铺信息.html',user=current_user)

@userhome_bp.route('/userhome/userlogedit',methods=['GET','POST'])
def userlogedit():
    if request.method=='POST':
        result_data={
            "code": 0,
            "msg": "",

            "count": 0,
            "data": 0,
        }
        return jsonify(result_data)
    elif request.method=='GET':
        return render_template('个人中心界面/个人日志编辑.html')

@userhome_bp.route('/userhome/groupdata')
#@login_required
def group_data():
    return render_template('个人中心界面/团队信息.html', user_name=current_user)

@userhome_bp.route('/userhome/shopdata')
@login_required
def shop_data():
    user_name=current_user.user_name
    return render_template('shopdata.html',user_name=user_name)

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



