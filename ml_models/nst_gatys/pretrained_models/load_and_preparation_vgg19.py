import torch
import torchvision.models as models


DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Сохранение модели, состоящей из первых 11 слоев VGG19 в файл
vgg = models.vgg19(pretrained=True).features.to(DEVICE).eval()
model_path = 'vgg19_first_11_layers.pth'
torch.save(vgg[:11], model_path)
