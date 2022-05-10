import torch
import torch.nn as nn
from enum import Enum, unique

@unique
class LossFunctions(Enum):
    #Some common loss functions
    L1LOSS = nn.L1Loss()
    MSELOSS = nn.MSELoss()
    BCELOSS = nn.BCELoss()
    CELOSS = nn.CrossEntropyLoss() 
    