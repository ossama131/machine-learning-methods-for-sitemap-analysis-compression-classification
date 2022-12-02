from typing import List, Literal
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import GPT2Tokenizer

import torch
import torch.nn.functional as F

from cnn import load_model
from config import CONFIG

CATEGORIES = ['ADULT', 'ARTS', 'BUSINESS', 'COMPUTERS', 'GAMES', 'HEALTH', 'HOME', 'KIDS', 'NEWS', 'RECREATION', 'REFERENCE', 'SCIENCE', 'SHOPPING', 'SOCIETY', 'SPORTS']

class ClassifierInput(BaseModel):
    urls: List[str]

app = FastAPI()

MAX_TOKENS = 256
model = None
tokenizer = None

@app.on_event("startup")
async def on_startup():
    global model
    global tokenizer
    print('\n')
    print(f'+ PyTorch using device: {CONFIG["DEVICE"]}\n')

    print(f'+ Lodaing PyTorhc model: {CONFIG["MODEL_PATH"]}\n')

    model = load_model()

    print(f'\t==> PyTorch Model loaded successfully\n')

    print('+ Configuring Tokenizer')

    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token 

    print(f'\t==> Tokenizer configured successfully\n')

@app.post('/api/v1/predict')
def predict(urls_input:ClassifierInput):
    res = {
        'category': [],
        'prob': []
    }
    urls = urls_input.urls

    assert urls, 'Empty list of URLs'
    
    input_ids = tokenizer(urls ,padding='max_length', max_length=MAX_TOKENS, truncation=True, return_tensors='pt')['input_ids']
    logits = model.forward(input_ids)
    probs = F.softmax(logits, dim=1).squeeze(dim=0).tolist()
    probs = [probs] if isinstance(probs[0], float) else probs

    preds = torch.argmax(logits, dim=1).flatten().tolist()

    for i, m in enumerate(preds):
        res['category'].append(CATEGORIES[m])
        res['prob'].append(round(probs[i][m], ndigits=3))

    return res