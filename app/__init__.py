from flask import Flask
from .routes.login import login_bp
from .routes.main import main_bp
from .routes.showdata import showdata_bp
from .routes.datahome import datahome_bp
from .models import db,Users
from .extensions import LoginManager
#from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.models import Users
import secrets

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    return user

def create_app():
    #初始化整个网站的实例
    app = Flask(__name__)
    secrets_temp=secrets.token_hex(16)
    app.config['SECRET_KEY']=secrets_temp
    url = 'mysql+pymysql://duoduo:duoduo20241204baiyang%40_.@192.168.1.148:3306/pdd_data'
    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'login.login'  # 设置未登录时重定向的视图
    login_manager.login_message = '请登录先登录'

    #从路由中读取已经设置好的路由
    app.register_blueprint(login_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(showdata_bp)
    app.register_blueprint(datahome_bp)


    return app