import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import requests
from celery import shared_task
import os
import shutil
from datetime import datetime
import csv
from django.http import Http404



class CsvFileHandling(object):

    def __init__(self):
        self.url = 'http://139.162.149.249'
        self.root_dir = '/Users/user/Documents/EMR/'
        self.in_dir = '/Users/user/Documents/EMR/in'
        self.out_dir = '/Users/user/Documents/EMR/out'
        self.err_dir = '/Users/user/Documents/EMR/err'

    @shared_task
    def post_csv(self):

        for filename in os.listdir(self.in_dir):
            if filename.endswith(".csv"):
                try:
                    with open(self.in_dir+'/'+filename, 'rb') as csv_file:
                        # read csv file to dtermine type of payload
                        csv_reader = csv.reader(csv_file, delimiter=',')
                        line_count = 0
                        for row in csv_reader:
                            if line_count == 0:
                                print('Column names are {',row)
                                line_count += 1
                            else:
                                print(row[0], 'first row of the csv file')
                                line_count += 1


                        # Add a post url that accepts csv file from the emr mediator
                        r = requests.post(self.url, files={filename: csv_file})
                        # move file to output folder
                        if r.status_code == 200:
                            # move to out dir after successful posting
                            shutil.move(self.in_dir +'/'+ filename, self.out_dir +'/' + filename )
                        else:
                            # move to err dir due to a failed posting
                            shutil.move(self.in_dir + '/' + filename, self.err_dir + '/' + filename)
                        return r.status_code
                except Exception as e:
                    raise e
            else:
                return "file not found"


    @shared_task
    def add_to_file_queue(self):

        try:
            for filename in os.listdir(self.root_dir):
                if filename.endswith(".csv"):
                    date_time_now = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
                    shutil.move(self.root_dir + 'payload.csv',
                                self.in_dir +'/payload' + '_' + date_time_now + '.csv')
                    return 200
        except Exception as e:
            return Http404