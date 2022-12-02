import unittest

from utils import read_file

class TestUtils(unittest.TestCase):

    def test_read_file_exact_batch_size(self):
        file_path = 'test_items/test_urls_50.txt'
        batch_size = 10
        total_read_urls = 0
        batches = []
        for batch in read_file(file_path=file_path, batch_size=batch_size):
            total_read_urls += len(batch)
            batches.append(batch)

        self.assertTrue(
            len(batches) == 5 and total_read_urls == 50 and \
            len(batches[0]) == len(batches[-1]) == batch_size
        )

    def test_read_file_non_exact_batch_size(self):
        file_path = 'test_items/test_urls_50.txt'
        batch_size = 11
        total_read_urls = 0
        batches = []
        for batch in read_file(file_path=file_path, batch_size=batch_size):
            total_read_urls += len(batch)
            batches.append(batch)

        self.assertTrue(
            len(batches) == 5 and total_read_urls == 50 and \
            len(batches[0]) == len(batches[-2]) == batch_size and \
            len(batches[-1]) == 6
        )

    def test_read_file_non_existing_file(self):
        non_existing_file_path = 'test_items/non_existing.txt'
        try:
            read_file(file_path=non_existing_file_path)
        except FileNotFoundError:
            self.fail("read_file reading non existing file test failed")