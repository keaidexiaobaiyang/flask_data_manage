from flask import Blueprint, render_template,request,redirect,url_for,jsonify
from flask_login import login_required,current_user
from app.models import users,Productpnl
from sqlalchemy import and_
import datetime

datahome_bp = Blueprint('datahome',__name__)

@datahome_bp.route('/datahome',methods=['GET','POST'])
def datahome():
    if request.method == 'GET':
        return render_template('datahome.html')
    elif request.method == 'POST':
        print('test')
    else:
        print('不是我想要的')

@datahome_bp.route('/datahome/get_data')
def get_data():
    product=request.args.get('product_id')
    num=request.args.get('num')
    need_type_dict={'1':'单日盈亏','2':'支付金额','3':'退款金额','4':'访客数','5':'支付件数'}
    need_type=need_type_dict[request.args.get('need_type')]
    print(product,num,need_type)
    today=datetime.date.today()
    start_day=today - datetime.timedelta(days=int(num))
    end_day=today
    data=Productpnl.query.filter(and_(
                                    Productpnl.商品id==product,
                                    Productpnl.日期 >= start_day,
                                    Productpnl.日期 < end_day
                                    )).all()
    print(data,type(data))
    need_data={'x_data':[i.日期 for i in data],'y_data':[getattr(i,need_type) for i in data],'dryk':[i.单日盈亏 for i in data]}
    result=jsonify(need_data)
    print(result)
    return result

@datahome_bp.route('/datahome/get_data/data_ZG')
def get_data_ZG():
    num=request.args.get('num')
    product_id=request.args.get('product_id')
    return render_template('data_ZG.html',num=num,product_id=product_id)