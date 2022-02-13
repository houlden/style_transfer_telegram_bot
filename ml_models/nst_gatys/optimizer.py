import torch
import torch.optim as optim


def get_input_optimizer(input_image: torch.Tensor):
    """
    Создает экземпляр оптимизатора
    """
    optimizer = optim.LBFGS([input_image.requires_grad_()])
    return optimizer
