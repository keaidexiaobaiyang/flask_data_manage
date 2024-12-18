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
    访客数 = db.Column(db.Integer, nullable=False)
    支付件数 = db.Column(db.Integer, nullable=False)
    支付买家数 = db.Column(db.Integer, nullable=False)
    支付金额 = db.Column(db.Numeric(precision=10,scale=3), nullable=False)
    评价有礼 = db.Column(db.Numeric(precision=6,scale=2), nullable=False)
    退款金额 = db.Column(db.Numeric(precision=10,scale=2), nullable=False)
    单日盈亏 = db.Column(db.Numeric(precision=10, scale=2), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            '日期': str(self.日期),  # 将日期转换为字符串
            '店铺名称': self.店铺名称,
            '产品名称': self.产品名称,
            '商品id': self.商品id,
            '访客数': self.访客数,
            '支付件数': self.支付件数,
            '支付买家数': self.支付买家数,
            '支付金额': float(self.支付金额),  # 将 Decimal 转换为 float
            '评价有礼': float(self.评价有礼),  # 将 Decimal 转换为 float
            '退款金额': float(self.退款金额),
            '单日盈亏': float(self.单日盈亏),  # 将 Decimal 转换为 float
        }


