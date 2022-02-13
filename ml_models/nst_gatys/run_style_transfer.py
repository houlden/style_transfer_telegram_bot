import torch


from ml_models.nst_gatys.image_preparation import image_loader, save_image
from ml_models.nst_gatys.settings import DEVICE, NORMALIZATION_MEAN, NORMALIZATION_STD, CNN_PRETRAINED_PATH
from ml_models.nst_gatys.train_loop import style_transfer_loop


def run(style_path, content_path, output_path):
    style_image = image_loader(style_path)
    content_image = image_loader(content_path)
    input_image = content_image.clone()

    normalization_mean = NORMALIZATION_MEAN.to(DEVICE)
    normalization_std = NORMALIZATION_STD.to(DEVICE)

    # Чтобы каждый раз не грузить веса всей VGG19 (~600 МБ) через интернет загрузим предварительно сохраненную сеть
    # и веса её первых 11-ти слоев до 5-й свертки включительно (~2 МБ)
    vgg19 = torch.load(CNN_PRETRAINED_PATH, map_location=DEVICE)

    output_image = style_transfer_loop(vgg19, normalization_mean, normalization_std, content_image, style_image,
                                       input_image)

    save_image(output_image, output_path)

    with open(output_path, 'rb') as f:
        return f.read()
