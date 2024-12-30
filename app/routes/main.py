from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
import datetime
from app.models import users,Productpnl
from app.extensions import login_manager
from sqlalchemy import and_

main_bp=Blueprint('main',__name__)

@main_bp.route('/')
def re_index():
    return redirect(url_for('main.index'))

@main_bp.route('/home')
@login_required
def index():
    print(current_user)
    # 获取当前日期
    today = datetime.date.today()
    # 昨日
    yesterday = today - datetime.timedelta(days=1)
    # 本周
    start_of_week = today - datetime.timedelta(days=today.weekday())  # 本周一
    end_of_week = today
    # 本月
    start_of_month = today.replace(day=1)
    end_of_month = today
    #开始获取数据
    yesterday_results = Productpnl.query.filter(and_(Productpnl.日期 == yesterday,Productpnl.店铺名称.like(f'%{current_user.user_name}%') ) ).all()
    yesterday_sr=sum([i.单日盈亏 for i in yesterday_results])

    week_results = Productpnl.query.filter(and_(Productpnl.日期 >= start_of_week, Productpnl.日期 <= end_of_week,Productpnl.店铺名称.like(f'%{current_user.user_name}%') ) ).all()
    week_sr = sum([i.单日盈亏 for i in week_results])

    month_results = Productpnl.query.filter(and_(Productpnl.日期 >= start_of_month,Productpnl.日期 <= end_of_month,Productpnl.店铺名称.like(f'%{current_user.user_name}%') ) ).all()
    month_sr = sum([i.单日盈亏 for i in month_results])


    data={'profit':{'day':yesterday_sr,'week':week_sr,'month':month_sr}}
    date = str(datetime.date.today() )

    return render_template('main.html',user=current_user,data=data,date=date)


@main_bp.route('/warning/<string:data>')
def warning(data):
    return render_template('warning.html',warning_data=data)