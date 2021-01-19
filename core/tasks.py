"""tasks.py is the file to hold all celery related tasks

rabbit-mq is the message broker and django will be the producer of files.
Tasks will be sent from django task file to celery via celery beats.
"""

import requests
from celery import Celery
import os
from pathlib import Path
from datetime import datetime
from .models import Mediator, File, FilePath

app = Celery()

@app.task
def prepare_csv_file_queue():
    try:
        mediators = Mediator.objects.filter(is_active=1)

        for mediator in mediators:
            # Get root directory
            root_path = FilePath.objects.get(mediator=mediator).directory_path

            # One mediator will have only one file to send
            file_description = File.objects.get(mediator=mediator).file_name

            for subdir, dirs, files in os.walk(root_path):#pylint: disable=possibly-unused-variable
                for file in os.listdir(subdir):
                    file_name = Path(subdir + "/" + file).stem
                    if file == file_description:
                        date_time_now = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
                        os.rename(subdir + '/' + file_name + '.csv',
                                  subdir +'/' + file_name + '__' + date_time_now + '_in.csv')
            return 200
    except Exception as e:
        raise e


@app.task
def post_csv_files():
    try:
        mediators = Mediator.objects.filter(is_active=1)

        for mediator in mediators:
            root_path = FilePath.objects.get(mediator=mediator).directory_path
            file_end_point = File.objects.get(mediator=mediator).end_point

            try:
                for subdir, dirs, files in os.walk(root_path):#pylint: disable=possibly-unused-variable
                    for file in os.listdir(subdir):
                        file_name = Path(subdir + "/" + file).stem
                        date_time_now = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
                        if file.endswith("in.csv"):
                            with open(subdir + '/' + file, 'rb') as csv_file:
                                r = requests.post(file_end_point, files={file: csv_file},
                                                  auth=("emr-filedrop-sync-service", "Him123"))
                                if r.status_code == 200:
                                    # move to out dir after successful posting
                                    os.rename(subdir + '/' + file_name + '.csv',
                                              subdir + '/' + file_name + '__' + date_time_now + '_out.csv')
                                else:
                                    # move to err dir due to a failed posting
                                    os.rename(subdir + '/' + file_name + '.csv',
                                              subdir + '/' + file_name + '__' + date_time_now + '_err.csv')
            except Exception as e:
                raise e
        return 200
    except Exception as e:
        raise e




