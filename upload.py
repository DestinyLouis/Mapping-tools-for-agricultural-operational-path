import csv
import json
import sys


import threading


def csv2json(json_path, csv_path, file_type):
    '''

    :param csv_path: 传入csv文件临时保存路径
    :param json_path: 转换后保存json文件到服务器文件夹路径
    :param file_type: 0~3 0-lands 1-routes 2-barriers 3-parameters
    :return:
    '''
    #json字段名，分别为：地块，路径，障碍物，农机参数
    fieldname = [['id', 'latitude', 'longtitude', 'altitude'],
                 ['id', 'latitude', 'longtitude', 'engine_speed', 'operate_mode'],
                 ['name', 'latitude', 'longtitude', 'altitude'],
                 ['id', 'operating_width', 'turning_radius','total_length', 'total_width']]
    #print(fieldname[0])

    #open csv file
    with open(json_path,'w') as jf:
        with open(csv_path,'r') as cf:
            #创建csv读取器
            reader = csv.DictReader(cf, fieldname[file_type])
            #读掉原来表头
            try:
                next(reader)
            except StopIteration:
                sys.exit()
            for row in reader:
                print(row)
                #只有农机参数中不涉及经纬度方向问题
                if file_type != 3:
                    if row['latitude'][-1] == 'N':
                        row['latitude'] = row['latitude'][0:-1]
                    elif row['latitude'][-1] == 'S':
                        row['latitude'] = row['latitude'][0:-1]
                        row['latitude'] = '-' + row['latitude']
                    if row['longtitude'][-1] == 'E':
                        row['longtitude'] = row['longtitude'][0:-1]
                    elif row['longtitude'][-1] == 'W':
                        row['longtitude'] = row['longtitude'][0:-1]
                        row['longtitude'] = '-' + row['longtitude']

                json.dump(row, jf)
                #jf.write('/n')
        # #读取第一行，这行是表头数据
        # header_row = next(reader)
        # print(header_row)
        # #读取第二行，这才是真正的读取数据
        # first_row = next(reader)
        # print(first_row)



    # filepath = open('C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\农机作业路径地图可视化与修正工具Web开发\\农机作业路径地图可视化与修正工具Web开发\\附件1：部分作业路径示例.csv','r')


#test: csv2json
# files_tmp = 'C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\files_tmp\\'
# fielname = '附件3：障碍物文件.csv'
# json_root = 'C:\\Users\\lenovo\\Desktop\\学习任务\\URP项目\\json\\'
# json_name = ['lands_json\\', 'routes_json\\', 'barriers_json\\', 'parameters_json\\']
# csv_path = files_tmp + fielname
# json_path = json_root + json_name[0] + 'lands_1.json'
# csv2json(json_path, csv_path, 0)


# def save_json():
#     '''
#     创建了threads数组，创建线程t1, 使用threading.Thread()方法，
#     在这个方法中调用music方法target = music，args方法对music进行传参。
#     把创建好的线程t1装到threads数组中。
#     最后通过for循环遍历数组。
#     '''
#     threads = []
#     t1 = threading.Thread(target, args)
#     threads.append[t1]
#     '''
#     setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，
#     如果不设置为守护线程程序会被无限挂起。
#     子线程启动后，父线程也继续执行下去，
#     当父线程执行完最后一条语句print "all over %s" %ctime()后，
#     没有等待子线程，直接就退出了，同时子线程也一同结束。
#
#     strat()开始线程
#     '''
#     for t in threads:
#         t.setDaemon()
#         t.strat()

#创建新生成的json文件名
def gen_name(file_type, num):
    file = ['lands_', 'routes_', 'barriers_', 'parameters_']
    filename = file[file_type] + str(num) + '.json'
    return filename

