from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class Users(UserMixin,db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(60), nullable=False)
    user_password=db.Column(db.String(100), nullable=False)
    create_time=db.Column(db.DateTime)
    owner=db.Column(db.String(20), db.ForeignKey('user.user_id'))

    def __init__(self):
        pass

    def get_id(self):
        return self.user_id

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