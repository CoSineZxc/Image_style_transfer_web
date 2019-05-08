from __future__ import print_function
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.optim as optim
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
import torchvision.models as models
import copy
from app.img_op import image_loader, image_unloader, img_show
from app.Loss import ContentLoss, GramMatrix, StyleLoss
from app.NN_Crt import run_style_transfer
from Image_Style_Transfer import settings


def Img_Style_Transfer(Style_imgdir, Cont_imgdir):
    ############################### GPU判断 ###############################
    use_cuda = torch.cuda.is_available()
    dtype = torch.cuda.FloatTensor if use_cuda else torch.FloatTensor

    ############################### 载入风格图像及内容图像 ###############################
    imsize = 256 if use_cuda else 128  # use small size if no gpu
    style_img = image_loader(Style_imgdir, imsize)[0].type(dtype)
    content_img, (imgwidth, imgheight) = image_loader(Cont_imgdir, imsize)
    content_img = content_img.type(dtype)
    # 异常退出
    assert style_img.size() == content_img.size(), \
        "we need to import style and content images of the same size"

    ############################### 显示图像 ###############################
    # img_show(style_img, imsize, title='Style Image')
    # img_show(content_img.data, imsize, title='Content Image')

    ############################### 神经网络搭建 ###############################
    cnn = models.vgg19(pretrained=True).features
    if use_cuda:
        cnn = cnn.cuda()
    # 风格损失及内容损失的插入位置
    content_layers_default = ['conv_4']
    style_layers_default = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']

    ############################### 载入输入图像 ###############################
    input_img = content_img.clone()

    ############################### 模型训练 ###############################
    output = run_style_transfer(cnn, content_img, style_img, input_img, use_cuda)

    img_show(output, imsize, title='Output Image')
    stl = Style_imgdir.split('/')[-1]
    stl = stl.split('.')[0]
    cnt = Cont_imgdir.split('/')[-1]
    cnt = cnt.split('.')[0]
    outputdir=settings.OUTPUTFILES_DIRS + '/' + stl + "_" + cnt + ".jpg"
    image_unloader(outputdir, output, imgheight, imgwidth)


# Img_Style_Transfer("Img/style/style7.jpg", "Img/content/cont3.jpg")
