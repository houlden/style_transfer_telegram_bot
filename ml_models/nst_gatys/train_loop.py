import asyncio
import torch
import torch.nn as nn

from ml_models.nst_gatys.build_style_transfer_model import build_model_and_get_losses
from ml_models.nst_gatys.optimizer import get_input_optimizer
from ml_models.nst_gatys.settings import NUM_STEPS, STYLE_WEIGHT, CONTENT_WEIGHT


async def style_transfer_loop(cnn: nn.Module, normalization_mean: torch.Tensor, normalization_std: torch.Tensor,
                              content_image: torch.Tensor, style_image: torch.Tensor, input_image: torch.Tensor,
                              num_steps: int = NUM_STEPS, style_weight: int = STYLE_WEIGHT,
                              content_weight: int = CONTENT_WEIGHT) -> torch.Tensor:
    """
    Реализует процесс стилизации изображения content под изображение style.

    :param cnn: nn.Module - Предобученная свёрточная нейросеть VGG19 (или VGG16)
    :param normalization_mean: torch.Tensor - Средние значения, по которым нормировалась VGG19
    :param normalization_std: torch.Tensor - Стандартные отклонения, по которым нормировалась VGG19
    :param content_image: torch.Tensor - Изображение content
    :param style_image: torch.Tensor - Изображение style
    :param input_image: torch.Tensor - Входное изображение
    :param num_steps: int - Количество итераций оптимизации
    :param style_weight: int - Вес style-loss
    :param content_weight: int - Вес content-loss
    :return: torch.Tensor
    """

    model, style_losses, content_losses = build_model_and_get_losses(cnn, normalization_mean, normalization_std,
                                                                     style_image, content_image)

    optimizer = get_input_optimizer(input_image)

    run = 0
    while run <= num_steps:
        await asyncio.sleep(0)  # Добавим асинхронный выход, чтобы бот мог реагировать на события во время обучения

        # Поскольку у нас нет функции подсчета loss-а, реализуем её явно в виде замыкания
        def closure():
            nonlocal run

            input_image.data.clamp_(0, 1)  # Ограничение на значения пикселей картинки

            optimizer.zero_grad()

            model(input_image)  # Вычисление content и style loss-ов внутри слоев модели

            style_score = 0
            content_score = 0

            # Извлечение loss-ов из промежуточных слоев модели
            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            # Взвешивание ошибки
            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()

            run += 1

            return style_score + content_score

        optimizer.step(closure)

    input_image.data.clamp_(0, 1)  # Ограничение на значения пикселей картинки на выходе

    return input_image
