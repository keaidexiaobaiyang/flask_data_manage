from http.client import responses
from json import JSONDecodeError

from flask import Blueprint, render_template,request,jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required,current_user
from app.models import users,Productpnl,get_all_children,db,shopConfig,shop_sub_counrt,product_code,get_all_childrenlist,ProductConfig
from sqlalchemy import and_
import datetime
import requests as rq
import json

managehome_bp = Blueprint('managehome',__name__)

#管理中心主页
@managehome_bp.route('/managehome')
#@login_required
def managehome():
    return render_template('管理中心/ManageHome.html')

#管理成员管理部分
@managehome_bp.route('/managehome/membermanage')
#@login_required
def membermanage():
    return render_template('管理中心/MemberManage.html')

#店铺管理部分
@managehome_bp.route('/managehome/shopmanage')
#@login_required
def shopmanage():
    data, _ = get_all_children(users, '迪维')
    _,all_user = get_all_children(users, current_user.user_name)
    need_list=[[i['user_name']]+[j['user_name'] for j in i['children']] for i in data['children']]
    print(need_list,all_user)
    return render_template('管理中心/ShopManage.html',users=need_list)

#更新店铺信息
@managehome_bp.route('/managehome/shopmanageupdate',methods=['GET','POST'])
def shopmanageupdate():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data,type(data))
            if data is None:
                return jsonify({'error': '未提交任何字段'}), 400
            else:
                shop_data=shopConfig.query.filter_by(id=data['id']).first().to_dict()
                print(shop_data,type(shop_data))
                _, all_user = get_all_children(users, current_user.user_name)
                if shop_data['owner'] in all_user:
                    print('可以修改')
                    flag = True
                    for i in ['owner','shop_name']:
                        if i in data.keys():
                            if shop_data[i] != data[i]:
                                flag = False
                                print(shop_data[i],data[i])
                                setattr(shopConfig.query.filter_by(id=data['id']).first(), i, data[i])
                        else:
                            continue
                    if flag:
                        print('未修改')
                        return jsonify({'data': '未修改任何属性'}), 200
                    print('已修改')
                    try:
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                    return jsonify({'data': data}), 200
                else:
                    return jsonify({'error':'您无权修改不属于您的店铺'}), 400
            # 处理数据
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON format'}), 400

#删除店铺信息
@managehome_bp.route('/managehome/shopmanagedelete',methods=['GET','POST'])
def shopmanagedelete():
    if request.method == 'POST':
        try:
            data = request.get_json()
            shop_list=data.split('\n')
            _, all_user = get_all_children(users, current_user.user_name)
            print(shop_list)
            not_you=[]
            success_list=[]
            fails_list=[]
            for i in shop_list:
                if shopConfig.query.filter_by(shop_name=i).first().to_dict()['owner'] not in all_user:
                    not_you.append(i)
            if not_you:
                return jsonify({'status2': 'error','message': f'这些店并不归您管：{",".join(not_you)}'}),400
            if int(users.query.filter_by(user_name=current_user.user_name).first().to_dict()['user_level']) > 2:
                return jsonify({'status2': 'error','message': '您的权限太低了，请联系您的上级删除'}),400
            for i in shop_list:
                query=shopConfig.query.filter_by(shop_name=i).first()
                print(query)
                if query:
                    try:
                        db.session.delete(query)
                        success_list.append(i)
                        db.session.commit()
                        print('删除成功')
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                        fails_list.append(i)
            return jsonify({'status2': 'success','message':f'成功的店：{",".join(success_list)},失败的店：{",".join(fails_list)}'}), 200
        except json.JSONDecodeError:
            return jsonify({'status2': 'error','message': 'Invalid JSON format'}), 400
        except Exception as ex:
            print(ex)
            return jsonify({'status2': 'error','message': 'An internal error occurred'}), 400

#添加店铺信息
@managehome_bp.route('/managehome/shopmanageadd',methods=['GET','POST'])
def shopmanageadd():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data,type(data))
            user_flag = users.query.filter_by(user_name=data['owner']).first()
            shop_flag = shopConfig.query.filter_by(shop_name=data['shop_name']).first()
            if not user_flag:
                return jsonify({'message': '用户不存在'}), 400
            elif shop_flag:
                return jsonify({'message': '店铺已存在'}), 400
            else:
                user_new = shopConfig(
                    shop_name=data['shop_name'],
                    create_time=datetime.datetime.now(),
                    create_user=current_user.user_name,
                    owner=data['owner'],
                )
                db.session.add(user_new)
                db.session.commit()
                try:
                    db.session.commit()
                    return jsonify('修改成功'), 200
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return jsonify({'message': '上传数据库异常，已回滚'}), 400
        except JSONDecodeError:
            return jsonify({'message': 'Invalid JSON format'}), 400
        except Exception as ex:
            print(ex)
            return jsonify({'message': 'An internal error occurred'}), 400

@managehome_bp.route('/managehome/shopmanagesub',methods=['GET','POST'])
def shopmanagesub():
    param = request.args
    print(param)
    shopname = '冰柠的小店'
    if param:
        if 'shopname' in param.keys():
            shopname = param['shopname']
    return render_template('管理中心/ShopSubManage.html', shopname=shopname)
    # if request.method == 'get':
    #     param=request.args.get('param')
    #     if 'shopname' in param.keys():
    #
    #         shopname=param['shopname']
    #     else:
    #         shopname='冰柠的小店'
    #     return render_template('管理中心/ShopSubManage.html',shopname=shopname)
    # else:
    #     return jsonify('sb')

#添加子账号信息
@managehome_bp.route('/managehome/shopmanageaddsub',methods=['GET','POST'])
def shopmanageaddsub():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(data,type(data))
            user_list=get_all_childrenlist(users,current_user.user_name)
            user_flag = users.query.filter_by(user_name=data['user_name']).first()
            shop_flag = shopConfig.query.filter_by(shop_name=data['shop_name']).first()
            user_all = shop_sub_counrt.query.filter(and_(shop_sub_counrt.user_name == data['user_name'], shop_sub_counrt.shop_name == data['shop_name'])).first()
            shop_flag_dict=shop_flag.to_dict()
            print('shop_flag_dict',shop_flag_dict)
            if shop_flag_dict['owner'] not in user_list:
                return jsonify({'message': '您无权为不属于自己的店铺添加子账号'}), 400
            if not user_flag:
                return jsonify({'message': '用户不存在'}), 400
            elif not shop_flag:
                return jsonify({'message': '店铺不存在'}), 400
            elif user_all:
                return jsonify({'message': '该子账号已存在'}), 400
            else:
                sub_new = shop_sub_counrt(
                    shop_name=data['shop_name'],
                    create_time=datetime.datetime.now(),
                    create_user=current_user.user_name,
                    user_name=data['user_name'],
                )
                db.session.add(sub_new)
                try:
                    db.session.commit()
                    return jsonify('修改成功'), 200
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    return jsonify({'message': '上传数据库异常，已回滚'}), 400
        except JSONDecodeError:
            return jsonify({'message': 'Invalid JSON format'}), 400
        except Exception as ex:
            print(ex)
            return jsonify({'message': f'An internal error occurred{ex}'}), 400

#删除子账号信息
@managehome_bp.route('/managehome/shopmanagedeletesub',methods=['GET','POST'])
def shopmanagedeletesub():
    if request.method == 'POST':
        try:
            data = request.get_json()
            shop_list=data.split('\n')
            _, all_user = get_all_children(users, current_user.user_name)
            print(shop_list)
            success_list=[]
            fails_list=[]
            if int(users.query.filter_by(user_name=current_user.user_name).first().to_dict()['user_level']) > 2:
                return jsonify({'status2': 'error','message': '您的权限太低了，请联系您的上级删除'}),400
            for i in shop_list:
                query=shop_sub_counrt.query.filter_by(user_name=i).first()
                print(query)
                if query:
                    try:
                        db.session.delete(query)
                        success_list.append(i)
                        db.session.commit()
                        print('删除成功')
                    except Exception as e:
                        print(e)
                        db.session.rollback()
                        fails_list.append(i)
            return jsonify({'status2': 'success','message':f'成功的账号：{",".join(success_list)}\n,失败的账号：{",".join(fails_list)}'}), 200
        except json.JSONDecodeError:
            return jsonify({'status2': 'error','message': 'Invalid JSON format'}), 400
        except Exception as ex:
            print(ex)
            return jsonify({'status2': 'error','message': 'An internal error occurred'}), 400

#商品管理部分
@managehome_bp.route('/managehome/productmanage')
#@login_required
def productmanage():
    return render_template('管理中心/ProductManage.html')

#商品更新
@managehome_bp.route('/managehome/productmanageupdate',methods=['GET','POST'])
def productmanageupdate():
    return '1'

#商品删除
@managehome_bp.route('/managehome/productmanagedelete',methods=['GET','POST'])
def productmanagedelete():
    return '2'

#商品添加
@managehome_bp.route('/managehome/productmanageadd',methods=['GET','POST'])
def productmanageadd():
    return '3'

#返回编码中心
@managehome_bp.route('/managehome/productcodemanage')
def productcodemanage():
    return render_template('管理中心/PruductCodeManage.html')

#更新编码
@managehome_bp.route('/managehome/productcodemanageupdate',methods=['GET','POST'])
def productcodemanageupdate():
    return '4'

#删除编码
@managehome_bp.route('/managehome/productcodemanagedelete',methods=['GET','POST'])
def productcodemanagedelete():
    return '5'

#添加编码
@managehome_bp.route('/managehome/productcodemanageadd',methods=['GET','POST'])
def productcodemanageadd():
    return '6'

@managehome_bp.route('/managehome/productcodemanagedata',methods=['GET','POST'])
def productcodemanagedata():
    print(request.args)
    query=product_code.query.paginate(page=int(request.args['page']), per_page=int(request.args['limit']) )
    data=[i.to_dict() for i in query]
    json_data=jsonify({
        'code':0,
        'count':query.total,
        'data':data
    })
    return json_data
#组织架构展示
@managehome_bp.route('/managehome/groupshow')
#@login_required
def groupshow():
    return render_template('管理中心/GroupShow.html')

#获取组织成员树
@managehome_bp.route('/managehome/getusertree',methods=['GET','POST'])
@login_required
def getusertree():
    if request.method == 'GET':
        username=request.args.get('username')
        print(username)
        if username:
            name=username
        else:
            name = current_user.user_name
        data,data_len=get_all_children(users,name)
        print(data_len)
        result_data={
            "code": 0,
            "msg": "",
            "count": len(data_len),
            "data": [data]
        }
        jsondata=json.dumps(result_data,ensure_ascii=False)
        print(jsondata)
        return jsondata
    elif request.method == 'POST':
        try:
            data = json.loads(request.data)
        except json.JSONDecodeError:
            return jsonify({'status': 'error', 'message': '无效的 JSON 数据'}), 200
        user_data = users.query.filter_by(user_name=current_user.user_name).first().to_dict()
        all_user = [j.to_dict()['user_name'] for j in users.query.all()]
        if int(user_data['user_level']) > 2:
            return jsonify({'status': 'error', 'message': '您的权限过低，无法提交'}), 200
        _, data_len = get_all_children(users, current_user.user_name)
        #print(data_len,data)
        if 'father_name' not in data or data['father_name'] not in data_len:
            return jsonify({'status': 'error', 'message': '您无权操作不属于自己的用户'}), 200
        if data['user_name'] in all_user:
            return jsonify({'status': 'error', 'message': '该用户名已被使用了哦~亲'}), 200
        if int(user_data['user_level']) >= int(data['user_level']):
            return jsonify({'status': 'error', 'message': '该成员的等级不可以比你厉害哦~'}), 200
        else:
            try:
                # 确保所有需要的键都存在
                required_keys = ['user_name', 'father_name', 'create_time', 'user_level']
                if not all(key in data for key in required_keys):
                    raise ValueError("Missing required data")

                # 创建新用户记录
                if data['user_id'] == 0:
                    user_new = users(
                        user_name=data['user_name'],
                        father_name=data['father_name'],
                        create_time=data['create_time'],
                        user_level=str(data['user_level']),
                        permision_level=str(data['user_level']+1),
                        user_password='123456',  # 使用密码哈希
                        owner=data['user_name']
                    )
                    db.session.add(user_new)
                    db.session.commit()
                else:
                    user_to_update = users.query.filter_by(user_id=data['user_id']).first()
                    user_to_update.user_name=data['user_name']
                    db.session.commit()

            except Exception as e:
                db.session.rollback()  # 发生异常时回滚
                print(f"An error occurred: {e}")
                return jsonify({'status': 'success', 'message': f'出现了点意外{e}'}), 200
            return jsonify({'status': 'success', 'message': '修改成功'}), 200
    else:
        return 'sb'

#删除成员
@managehome_bp.route('/managehome/deleteuser',methods=['POST'])
@login_required
def deleteuser():
    try:
        data = json.loads(request.data)
    except json.JSONDecodeError:
        return jsonify({'status': 'error', 'message': '无效的 JSON 数据'}), 200
    _, data_len = get_all_children(users, current_user.user_name)
    # print(data_len,data)
    if data['father_name'] not in data_len:
        return jsonify({'status': 'error', 'message': '您无权操作不属于自己的用户'}), 200
    user_data = users.query.filter_by(user_name=current_user.user_name).first().to_dict()
    all_user = [j.to_dict()['user_name'] for j in users.query.all()]
    if int(user_data['user_level']) > 2:
        return jsonify({'status': 'error', 'message': '您的权限过低，无法删除'}), 200
    user_data = users.query.filter_by(user_id=int(data['user_id'])).first()
    if user_data:
        # 删除记录
        try:
            db.session.delete(user_data)
            db.session.commit()
            return jsonify({'status': 'success', 'message': f'damn,终于成功'}), 200
        except Exception as e:
            db.session.rollback()  # 发生异常时回滚
            print(f"An error occurred: {e}")
            return jsonify({'status': 'error', 'message': f'出现了点意外{e}'}), 200
    else:
        return jsonify({'status': 'error', 'message': '不存在的id'}), 200

#获取店铺信息
@managehome_bp.route('/managehome/getshop',methods=['GET'])
#@login_required
def getshop():
    if request.method == 'GET':
        data=request.data
        args=request.args
        print(data,args)
        query = []
        if '店铺名' in args:
            query.append(shopConfig.shop_name.like(f'%{args["店铺名"]}%'))
        if '用户' in args:
            query.append(shopConfig.owner.like(f'%{args["用户"]}%'))
        print(query)
        shopdata=shopConfig.query.filter(and_(*query)).paginate(page=int(request.args['page']), per_page=int(request.args['limit']) )
        print(data)
        result_list=[]
        for i in shopdata:
            temp=i.to_dict()
            temp['create_time']=datetime.datetime.strftime(temp['create_time'],'%Y-%m-%d %H:%M:%S')
            result_list.append(temp)
        responses=jsonify({
            "code": 0,
            'count':shopdata.total,
            'data':result_list,
        })
        return responses

#获取店铺子账号信息
@managehome_bp.route('/managehome/getshopsub',methods=['GET'])
#@login_required
def getshopsub():
    if request.method == 'GET':
        data=request.data
        args=request.args
        print(data,args)
        query = []
        if 'shopname' in args:
            query.append(shop_sub_counrt.shop_name.like(f'%{args["shopname"]}%'))
        if '用户' in args:
            query.append(shop_sub_counrt.user_name.like(f'%{args["用户"]}%'))
        print(query)
        shopdata=shop_sub_counrt.query.filter(and_(*query)).paginate(page=int(request.args['page']), per_page=int(request.args['limit']) )
        print(data)
        result_list=[]
        for i in shopdata:
            temp=i.to_dict()
            temp['create_time']=datetime.datetime.strftime(temp['create_time'],'%Y-%m-%d %H:%M:%S')
            result_list.append(temp)
        responses=jsonify({
            "code": 0,
            'count':shopdata.total,
            'data':result_list,
        })
        print(responses)
        return responses

@managehome_bp.route('/managehome/getpruduct',methods=['GET'])
def getpruduct():
    if request.method == 'GET':
        sql_data=ProductConfig.query.all()

        data=jsonify({
            "code": 0,
            'count':len(sql_data),
            'data':[i.to_dict() for i in sql_data],
        })
        return data
