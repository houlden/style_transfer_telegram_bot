import torch

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
IMAGE_SIZE = 128  # Размер выходного изображения IMAGE_SIZE*IMAGE_SIZE
CONTENT_LAYERS = ['conv_4']  # Слои, по которым считается content-loss
STYLE_LAYERS = ['conv_1', 'conv_2', 'conv_3', 'conv_4', 'conv_5']  # Слои, по которым считается style-loss
NORMALIZATION_MEAN = torch.tensor([0.485, 0.456, 0.406])  # Средние значения, по которым нормировалась VGG19
NORMALIZATION_STD = torch.tensor([0.229, 0.224, 0.225])  # Стандартные отклонения, по которым нормировалась VGG19
NUM_STEPS = 500  # Количество итераций оптимизации
STYLE_WEIGHT = 100000  # Вес style-loss
CONTENT_WEIGHT = 1  # Вес content-loss (небольшой вес, поскольку на вход сети подается копия изображения content)
