import torchvision.transforms as transforms
import torch
from PIL import Image
import io

from ml_models.nst_gatys.settings import DEVICE, IMAGE_SIZE


transform_PIL_to_tensor_resize_and_crop = transforms.Compose([
    transforms.Resize(IMAGE_SIZE),
    transforms.CenterCrop(IMAGE_SIZE),
    transforms.ToTensor()
])


transform_tensor_to_PIL = transforms.ToPILImage()


def image_loader_from_file(image_path):
    try:
        with Image.open(image_path) as image:
            image = transform_PIL_to_tensor_resize_and_crop(image).unsqueeze(0)
            return image.to(DEVICE, torch.float)
    except IOError:
        raise IOError


def image_loader_from_RAM(image):
    try:
        with Image.open(image) as image:
            image = transform_PIL_to_tensor_resize_and_crop(image).unsqueeze(0)
            return image.to(DEVICE, torch.float)
    except IOError:
        raise IOError


def save_image_disk(tensor, path):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = transform_tensor_to_PIL(image)
    image.save(path)


def save_image_RAM(tensor):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = transform_tensor_to_PIL(image)
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    buffer.seek(0)
    return buffer
