#encoding: utf-8

#Config类在config模块中定义
import os

#base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Database configuration
    DIALECT = 'mysql'
    DRIVER = 'pymysql'
    USERNAME = 'root'
    PASSWORD = '123456'
    HOST = 'localhost'
    PORT = '3306'
    DATABASE = 'flask_test'
    # 连接数据库, url的格式为：数据库的协议：//用户名：密码@ip地址：端口号（默认可以不写）/数据库名
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)

    # 设置是否跟踪数据库的修改情况，一般不跟踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 每次请求结束后都会自动提交数据库中的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 数据库操作时是否显示原始SQL语句，一般都是打开的，因为我们后台要日志
    SQLALCHEMY_ECHO = True

    #configuration for flask-wtf
    SECRET_KEY = os.urandom(6)