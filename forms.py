from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
'''
使用WTF需要自定义表单类
相当于原来的<form><label>xx</label><input type=""></form>
'''
#定义文件提交表单
class UploadFileForm(FlaskForm):
    lands_file = FileField(u'请上传您的地块文件:', validators=[FileRequired(),FileAllowed(['csv'], 'csv only!')])
    routes_file = FileField(u'请上传您的路径文件:', validators=[FileRequired(),FileAllowed(['csv'], 'csv only!')])
    barriers_file = FileField(u'请上传您的障碍物文件:', validators=[FileRequired(),FileAllowed(['csv'], 'csv only!')])
    parameters_file = FileField(u'请上传您的农机参数文件:', validators=[FileRequired(),FileAllowed(['csv'], 'csv only!')])
    submit = SubmitField(u'提交')

