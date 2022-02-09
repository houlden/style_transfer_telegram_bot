import torchvision.models as models

from ml_models.nst_gatys.image_preparation import image_loader, save_image
from ml_models.nst_gatys.settings import DEVICE, NORMALIZATION_MEAN, NORMALIZATION_STD
from ml_models.nst_gatys.train_loop import style_transfer_loop


async def run(style_path, content_path, output_path):
    style_image = image_loader(style_path)
    content_image = image_loader(content_path)
    input_image = content_image.clone()

    normalization_mean = NORMALIZATION_MEAN.to(DEVICE)
    normalization_std = NORMALIZATION_STD.to(DEVICE)

    vgg19 = models.vgg19(pretrained=True).features.to(DEVICE).eval()

    output_image = await style_transfer_loop(vgg19, normalization_mean, normalization_std, content_image, style_image,
                                             input_image)

    save_image(output_image, output_path)
