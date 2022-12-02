import re
from typing import List

import networkx as nx

from .regex_tree import RegExTree, REGEX_EXPRESSION, initialize_regex_tree


class Helpers:

    regex_tree = re.compile(r'^\s+|^[^a-zA-Z0-9\s]+|^[0-9]+|^[a-zA-Z]+')
    space_chars_regex = re.compile(r'^\s+')
    special_chars_regex = re.compile(r'^[^a-zA-Z0-9\s]+')
    digits_regex = re.compile(r'^[0-9]+')
    alpha_chars_regex = re.compile(r'^[a-zA-Z]+')

    G = initialize_regex_tree()

    def column(self, matrix, i):
        '''
        return column i from matrix
        '''
        return [row[i] for row in matrix]


    def tokenize(self, token: str) -> list:
        '''
        tokenize token based on the regex tree
        '''
        deep_tokens = []
        while token:
            deep_token = self.regex_tree.search(token).group()
            deep_tokens.append(deep_token)
            token = self.regex_tree.sub('', token, 1)
        return deep_tokens

    def is_candidate_token(self, tokens:list, min_sup:float) -> bool:
        '''
        - Return True if tokens in the list are candidate tokens
        - Candidate tokens are tokens with support >= min_sup
        - Tokens support is calculated as following: (A-B)/A
            - A : total number of tokens
            - B : number of unique tokens
        - each None token is counted as a unique token, as a None is considered as a wildcard (*)
        '''

        none_values_count = tokens.count(None)
        unique_tokens = set(tokens)
        unique_tokens.discard(None)
        A = len(tokens)
        B = len(unique_tokens) + none_values_count
        tokens_support = (A-B)/A

        if tokens_support >= min_sup:
            return True
        
        return False
    
    def find_tokens_lowest_common_ancestor(self, tokens:list) -> RegExTree:
        '''
        Given a list Tokens, return the common regular expression class for all of them
        '''
        unique_tokens = set(tokens)
        unique_tokens.discard(None)

        tokens_class = set()
        for token in unique_tokens:
            if self.alpha_chars_regex.search(token):
                tokens_class.add(RegExTree.alpha_chars)
            elif self.digits_regex.search(token):
                tokens_class.add(RegExTree.digits)
            elif self.special_chars_regex.search(token):
                tokens_class.add(RegExTree.special_chars)
            elif self.space_chars_regex.search(token):
                tokens_class.add(RegExTree.space_chars)

        if len(tokens_class) == 1:
            regex_class = list(tokens_class)[0]
            return regex_class
        
        sorted_tokens_class = sorted(tokens_class)
        lowest_common_ancestor = nx.tree_all_pairs_lowest_common_ancestor(
            self.G,
            root=RegExTree.all_chars,
            pairs=[
                (sorted_tokens_class[0], sorted_tokens_class[1])
            ]
        )

        regex_class = next(lowest_common_ancestor)[-1]
        
        return regex_class

    def find_classes_lowest_common_ancestor(self, classes:List[RegExTree]) -> RegExTree:
        '''
        - Given a list of regular expression classes, return their lowest common class
        - For example:
            - Input: [RegExTree.digits, RegExTree.alph_chars]
            - Output: RegExTree.alphanumeric
        '''
        if len(classes) == 1:
            regex_class = classes[0]
            return regex_class
        
        sorted_classes = sorted(classes)
        lowest_common_ancestor = nx.tree_all_pairs_lowest_common_ancestor(
            self.G,
            root=RegExTree.all_chars,
            pairs=[
                (sorted_classes[0], sorted_classes[1])
            ]
        )

        regex_class = next(lowest_common_ancestor)[-1]

        return regex_class

    def generate_regex_string(self, regex_class:RegExTree, wildcard:bool) -> str:
        '''
        - Given a regular expression class, return a string representing that class
        - Input:
            - regex_class: Regular expression class of type RegExTree
            - wildcard: boolean describing if wildcard('*') is needed or not 
        '''
        regex = REGEX_EXPRESSION[regex_class]
        
        if wildcard:
            return '(' + regex + '?' + ')'

        return '(' + regex + '+' + ')'

    def join_values(self, values:list, wildcard:bool) -> str:
        '''
        Given a list values, return an OR regular expression of those values
        '''
        #escape special characters
        values = list(map(re.escape, values))
           
        concatenated_values = '|'.join(values)

        if wildcard:
            return '(' + concatenated_values + ')' + '?'
        
        return '(' + concatenated_values + ')'
