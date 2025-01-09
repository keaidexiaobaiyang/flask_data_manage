from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import inspect
db = SQLAlchemy()
import datetime
from datetime import date

all_shop={}
all_users_logs={}

class users(UserMixin, db.Model):
    user_id=db.Column(db.Integer, primary_key=True)
    user_name=db.Column(db.String(60), nullable=False,unique=True,index=True)
    user_password=db.Column(db.String(100), nullable=False)
    user_level = db.Column(db.String(50), nullable=False)
    create_time=db.Column(db.DateTime)
    father_name = db.Column(db.String(60), nullable=False)
    permision_level = db.Column(db.String(60), nullable=False)
    owner=db.Column(db.String(20) )


    def get_id(self):
        return self.user_id

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'user_name': self.user_name,
            'create_time': self.create_time,
            'father_name': self.father_name,
            'owner': self.owner,
            'user_level':self.user_level,
            'user_password': self.user_password,
        }

class shopConfig(db.Model):
    __tablename__='shop_config'
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(60), nullable=False)
    create_time = db.Column(db.DateTime)
    create_user = db.Column(db.String(60),db.ForeignKey('users.user_name'))
    owner=db.Column(db.String(20),db.ForeignKey('users.user_name'))

    def to_dict(self):
        return {
            'id': self.id,
            'shop_name': self.shop_name,
            'create_time': self.create_time,
            'create_user': self.create_user,
            'owner': self.owner,
        }

class User_shop_relation(db.Model):
    __tablename__='user_shop_relation_config'
    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(60), db.ForeignKey('shop_config.shop_name'))
    user=db.Column(db.String(60), db.ForeignKey('users.user_name'))

class ProductConfig(db.Model):
    __tablename__='product_config'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(60), nullable=False)
    product_id = db.Column(db.String(60), nullable=False)
    shop_name = db.Column(db.String(60), nullable=False)
    owner = db.Column(db.String(60),db.ForeignKey('users.user_name'), nullable=False)
    create_time = db.Column(db.DateTime)

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

def get_all_children(session, node_name):
    # 定义一个递归函数来构建树
    all_len = []
    user_level={'0':'超级管理员','1':'管理员','2':'组长','3':'组员'}
    def build_tree(father_name,root_alldata):
        # 查询当前节点的所有子节点

        children = [i for i in root_alldata if i['father_name'] == father_name]
        # 如果没有子节点，返回一个空列表
        if not children:
            return []
        all_len.extend([i['user_name'] for i in children])
        # 为每个子节点创建一个字典，并递归构建其子树
        my_result = []
        for child in children:
            #print(child)
            inner_result = build_tree(child['user_name'],root_alldata)
            my_result.append({
                'user_id': child['user_id'],
                'user_name': child['user_name'],
                'name': child['user_name'],
                'father_name': father_name,
                'create_time': str(child['create_time']),
                'user_level': user_level[child['user_level']],
                'parentId':father_name,
                'children': inner_result,  # 递归调用构建子节点的树
                'isParent': len(inner_result) > 0  # 判断当前节点是否有子节点
            })
        return my_result

    # 从根节点开始构建树
    root_alldata=[i.to_dict() for i in session.query.all()]
    #print(root_alldata)
    root_data1=session.query.filter_by(user_name=node_name).first()
    all_len.append(root_data1.user_name)
    one_result = build_tree(node_name,root_alldata)
    return {
        'user_id':root_data1.user_id,
        'user_name': node_name,
        'name': node_name,
        'father_name':root_data1.father_name,
        'create_time':str(root_data1.create_time),
        'user_level':user_level[root_data1.user_level],
        'parentId': None,
        'children': one_result,  # 调用递归函数构建子树
        'isParent': len(one_result) > 0  # 判断根节点是否有子节点
    },all_len

def get_all_childrenlist(session,node_name):
    node_list = [[node_name]]
    reslist = []  # 使用集合来避免重复
    while node_list:
        child_list=[]
        for i in node_list:
            child_list.extend([{j.user_name:''} for j in session.query.filter_by(father_name=i).all()])
            print(child_list)
        if not child_list:
            break
        reslist.extend(child_list)  # 添加新的子节点到结果集
        node_list = child_list  # 更新下一轮的节点列表

    return list(reslist)

def get_shop(shop_name):
    class Shop_Temp(db.Model):
        __tablename__=shop_name
        id = db.Column(db.Integer, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey('productpnl.pid'))
        create_time = db.Column(db.DateTime)
        create_user = db.Column(db.String(60),db.ForeignKey('menber_ship.user_name'))
        owner=db.Column(db.String(20), db.ForeignKey('member_ship.user_name'))

    inspector = inspect(db.engine)
    if not inspector.has_table(shop_name):
        try:
            db.create_all()
            all_shop[shop_name] = Shop_Temp
            return Shop_Temp
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
    else:
        all_shop[shop_name]=Shop_Temp
        return Shop_Temp

def get_user_log(username):
    table_name=username+'个人日志'
    class userlog(db.Model):
        __tablename__=table_name
        id = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.Date)#指定这条日志的时间
        title = db.Column(db.String(60))#标题
        logdata = db.Column(db.Text)#内容
        status = db.Column(db.String(10))#状态，只有公开和非公开两个状态
        comment = db.Column(db.Text)#备注或评论
        level = db.Column(db.Integer)#等级，有三级：1是重要，2是普通，3是不重要
        createtime = db.Column(db.DateTime)

        def to_dict(self):
            return {
                'id': self.id,
                'date': self.date.strftime('%Y年%m月%d日'),
                'logdata': self.logdata,
                'createtime': datetime.datetime.strftime(self.createtime,'%Y-%m-%d %H:%M:%S'),
                'titile':self.title,
                'status': self.status,
                'comment': self.comment,
                'level': self.level,
            }

    inspector = inspect(db.engine)

    if not inspector.has_table(table_name):
        try:
            db.create_all()
            all_users_logs[table_name] = userlog
            return userlog
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
    else:
        all_users_logs[table_name] = userlog
        return userlog








