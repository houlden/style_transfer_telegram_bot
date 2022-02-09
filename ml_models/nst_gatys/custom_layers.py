import torch
import torch.nn as nn
import torch.nn.functional as F


class ContentLoss(nn.Module):
    def __init__(self, target):
        super().__init__()
        self.target = target.detach()
        self.loss = F.mse_loss(self.target, self.target)

    def forward(self, features):
        self.loss = F.mse_loss(features, self.target)
        return features


class StyleLoss(nn.Module):
    def __init__(self, target_features):
        super().__init__()
        self.target = StyleLoss._gram_matrix(target_features).detach()
        self.loss = F.mse_loss(self.target, self.target)

    @staticmethod
    def _gram_matrix(features):
        batch_size, channels, h, w = features.size()
        flattened_features = features.view(batch_size * channels, h * w)
        G = torch.mm(flattened_features, flattened_features.t())
        return G.div(batch_size * channels * h * w)

    def forward(self, features):
        G = StyleLoss._gram_matrix(features)
        self.loss = F.mse_loss(G, self.target)
        return features


class Normalization(nn.Module):
    def __init__(self, mean, std):
        super().__init__()
        self.mean = mean.view(-1, 1, 1)
        self.std = std.view(-1, 1, 1)

    def forward(self, img):
        return (img - self.mean) / self.std
