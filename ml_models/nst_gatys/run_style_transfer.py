import io
import torch


from ml_models.nst_gatys.image_preparation import image_loader_from_RAM, save_image_RAM
from ml_models.nst_gatys.settings import DEVICE, NORMALIZATION_MEAN, NORMALIZATION_STD, CNN_PRETRAINED_PATH
from ml_models.nst_gatys.train_loop import style_transfer_loop


def run(style_image: io.BytesIO, content_image: io.BytesIO):
    """
    Преобразует изображения в тензор, приводит их к общему размеру, загружает модель и запускает стилизацию.

    :param style_image: io.BytesIO - изображение style
    :param content_image: io.BytesIO - изображение content
    :return: io.BytesIO
    """
    style_image = image_loader_from_RAM(style_image)
    content_image = image_loader_from_RAM(content_image)
    input_image = content_image.clone()

    normalization_mean = NORMALIZATION_MEAN.to(DEVICE)
    normalization_std = NORMALIZATION_STD.to(DEVICE)

    # Чтобы каждый раз не грузить веса всей VGG19 (~600 МБ) через интернет загрузим предварительно сохраненную сеть
    # и веса её первых 11-ти слоев до 5-й свертки включительно (~2 МБ)
    vgg19 = torch.load(CNN_PRETRAINED_PATH, map_location=DEVICE).to(DEVICE).eval()

    output_image = style_transfer_loop(vgg19, normalization_mean, normalization_std, content_image, style_image,
                                       input_image)

    return save_image_RAM(output_image)
