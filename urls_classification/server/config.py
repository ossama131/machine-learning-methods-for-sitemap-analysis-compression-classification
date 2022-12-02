import os
import torch

CONFIG = {
    "MODEL_PATH": "../model/model.bin",
    "USE_CUDE_IF_AVAILABLE": False
}

CONFIG['DEVICE'] = 'cuda' if torch.cuda.is_available() and config['USE_CUDE_IF_AVAILABLE'] else 'cpu'