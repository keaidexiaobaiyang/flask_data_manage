###### 2024-12-04 Wed:

​    新建项目，并git init

网站结构路由：
    1、主界面（main.py）：主界面路由是main,包含两个函数：index(返回主界面的html文件同时计算当前登录的账号有关的店铺信息)、warining(返回错误界面)
    2、登录(login.py)：主界面的路由是login。
        (1)login.login:如果是get请求，则返回登录界面的html，如果是post请求，则会想服务端提交当前界面填写的账号密码信息。
        (2)login.return_user:测试所有用户
        (3)login.loginout:推出当前推出的用户
    3、管理中心(managehome.py):
        (1)managehome.managehome:返回管理中心的html文件。
        (2)managehome.getusertree:如果是get请求，则返回当前用户和用户所有的子、孙节点。
        (3)managehome.changeuser:更改用户数据的请求。（待制作）
        (4)店铺管理：待制作
        (5)修改数据库功能。
    4、数据中心(data.py)：
        (1)datahome.datahome:暂时没用上
        (2)datahome.get_data:获取数据从数据库中，包含有产品id参数、获取的数量、获取的列属性。
        (3)datahome.get_data_ZG:返回折线图界面。
    5、数据展示(showdata):
        (1)showdata.showdata:返回数据展示界面。
        (2)showdata.getdata:数据展示界面的初始化数据。
    6、用户中心(userhome):
        (1)userhome.userhome:返回用户中心html界面。
        (2)userhome.userhome_data:返回用户中心初始化需要的数据。
网站静态网站：
    1、main.html:返回的主界面。
    2、logon.html:登录界面。
    3、managehome:管理界面。
    4、datahome:数据中心界面。（没做）
    5、showdata:盈亏表数据展示界面。
    6、data_ZG：盈亏表折线图展示界面。
    7、user_home:用户中心，展示和用户有关的信息。（没有数据筛选功能）
    8、warning:展示警告界面。