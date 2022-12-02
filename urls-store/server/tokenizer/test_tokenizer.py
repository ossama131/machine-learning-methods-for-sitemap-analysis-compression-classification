import unittest

from tokenizer import RegExTokenizer, GPT2BPETokenizer

single_url_list = [
    'https://www.uni-passau.de/informatik.php'
]

class TestRegExTokenizer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tokenizer = RegExTokenizer()

    def test_tokenize(self):
        tokens = self.tokenizer.tokenize(single_url_list)
        self.assertEqual(
            tokens,
            [['https', ':', '/', '/', 'www', '.', 'uni', '-', 'passau', '.', 'de', '/', 'informatik', '.', 'php']]
        )


    def test_vocab_size(self):
        self.assertEqual(
            self.tokenizer.vocab_size,
            -1
        )


class TestGPT2BPETokenizer(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.tokenizer = GPT2BPETokenizer()

    def test_tokenize(self):
        tokens = self.tokenizer.tokenize(single_url_list)
        self.assertEqual(
            tokens,
            [['https', '://', 'www', '.', 'uni', '-', 'pass', 'au', '.', 'de', '/', 'in', 'format', 'ik', '.', 'php']]
        )

    def test_vocab_size(self):
        return self.assertEqual(
            self.tokenizer.vocab_size,
            50257
        )
        
if __name__ == '__main__':
    unittest.main()