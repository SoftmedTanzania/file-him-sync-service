import requests
from celery import shared_task
import os
from pathlib import Path
import shutil
from datetime import datetime




class CsvFileHandling(object):

    def __init__(self):
        # mediator end points
        self.send_bed_occupancy_url = 'http://139.162.143.150:5001/bed_occupancy'
        self.send_services_url = 'http://139.162.143.150:5001/services_received'
        self.send_daily_death_count_url = 'http://139.162.143.150:5001/daily_death_count'
        self.send_revenue_url = 'http://139.162.143.150:5001/revenue_received'



        # file paths
        # self.root_dir = '/Users/user/Documents/EMR/'
        # self.in_dir = '/Users/user/Documents/EMR/in'
        # self.out_dir = '/Users/user/Documents/EMR/out'
        # self.err_dir = '/Users/user/Documents/EMR/err'

        self.root_dir = '/home/danny/EMR/'
        self.in_dir = '/home/danny/EMR/in'
        self.out_dir = '/home/danny/EMR/out'
        self.err_dir = '/home/danny/EMR/err'

    @shared_task
    def add_to_file_queue(self):

        try:
            for filename in os.listdir(self.root_dir):
                if filename.endswith(".csv"):
                    file = Path(self.root_dir + "/" + filename).stem
                    date_time_now = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
                    shutil.move(self.root_dir + file + '.csv',
                                self.in_dir + '/' + file + '_' + date_time_now + '.csv')
                    return 200
                else:
                    return 404
        except Exception as e:
            raise e

    @shared_task
    def post_csv(self):

        for filename in os.listdir(self.in_dir):
            if filename.endswith(".csv"):
                file = Path(self.in_dir + "/" + filename).stem
                try:
                    with open(self.in_dir+'/'+filename, 'rb') as csv_file:
                        # bed occupancy processing
                            if file.startswith('bed_occupancy'):
                                r = requests.post(self.send_bed_occupancy_url, files={filename: csv_file})
                                # move file to output folder
                                if r.status_code == 200:
                                    # move to out dir after successful posting
                                    shutil.move(self.in_dir +'/'+ filename, self.out_dir +'/' + filename )
                                else:
                                    # move to err dir due to a failed posting
                                    shutil.move(self.in_dir + '/' + filename, self.err_dir + '/' + filename)
                                return 200
                            elif file.startswith('services_received'):
                                r = requests.post(self.send_services_url, files={filename: csv_file})
                                # move file to output folder
                                if r.status_code == 200:
                                    # move to out dir after successful posting
                                    shutil.move(self.in_dir + '/' + filename, self.out_dir + '/' + filename)
                                else:
                                    # move to err dir due to a failed posting
                                    shutil.move(self.in_dir + '/' + filename, self.err_dir + '/' + filename)
                                return 200
                            elif file.startswith('daily_death_count'):
                                r = requests.post(self.send_daily_death_count_url, files={filename: csv_file})
                                # move file to output folder
                                if r.status_code == 200:
                                    # move to out dir after successful posting
                                    shutil.move(self.in_dir + '/' + filename, self.out_dir + '/' + filename)
                                else:
                                    # move to err dir due to a failed posting
                                    shutil.move(self.in_dir + '/' + filename, self.err_dir + '/' + filename)
                                return 200
                            elif file.startswith('revenue_received'):
                                r = requests.post(self.send_revenue_url, files={filename: csv_file})
                                # move file to output folder
                                if r.status_code == 200:
                                    # move to out dir after successful posting
                                    shutil.move(self.in_dir + '/' + filename, self.out_dir + '/' + filename)
                                else:
                                    # move to err dir due to a failed posting
                                    shutil.move(self.in_dir + '/' + filename, self.err_dir + '/' + filename)
                                return 200
                except Exception as e:
                    raise e
            else:
                return 404

