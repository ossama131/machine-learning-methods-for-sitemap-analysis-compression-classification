"""
This module provide classes that serves to tokenize URLs
"""

from abc import ABC, abstractmethod
import re
from typing import List

from transformers import GPT2Tokenizer

class Tokenizer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def tokenize(self, urls:List[str]) -> List[List[str]]:
        pass

    @property
    @abstractmethod
    def vocab_size(self):
        pass


class RegExTokenizer(Tokenizer):
    def __init__(self, regex=None):
        super().__init__()
        self.regex = self._init_regex(regex)
        
    def _init_regex(self, regex):
        if not regex:
            return re.compile(r'([^a-zA-Z0-9])')
        
        if isinstance(regex, re.Pattern):
            return regex

        if isinstance(regex, str):
            return re.compile(regex)
    
    def tokenize(self, urls:List[str]) -> List[List[str]]:
        tokenized = []
        for url in urls:
            tokens = list(filter(None, self.regex.split(url)))
            tokenized.append(tokens)
        
        return tokenized

    @property
    def vocab_size(self):
        return -1


class GPT2BPETokenizer(Tokenizer):
    def __init__(self):
        super().__init__()
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    def tokenize(self, urls:List[str]) -> List[List[str]]:
        tokenized = []
        for url in urls:
            tokens = self.tokenizer.tokenize(url)
            tokenized.append(tokens)

        return tokenized

    @property
    def vocab_size(self):
        return self.tokenizer.vocab_size
