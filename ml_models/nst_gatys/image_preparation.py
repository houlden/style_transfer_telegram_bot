import torchvision.transforms as transforms
import torch
from PIL import Image
import matplotlib.pyplot as plt

from ml_models.nst_gatys.settings import DEVICE, IMAGE_SIZE


transform_PIL_to_tensor_resize_and_crop = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor()
])


transform_tensor_to_PIL = transforms.ToPILImage()


def image_loader(image_path):
    try:
        with Image.open(image_path) as image:
            image = transform_PIL_to_tensor_resize_and_crop(image).unsqueeze(0)
            return image.to(DEVICE, torch.float)
    except IOError:
        print('Unable to load image')


def imshow(tensor, title=None):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = transform_tensor_to_PIL(image)
    plt.imshow(image)
    if title is not None:
        plt.title(title)
    plt.pause(10)


def save_image(tensor, path):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = transform_tensor_to_PIL(image)
    image.save(path)
