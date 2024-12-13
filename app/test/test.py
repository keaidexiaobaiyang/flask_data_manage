from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# 配置数据库连接
url='mysql+pymysql://duoduo:duoduo20241204baiyang%40_.@192.168.1.148:3306/pdd_data'
app.config['SQLALCHEMY_DATABASE_URI'] = url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 定义数据模型
class Productpnl(db.Model):
    __tablename__='productpnl'
    id = db.Column(db.Integer, primary_key=True)
    日期 = db.Column(db.Date, nullable=False)
    店铺名称 = db.Column(db.String(30), nullable=False)
    产品名称 = db.Column(db.String(40))
    商品id = db.Column(db.String(40), nullable=False)
    单日盈亏 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return fr'{self.日期} {self.店铺名称} {self.商品id} {self.单日盈亏}'

class Users(db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(60), nullable=False)
    user_password=db.Column(db.String(100), nullable=False)
    create_time=db.Column(db.DateTime)
    owner=db.Column(db.String(20), db.ForeignKey('user.user_id'))
    

@app.route('/<string:name>')
def get_users(name):
    sp = Productpnl.query.filter(Productpnl.店铺名称.ilike(f'%{name}%')).all()
    print(sp)
    return '<br>'.join([str(i) for i in sp])

@app.route('/')
def index():
    return '请输入需要查询的人'

@app.route('/users/')
def return_user():
    users = Users.query.all()
    print(1,type(users))
    print([[i.owner,i.user_name,i.user_password] for i in users])
    print(users)
    return str(users)

if __name__ == '__main__':
    app.run(debug=True,port=10131)
 