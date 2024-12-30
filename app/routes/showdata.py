from flask import Blueprint, render_template,request,jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from app.models import users,Productpnl
from sqlalchemy import and_
import datetime

showdata_bp = Blueprint('showdata',__name__)

@showdata_bp.route('/showdata')
@login_required
def showdata():
    return render_template('showdata.html')

@showdata_bp.route('/getdata',methods=['POST','GET'])
@login_required
def getdata():
    if request.method == 'POST':
        pass
    else:
        today = datetime.date.today()
        page=request.args.get('page')
        limit=request.args.get('limit')
        start_date=request.args.get('start_date')
        end_date=request.args.get('end_date')
        product_id=request.args.get('product_id')
        shop_name=request.args.get('shop_name')

        print(page, limit, start_date, end_date, product_id, shop_name)
        print(type(page), type(limit), type(start_date), type(end_date), type(product_id), type(shop_name))
        try:
            start_date = datetime.datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
        except:
            start_date = today - datetime.timedelta(days=30)

        try:
            end_date = datetime.datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()
        except:
            end_date = today
        filters=[]
        if product_id:
            filters.append(Productpnl.商品id.like(f'%{product_id}%'))
        if shop_name:
            filters.append(Productpnl.店铺名称.like(f'%{shop_name}%'))

        sp_data = Productpnl.query.filter(and_(Productpnl.店铺名称.like(f'%{current_user.user_name}%'),
                                                Productpnl.日期 >= start_date,
                                                Productpnl.日期 <= end_date,
                                                *filters,
                                                )).order_by(Productpnl.日期.desc()).paginate(page=int(page), per_page=int(limit) )


        result_data={
            "code": 0,
            "msg": "",

            "count": sp_data.total,
            "data": [i.to_dict() for i in sp_data.items]
        }
        data = jsonify(result_data)
        print(data)
        return data
