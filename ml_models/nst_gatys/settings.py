import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Размер выходного изображения IMAGE_SIZE*IMAGE_SIZE
IMAGE_SIZE = 256

# Слои, по которым считается content-loss
CONTENT_LAYERS = ['conv_4']
# Слои, по которым считается style-loss
STYLE_LAYERS = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']

# Первые 11 слоев (5 сверток VGG19)
CNN_PRETRAINED_PATH = 'ml_models/nst_gatys/pretrained_models/vgg19_first_11_layers.pth'

# Средние значения, по которым нормировалась VGG19
NORMALIZATION_MEAN = torch.tensor([0.485, 0.456, 0.406])
# Стандартные отклонения, по которым нормировалась VGG19
NORMALIZATION_STD = torch.tensor([0.229, 0.224, 0.225])

# Количество итераций оптимизации
NUM_STEPS = 500

# Вес style-loss
STYLE_WEIGHT = 100000
# Вес content-loss (небольшой вес, поскольку на вход сети подается копия изображения content)
CONTENT_WEIGHT = 1
