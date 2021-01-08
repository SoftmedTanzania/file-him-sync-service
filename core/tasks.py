"""tasks.py is the file to hold all celery related tasks

rabbit-mq is the message broker and django will be the producer of files.
Tasks will be sent from django task file to celery via celery beats.
"""

import requests
from celery import Celery
import os
from pathlib import Path
import shutil
from datetime import datetime

app = Celery()

# def __init__(self):
#     # mediator end points
send_bed_occupancy_url = 'http://139.162.143.150:5001/bed_occupancy'
send_services_url = 'http://139.162.143.150:5001/services_received'
send_daily_death_count_url = 'http://139.162.143.150:5001/daily_death_count'
send_revenue_url = 'http://139.162.143.150:5001/revenue_received'

# staging
# root_dir = '/home/danny/EMR/'
# in_dir = '/home/danny/EMR/in'
# out_dir = '/home/danny/EMR/out'
# err_dir = '/home/danny/EMR/err'

# development
root_dir = '/Users/user/Documents/EMR/'
in_dir = '/Users/user/Documents/EMR/in'
out_dir = '/Users/user/Documents/EMR/out'
err_dir = '/Users/user/Documents/EMR/err'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    app.add_periodic_task(10.0, add_to_file_queue.s(root_dir, in_dir), name='add every 10')

    app.add_periodic_task(10.0, post_csv.s(in_dir, out_dir, err_dir, send_bed_occupancy_url,
                                           send_services_url, send_daily_death_count_url, send_revenue_url),
                          name='add every 10')

@app.task
def add_to_file_queue(root_path,in_path):
    try:
        for filename in os.listdir(root_path):
            if filename.endswith(".csv"):
                file = Path(root_path + "/" + filename).stem
                date_time_now = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
                shutil.move(root_path + file + '.csv',
                            in_path + '/' + file + '_' + date_time_now + '.csv')
        return 200
    except Exception as e:
        raise e


@app.task
def post_csv(in_path, out_path, err_path, final_bed_occupancy_url, final_services_url,
             final_daily_death_count_url, final_revenue_url):

    for filename in os.listdir(in_path):
        if filename.endswith(".csv"):
            file = Path(in_path + "/" + filename).stem
            try:
                with open(in_path+'/'+filename, 'rb') as csv_file:
                    # bed occupancy processing
                    if file.startswith('bed_occupancy'):
                        r = requests.post(final_bed_occupancy_url, files={filename: csv_file})
                        # move file to output folder
                        if r.status_code == 200:
                            # move to out dir after successful posting
                            shutil.move(in_path +'/'+ filename, out_path +'/' + filename )
                        else:
                            # move to err dir due to a failed posting
                            shutil.move(in_path + '/' + filename, err_path + '/' + filename)
                    elif file.startswith('services_received'):
                        r = requests.post(final_services_url, files={filename: csv_file})
                        # move file to output folder
                        if r.status_code == 200:
                            # move to out dir after successful posting
                            shutil.move(in_path + '/' + filename, out_path + '/' + filename)
                        else:
                            # move to err dir due to a failed posting
                            shutil.move(in_path + '/' + filename, err_path + '/' + filename)
                    elif file.startswith('daily_death_count'):
                        r = requests.post(final_daily_death_count_url, files={filename: csv_file})
                        # move file to output folder
                        if r.status_code == 200:
                            # move to out dir after successful posting
                            shutil.move(in_path + '/' + filename, out_path + '/' + filename)
                        else:
                            # move to err dir due to a failed posting
                            shutil.move(in_path + '/' + filename, err_path + '/' + filename)
                    elif file.startswith('revenue_received'):
                        r = requests.post(final_revenue_url, files={filename: csv_file})
                        # move file to output folder
                        if r.status_code == 200:
                            # move to out dir after successful posting
                            shutil.move(in_path + '/' + filename,out_path + '/' + filename)
                        else:
                            # move to err dir due to a failed posting
                            shutil.move(in_path + '/' + filename, err_path + '/' + filename)
                    return 200
            except Exception as e:
                raise e

