from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库连接
password='duoduo20241204baiyang%40_.'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://duoduo:{password}@192.168.1.148:3306/pdd_data?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库对象
db = SQLAlchemy(app)

# 定义模型
class Users(db.Model):

    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(60))
    user_password = db.Column(db.String(100))
    create_time = db.Column(db.Date)
    owner = db.Column(db.String(20))


# 创建数据库表
with app.app_context():
    db.create_all()

# 定义路由
@app.route('/')
def index():
    users = Users.query.all()
    print('返回值',users[0].user_password)
    print(type(users))
    return '<br>'.join([str(users) for user in users])

if __name__ == '__main__':
    app.run(debug=True,port=10001)
