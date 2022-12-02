from .helpers import Helpers

class RegExPatternGenerator():
    def __init__(self, tokens: list, min_sup:float=0.7) -> None:
        self.tokens = tokens
        self.min_sup = min_sup
        self.helpers = Helpers()

    def run(self) -> str:
        if len(set(self.tokens)) == 1:
            if self.tokens[0] in ['', None]:
                return '(.*)'

            '''if there is only one token or all tokens are the equal'''
            return self.helpers.join_values(self.tokens[:1], wildcard=False)

        max_tokens_len = 0
        tokenized = []
        for token in self.tokens:
            deep_tokens = self.helpers.tokenize(token)
            tokenized.append(deep_tokens)
            max_tokens_len = max(max_tokens_len, len(deep_tokens))

        tokenized_matrix = list(
            map(
                lambda row: row + [None] * (max_tokens_len - len(row)),
                tokenized
            )
        )

        candidate_tokens = []
        empty_tokens_exist = []
        for i in range(max_tokens_len):
            column_i = self.helpers.column(tokenized_matrix, i)

            candidate_token = self.helpers.is_candidate_token(column_i, self.min_sup)
            empty_token_exist = None in column_i

            candidate_tokens.append(candidate_token)
            empty_tokens_exist.append(empty_token_exist)
        
        non_candidate_tokens_to_be_grouped = {'classes':set(), 'empty_tokens_exist':[]}
        regex_elements = []
        for i, (is_candidate, empty_token) in enumerate(zip(candidate_tokens, empty_tokens_exist)):
            column_i = self.helpers.column(tokenized_matrix, i)

            if is_candidate:

                if non_candidate_tokens_to_be_grouped['classes']:
                    regex_class = self.helpers.find_classes_lowest_common_ancestor(
                        classes= list(non_candidate_tokens_to_be_grouped['classes'])
                    )
                    wildcard = all(non_candidate_tokens_to_be_grouped['empty_tokens_exist'])

                    regex_str = self.helpers.generate_regex_string(regex_class, wildcard)

                    regex_elements.append(regex_str)
                    non_candidate_tokens_to_be_grouped = {'classes':set(), 'empty_tokens_exist':[]}
                
                unique_tokens = set(column_i)
                unique_tokens.discard(None)
                unique_tokens_list = list(unique_tokens)
                wildcard = empty_tokens_exist[i]

                regex_str = self.helpers.join_values(unique_tokens_list, wildcard)
                regex_elements.append(regex_str)

            else:
                unique_tokens = set(column_i)
                unique_tokens.discard(None)
                unique_tokens_list = list(unique_tokens)
                regex_class = self.helpers.find_tokens_lowest_common_ancestor(unique_tokens_list)

                non_candidate_tokens_to_be_grouped['classes'].add(regex_class)
                non_candidate_tokens_to_be_grouped['empty_tokens_exist'].append(empty_tokens_exist[i])
        
        if non_candidate_tokens_to_be_grouped['classes']:
            regex_class = self.helpers.find_classes_lowest_common_ancestor(
                classes= list(non_candidate_tokens_to_be_grouped['classes'])
            )
            wildcard = all(non_candidate_tokens_to_be_grouped['empty_tokens_exist'])
            regex_str = self.helpers.generate_regex_string(regex_class, wildcard)
            regex_elements.append(regex_str)
            non_candidate_tokens_to_be_grouped = {'classes':set(), 'empty_tokens_exist':[]}

        if regex_elements:
            return '^' + ''.join(regex_elements) + '$'
        
        return '(.*)'