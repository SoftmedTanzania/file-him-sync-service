import string
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import requests
from celery import shared_task
import os
import shutil
from datetime import datetime

@shared_task
def post_csv():
    in_dir = '/Users/user/Documents/EMR/in'
    out_dir = '/Users/user/Documents/EMR/out'
    err_dir = '/Users/user/Documents/EMR/err'

    url = 'http://139.162.149.249'

    for filename in os.listdir(in_dir):
        if filename.endswith(".csv"):
            try:
                with open(filename, 'rb') as f:
                    # Add a post url that accepts csv file from the emr mediator
                    r = requests.post(url, files={filename: f})

                    # move file to output folder
                    shutil.move(in_dir +'/'+ filename, out_dir +'/' + filename )
                    return r.status_code
            except Exception as e:
                shutil.move(in_dir + '/' + filename, err_dir + '/' + filename )
                raise e
        else:
            return "file not found"

@shared_task
def add_to_file_queue():
    root_dir = '/Users/user/Documents/EMR/'
    in_dir = '/Users/user/Documents/EMR/in'
    try:
        date_time_now = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
        shutil.move(root_dir + 'payload.csv',
                    in_dir +'/payload ' + '_' + date_time_now + '.csv')
    except Exception as e:
        raise e