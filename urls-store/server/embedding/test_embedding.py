import unittest

import numpy as np

from embedding import FastTextEmbedding

class TestFastTextEmbedding(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.model_path = "models/fasttext/gpt2_bpe_fasttext_model.bin"
        self.embedder = FastTextEmbedding(self.model_path)

    def test_load_existing_model(self):
        model_path = "models/fasttext/gpt2_bpe_fasttext_model.bin"
        try:
            embedder = FastTextEmbedding(model_path)
        except FileNotFoundError:
            self.fail("FastText load_module function failed")

    def test_load_non_existing_model(self):
        model_path = "models/fasttext/gpt2_bpe_fasttext_model.bin"
        try:
            embedder = FastTextEmbedding(model_path)
        except FileNotFoundError:
            self.fail("FastText load_module function failed")

    def test_embedding_vector_size(self):
        input_to_get_word_vector = ["some_word"]
        self.assertEqual(
            len(self.embedder.get_word_vector(input_to_get_word_vector)[0]),
            300
        )

    def test_get_word_vector(self):
        words = ["one", "two"]
        arr = self.embedder.get_word_vector(words)
        self.assertIsInstance(
            arr,
            np.ndarray,
            "embedding vector is not a numpy array"
        )
        self.assertIsInstance(
            arr[0],
            np.ndarray,
            "embedding vector is not a numpy array"
        )
        self.assertIsInstance(
            arr[0][0],
            np.float32,
            "embedding vector is not float"
        )
        self.assertEqual(
            len(arr),
            2
        )

    def test_get_sentence_vector(self):
        sentences = [["one", "two"], ["three", "four"]]
        words_embedding = self.embedder.get_word_vector(sentences[0])
        arr = self.embedder.get_sentence_vector(sentences)
        self.assertIsInstance(
            arr,
            np.ndarray,
            "embedding vector is not a numpy array"
        )
        self.assertIsInstance(
            arr[0],
            np.ndarray,
            "embedding vector is not a numpy array"
        ),
        self.assertIsInstance(
            arr[0][0],
            np.float32,
            "embedding vector is not float"
        )
        self.assertTrue(
            np.array_equal(
                (words_embedding[0] + words_embedding[1]) / 2,
                arr[0]
            )
        )
        self.assertEqual(
            len(arr),
            2
        )


        