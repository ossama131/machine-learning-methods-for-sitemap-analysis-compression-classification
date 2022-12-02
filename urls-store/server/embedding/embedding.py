"""
This module provide classes that serves to transform URLs into a dense vectors representation
"""

from abc import ABC, abstractmethod
import errno
import os
from typing import List

import fasttext
import numpy as np

class Embedding(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_word_vector(self, words: List[str]) -> np.ndarray:
        pass

    @abstractmethod
    def get_sentence_vector(self, sentences: List[List[str]]) -> np.ndarray:
        pass
    

class FastTextEmbedding(Embedding):
    def __init__(self, model_path: str):
        self.model = self._load_model(model_path)

    def _load_model(self, model_path:str):
        if not os.path.isfile(model_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), model_path)
        model = fasttext.load_model(model_path)
        return model

    def get_word_vector(self, words: List[str]) -> np.ndarray:
        vectors = []
        for word in words:
            vector = self.model[word]
            vectors.append(vector)
        
        return np.array(vectors)

    def get_sentence_vector(self, sentences:List[List[str]]) -> np.ndarray:
        vectors = []
        for sent in sentences:
            words_embedding = self.get_word_vector(sent)
            sent_embedding = np.mean(words_embedding, axis=0)
            vectors.append(sent_embedding)

        return np.array(vectors)
