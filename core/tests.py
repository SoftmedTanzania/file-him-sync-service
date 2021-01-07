from .tasks import CsvFileHandling
import unittest
import os
from pathlib import Path


# Create your tests here.
class TestFileHandling(unittest.TestCase):

    def test_file_handling(self):
        self.send_bed_occupancy_url = 'http://139.162.143.150:5001/bed_occupancy'
        self.send_services_url = 'http://139.162.143.150:5001/services_received'
        self.send_daily_death_count_url = 'http://139.162.143.150:5001/daily_death_count'
        self.send_revenue_url = 'http://139.162.143.150:5001/revenue_received'

        # self.root_dir = '/Users/user/Documents/EMR/'
        # self.in_dir = '/Users/user/Documents/EMR/in'
        # self.out_dir = '/Users/user/Documents/EMR/out'
        # self.err_dir = '/Users/user/Documents/EMR/err'

        self.root_dir = 'EMR/'
        self.in_dir = 'EMR/in'
        self.out_dir = 'EMR/out'
        self.err_dir = 'EMR/err'

        csv_file_handling = CsvFileHandling()
        for filename in os.listdir(self.root_dir):
            if filename.endswith('csv'):
                self.assertEqual(csv_file_handling.add_to_file_queue(self), 200)
            else:
                self.assertEqual(csv_file_handling.add_to_file_queue(self), 404)


    def test_posting_csv(self):
        self.send_bed_occupancy_url = 'http://139.162.143.150:5001/bed_occupancy'
        self.send_services_url = 'http://139.162.143.150:5001/services_received'
        self.send_daily_death_count_url = 'http://139.162.143.150:5001/daily_death_count'
        self.send_revenue_url = 'http://139.162.143.150:5001/revenue_received'

        self.root_dir = 'EMR/'
        self.in_dir = 'EMR/in'
        self.out_dir = 'EMR/out'
        self.err_dir = 'EMR/err'

        csv_file_handling = CsvFileHandling()

        for filename in os.listdir(self.in_dir):
            if filename.endswith(".csv"):
                file = Path(self.in_dir + "/" + filename).stem

                if file.startswith('bed_occupancy'):
                    self.assertEqual(csv_file_handling.post_csv(self), 200)
                elif file.startswith('services_received'):
                    self.assertEqual(csv_file_handling.post_csv(self), 200)
                elif file.startswith('daily_death_count'):
                    self.assertEqual(csv_file_handling.post_csv(self), 200)
                elif file.startswith('revenue_received'):
                    self.assertEqual(csv_file_handling.post_csv(self), 200)
            else:
                self.assertEqual(csv_file_handling.post_csv(self), 404)





