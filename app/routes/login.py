from flask import Blueprint, render_template,request,jsonify, redirect, url_for, flash
from app.models import Users,Productpnl
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
login_bp = Blueprint('login', __name__)





@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    # print(dir(current_user))
    # if current_user.is_authenticated:
    #     print('已经登录')
    #     return redirect(url_for('main.index'))

    if request.method == 'POST':
        print(1)
        print(json.loads(request.data))
        data=json.loads(request.data)
        # username = request.form['username']
        # password = request.form['password']
        user = Users.query.filter_by(user_name=data['username'], user_password=data['password']).first()
        print(user)
        if user:
            login_user(user)
            flash('Logged in successfully.')
            next = request.args.get('next')
            if next:
                print(f'你已遭受重定向攻击{next}')
                return jsonify({'redirect':url_for('main.warning',data=f'你已遭受重定向攻击{next}')})
            else:
                print('登录成功')
                return jsonify({'redirect':url_for('main.index')})
        else:
            print('账号密码错误')
            flash('Invalid username or password')
            return render_template('login.html')

    return render_template('login.html')


@login_bp.route('/users')
def return_user():
    users = Users.query.all()
    print(1,type(users))
    print([[i.owner,i.user_name,i.user_password] for i in users])
    print(users)
    return str(users)

@login_bp.route('/loginout')
@login_required
def loginout():
    logout_user()
    return redirect(url_for('main.index'))