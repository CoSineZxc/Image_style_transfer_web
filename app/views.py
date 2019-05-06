from django.shortcuts import render
import os
import json
from Image_Style_Transfer import settings
from app import img_trans
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'index.html')  # 上传index.html文件到templates目录下


def upload_picture(request):
    if request.method == 'POST':  # 请求方法为POST时，进行处理
        myFile = request.FILES.get('file')  # 获取上传的文件，如果没有文件，则默认为None
        type = request.POST.get('type')
        dirs = settings.INPUTFILES_DIRS
        if type == "1":
            dirs = settings.INPUTFILES_DIRS
        elif type == "2":
            dirs = settings.CUSTOMER_STYLEFILES_DIRS
        print(dirs)
        if not myFile:
            return HttpResponse('上传失败')
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        destination = open(os.path.join(dirs, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()
        return HttpResponse("上传成功")


def trans_picture(request):
    filename1 = request.POST.get('filename1')  # 原始图片
    filename2 = request.POST.get('filename2')  # 风格图片
    type = request.POST.get('type')  # 由type判断风格图片是默认还是由用户上传
    dir_input = settings.INPUTFILES_DIRS + '/' + filename1  # 原始图片路径
    dir_style = settings.CUSTOMER_STYLEFILES_DIRS + '/' + filename2  # 风格图片路径
    if type == "default":
        dir_style = settings.DEFAULT_STYLEFILES_DIRS + '/' + filename2
    elif type == "customer":
        dir_style = settings.CUSTOMER_STYLEFILES_DIRS + '/' + filename2
    dict = {}
    print(dir_input)
    print(dir_style)
    img_trans.Img_Style_Transfer(dir_style,dir_input)  # 接口示例，dir_input为原始图片路径, dir_style为风格图片路径
    filename1 = filename1.split('.')[0]
    filename2 = filename2.split('.')[0]

    dict['filename'] = filename2+'_'+filename1+".jpg"
    data = json.dumps(dict)
    return HttpResponse(data)
