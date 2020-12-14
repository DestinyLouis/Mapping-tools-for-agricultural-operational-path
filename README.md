# Mapping-tools-for-agricultural-operational-path
Based on leaflet

使用方法：
运行 app.py 文件
-->进入路由主页 http://127.0.0.1:5000/ 
-->上传csv文件，回到主页加载数据
-->使用修改工具进行修改
-->下载修改后路径文件

12.14
bug描述：
测试文件 curve.html 和 app.py中的路由 /curve ，template只能向前端传一次数据，但是后端传前端用ajax正常，后端的判断值m也在变。
