# encoding: utf-8
import os
import sys
import csv
import json

from flask import Flask, render_template, request, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from barriers import barriers
from curvature import curvature
from lands import lands
from routes import routes
from upload import csv2json, gen_name
from config import Config
from forms import UploadFileForm
import models as md


# 创建Flask  ，实例化app


app = Flask(__name__)
app.config.from_object(Config)  # 关联config.py文件进来
db = SQLAlchemy(app)  # 建立数据库的关系映射



bootstrap = Bootstrap(app)  # 应用Bootstrap

#服务器临时文件夹，json保存根目录，分目录名
files_tmp = u'C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\files_tmp\\'
json_root = u'C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\json\\'
json_name = ['lands_json\\', 'routes_json\\', 'barriers_json\\', 'parameters_json\\']

fieldname = [['id', 'latitude', 'longtitude', 'altitude'],
                 ['id', 'latitude', 'longtitude', 'engine_speed', 'operate_mode'],
                 ['name', 'latitude', 'longtitude', 'altitude'],
                 ['id', 'operating_width', 'turning_radius','total_length', 'total_width']]
filenum = 0

#主页
@app.route('/', endpoint='toolbar')
def index():
    title = 'Flask App'
    #从数据库获取地块信息
    lands_tuple = db.session.query(md.Land.latitude, md.Land.longtitude).all()
    location_mid, lands_list = lands(lands_tuple)

    #从数据库获取路径信息
    routes_tuple = db.session.query(md.Route.latitude, md.Route.longtitude, md.Route.operate_mode).all()
    routes_list = routes(routes_tuple)

    #从数据库获取障碍物信息
    barriers_tuple = db.session.query(md.Barrier.name, md.Barrier.latitude, md.Barrier.longtitude).all()
    Circle, Line4points = barriers(barriers_tuple)

    return render_template('toolbar.html', title=title, location_mid_json=json.dumps(location_mid), lands_list_json=json.dumps(lands_list), routes_list_json=json.dumps(routes_list), Circle_json=json.dumps(Circle), Line4points_json=json.dumps(Line4points))

#下载文件页
@app.route('/download', endpoint='download')
def download():
    return render_template('download.html')

#上传文件页
@app.route('/upload/', endpoint='upload', methods=['GET', 'POST'])
def upload():
    uff = UploadFileForm()
    filenames = []
    if uff.validate_on_submit():
    #filepath = 'C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\农机作业路径地图可视化与修正工具Web开发\\农机作业路径地图可视化与修正工具Web开发\\' + uff.lands_file.data.filename
    # print(filepath)
    #获取文件名并保存csv文件到服务器临时文件夹C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\csv_tmp\\csv_tmp

        filenames.append(uff.lands_file.data.filename)
        filenames.append(uff.routes_file.data.filename)
        filenames.append(uff.barriers_file.data.filename)
        filenames.append(uff.parameters_file.data.filename)
        print(filenames)
        print(type(filenames))
        #获取当前存储的json文件数量
        filenum = len(os.listdir(json_root + json_name[0]))
        print(filenum)
        flash(u'上传成功')

    for file_type in range(len(filenames)):
            csv_path = files_tmp + filenames[file_type]
            print(csv_path)
            if file_type == 0:
                uff.lands_file.data.save(csv_path)
            elif file_type == 1:
                uff.routes_file.data.save(csv_path)
            elif file_type == 2:
                uff.barriers_file.data.save(csv_path)
            elif file_type == 3:
                uff.parameters_file.data.save(csv_path)

            # 调用csv2json，生成标准数据到json文件
            #json_path = json_root + json_name[file_type] + json_partname[file_type] + str(filenum) + '.json'
            json_path = json_root + json_name[file_type] + gen_name(file_type, filenum)
            print(json_path)
            flash(u'正在导入文件数据...')
            csv2json(json_path, csv_path, file_type)

            #保存数据到数据库
            with open(csv_path, 'r') as cf:
                # 创建csv读取器
                reader = csv.DictReader(cf, fieldname[file_type])
                # 读掉原来表头
                try:
                    next(reader)
                except StopIteration:
                    sys.exit()

                for row in reader:
                    # 只有农机参数中不涉及经纬度方向问题
                    if file_type != 3:
                        if row['latitude'][-1] == 'N':
                            row['latitude'] = row['latitude'][0:-1]
                        elif row['latitude'][-1] == 'S':
                            row['latitude'] = '-' + row['latitude'][0:-1]

                        if row['longtitude'][-1] == 'E':
                            row['longtitude'] = row['longtitude'][0:-1]
                        elif row['longtitude'][-1] == 'W':
                            row['longtitude'] = '-' + row['longtitude'][0:-1]

                    # 保存到数据库
                    if file_type == 0:
                        data = md.Land(latitude=row['latitude'],
                                       longtitude=row['longtitude'],
                                       altitude=row['altitude'])
                    elif file_type == 1:
                        data = md.Route(latitude=row['latitude'],
                                        longtitude=row['longtitude'],
                                        engine_speed=row['engine_speed'],
                                        operate_mode=row['operate_mode'])
                    elif file_type == 2:
                        data = md.Barrier(name=row['name'],
                                          latitude=row['latitude'],
                                          longtitude=row['longtitude'],
                                          altitude=row['altitude'])
                    elif file_type == 3:
                        data = md.Parameter(operating_width=row['operating_width'],
                                            turning_radius=row['turning_radius'],
                                            total_length=row['total_length'],
                                            total_width=row['total_width'])
                    db.session.add(data)
                    db.session.commit()

    #节约服务器空间，删除已经生成过json文件的相应csv文件
    for file in os.listdir(files_tmp):
        os.remove(files_tmp + file)

    return render_template('upload.html', form=uff)

@app.route('/my_leaflet')
def my_leaflet():
    return render_template('my_leaflet.html')

@app.route('/test')
def test():
    return render_template('test.html')
# @app.route('/upload_landfile', methods=['GET', 'POST'])
# def upload_landfile():
#     recv_data = request.get_data()
#     print(recv_data)
#     return render_template('index.html')


@app.route('/show_map')
def show_map():
    return render_template('map.html')


@app.route('/user_add')
def user_add():
    u1 = md.User(user_name='zbz', email='zbz@qq.com')
    u2 = md.User(user_name='wzx', email='wzx@qq.com')
    # 添加记录
    db.session.add(u1)
    db.session.add(u2)
    # 必须有提交动作才能执行添加指令，增删改都是最后需要下面的提交命令
    db.session.commit()

    return "OK"


@app.route('/route')
def route():
    route_list = db.session.query(md.Route.latitude, md.Route.longtitude).all()
    # user_list = md.User.query.order_by(md.User.id).all()
    # print(md.User.user_name, md.User.email)
    #print(type(route_list))
    #print(route_list)

    return render_template("users.html", route_list=route_list)
    # return 'ok'


@app.route('/routes')
def routes_map():
    routes_tuple = db.session.query(md.Route.latitude, md.Route.longtitude, md.Route.operate_mode).all()
    routes_list = routes(routes_tuple)

    lands_tuple = db.session.query(md.Land.latitude, md.Land.longtitude, md.Land.altitude).all()
    lands_list = lands(lands_tuple)

    barriers_tuple = db.session.query(md.Barrier.latitude, md.Barrier.longtitude, md.Barrier.altitude).all()
    barriers_list = barriers(barriers_tuple)

    return render_template('toolbar.html', lands_list_json=json.dumps(lands_list), routes_list_json=json.dumps(routes_list), barriers_list_json=json.dumps(barriers_list))

'''@app.route('/curve')
def curve():
    data = [[39.581396912637935, 116.13201141357422],
            [39.626868974000274, 116.24084472656251],
            [39.6107456716115, 116.35620117187501],
            [39.52319146034901, 116.37577056884767],
            [39.48797993746985, 116.23775482177736],
            [39.39824963706614, 116.18316650390626],
            [39.38021664686007, 116.41456604003908]]

    # data2 = [[50.54136296522163, 28.520507812500004],
    #          [52.214338608258224, 28.564453125000004],
    #          [48.45835188280866, 33.57421875000001],
    #          [50.680797145321655, 33.83789062500001],
    #          [47.45839225859763, 31.201171875],
    #          [48.40003249610685, 28.564453125000004]]
    return render_template('curve2.html', data_json=json.dumps(data))
    '''

# @app.route('/curve2_k', methods=['GET', 'POST'])
# def curve():
#     if request.method == 'POST':
#         m = '0'
#         points = request.get_json()
#         # points = list(points)
#         print(points)
#         print(type(points))
#         R = 0
#
#         if points != None:
#             for i in range(1001):
#                 t = i / 1000
#                 r = curvature(t, points[0], points[1], points[2], points[3])
#                 if r > R:
#                     R = r
#             turningR = 10
#             print(R)
#             if R >= turningR:
#                 m = '1'
#                 print(m)
#             else:
#                 m = '0'
#                 print(m)
#
#     # turningR = db.session.query(md.Parameter.turning_radius).all()
#
#     #return render_template('curve2_k.html', m_json=json.dumps(m))
#
#     return render_template('curve2_k.html', m)

if __name__ == '__main__':
    # 需要写在model.py文件中才生效，且这个只是用于开发过程中的测试之用
    # 删除所有的表
    # db.drop_all()
    # 创建表
    # db.create_all()
    app.run(debug=True)
    bootstrap.run()
