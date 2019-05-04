import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt


def image_loader(image_name, stdImgSize):
    '''
    根据文件名，将图片转化为标准大小的tensor
    '''
    loader = transforms.Compose([
        transforms.Resize((stdImgSize, stdImgSize)),  # scale imported image
        transforms.ToTensor()  # transform it into a torch tensor
    ])
    image = Image.open(image_name)
    imgsize = image.size
    image = loader(image)
    image = image.unsqueeze(0)  # 增加batch size为1的维度
    return image, imgsize


def image_unloader(image_name, image_tensor, imgHeight, imgWidth):
    '''
    根据文件名，将tensor转化为原有格式的
    '''
    unloader = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((imgHeight, imgWidth))
    ])
    image = image_tensor.cpu().clone()
    image = image.squeeze(0)
    image = unloader(image)
    image.save(image_name)


def img_show(tensor, stdImgSize, title=None):
    '''
    将tensor转化为PIL变量显示
    '''
    unloader = transforms.ToPILImage()
    image = tensor.clone().cpu()  # we clone the tensor to not do changes on it
    image = image.view(3, stdImgSize, stdImgSize)  # remove the fake batch dimension
    image = unloader(image)
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.pause(0.001)  # pause a bit so that plots are updated


# image, (ImgW, ImgH) = image_loader("Img/style/style1.jpg", 256)
# image_unloader("Img/result/rslt1.jpg", image, ImgH, ImgW)
# img_show(image, 256, "style-image1")
# image, (ImgW, ImgH) = image_loader("static/input/cont1.jpg", 256)
# image_unloader("static/output/rslt2.jpg", image, ImgH, ImgW)
# img_show(image, 256, "style-image2")