from django.test import TestCase
from .tasks import CsvFileHandling
import unittest
# Create your tests here.

class TestFileHandling(unittest.TestCase):

    def test_file_handling(self):
        self.url = 'http://139.162.149.249'
        self.root_dir = '/Users/user/Documents/EMR/'
        self.in_dir = '/Users/user/Documents/EMR/in'
        self.out_dir = '/Users/user/Documents/EMR/out'
        self.err_dir = '/Users/user/Documents/EMR/err'

        csv_file_handling = CsvFileHandling()
        self.assertEqual(200, csv_file_handling.add_to_file_queue(self))

    def test_failed_file_handling(self):
        self.url = 'http://139.162.149.249'
        self.root_dir = '/Users/user/Documents/EMR/'
        self.in_dir = '/Users/user/Documents/EMR/in'
        self.out_dir = '/Users/user/Documents/EMR/out'
        self.err_dir = '/Users/user/Documents/EMR/err'

        csv_file_handling = CsvFileHandling()
        self.assertEqual(404, csv_file_handling.add_to_file_queue(self), )

    def test_posting_csv(self):
        self.url = 'http://139.162.149.249'
        self.root_dir = '/Users/user/Documents/EMR/'
        self.in_dir = '/Users/user/Documents/EMR/in'
        self.out_dir = '/Users/user/Documents/EMR/out'
        self.err_dir = '/Users/user/Documents/EMR/err'

        csv_file_handling = CsvFileHandling()
        self.assertEqual(200, csv_file_handling.post_csv(self))

    def test_posting_csv_failed(self):
        self.url = 'http://139.162.149.249'
        self.root_dir = '/Users/user/Documents/EMR/'
        self.in_dir = '/Users/user/Documents/EMR/in'
        self.out_dir = '/Users/user/Documents/EMR/out'
        self.err_dir = '/Users/user/Documents/EMR/err'

        csv_file_handling = CsvFileHandling()
        self.assertEqual(404, csv_file_handling.post_csv(self))
