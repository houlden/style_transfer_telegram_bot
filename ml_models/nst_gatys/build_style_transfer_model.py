import torch
import torch.nn as nn
import copy

from ml_models.nst_gatys.custom_layers import Normalization, ContentLoss, StyleLoss
from ml_models.nst_gatys.settings import DEVICE, CONTENT_LAYERS, STYLE_LAYERS


def build_model_and_get_losses(cnn: nn.Module, normalization_mean: torch.Tensor, normalization_std: torch.Tensor,
                               style_img: torch.Tensor, content_img: torch.Tensor,
                               content_layers: list = CONTENT_LAYERS, style_layers: list = STYLE_LAYERS):
    """
    Собирает модель для переноса стиля из слоев предобученной сети и слоев для нормализации и вычисления loss-ов.
    Создает списки со слоями ContentLoss и StyleLoss, чтобы была возможность обратиться к их полям.

    :param cnn: nn.Module - Предобученная свёрточная нейросеть
    :param normalization_mean: torch.Tensor - Средние значения, по которым нормировалась cnn
    :param normalization_std: torch.Tensor - Стандартные отклонения, по которым нормировалась cnn
    :param style_img: torch.Tensor - Изображение content
    :param content_img: torch.Tensor - Изображение style
    :param content_layers: list - Список слоев, после которых считается content-loss
    :param style_layers: list - Список слоев, после которых считается style-loss
    :return: model: nn.Module - собранная модель, style_losses: list, content_losses: list - списки со слоями для
    подсчета loss-ов
    """
    cnn = copy.deepcopy(cnn)

    normalization = Normalization(normalization_mean, normalization_std).to(DEVICE)

    content_losses = []
    style_losses = []

    # Собираем модель для переноса стилей
    model = nn.Sequential(normalization)

    i = 0
    for layer in cnn.children():
        if isinstance(layer, nn.Conv2d):
            i += 1
            name = f'conv_{i}'
        elif isinstance(layer, nn.ReLU):
            name = f'relu_{i}'
            layer = nn.ReLU(inplace=False)
        elif isinstance(layer, nn.MaxPool2d):
            name = f'pool_{i}'
        elif isinstance(layer, nn.BatchNorm2d):
            name = f'bn_{i}'
        else:
            raise RuntimeError(f'Unrecognized layer: {layer.__class__.__name__}')

        model.add_module(name, layer)

        if name in content_layers:
            target = model(content_img).detach()  # Убираем из графа вычислений target, он константа
            content_loss = ContentLoss(target)
            model.add_module(f'content_loss_{i}', content_loss)
            content_losses.append(content_loss)

        if name in style_layers:
            target_feature = model(style_img).detach()  # Убираем из графа вычислений target_feature, он константа
            style_loss = StyleLoss(target_feature)
            model.add_module(f'style_loss_{i}', style_loss)
            style_losses.append(style_loss)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]

    return model, style_losses, content_losses
