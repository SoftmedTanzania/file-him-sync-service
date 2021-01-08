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
from .models import Mediator, File, FilePath

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # pass_emr_related_configs
    app.add_periodic_task(10.0, prepare_csv_file_queue.s(), name='add every 10')
    app.add_periodic_task(10.0, post_csv_files.s(), name='add every 10')


@app.task
def prepare_csv_file_queue():
    try:
        mediators = Mediator.objects.filter(is_active=1)

        for mediator in mediators:
            # Get root directory
            in_path = FilePath.objects.get(mediator=mediator, path_type='in_dir').file_path
            root_path = FilePath.objects.get(mediator=mediator, path_type='root_dir').file_path

            for file in os.listdir(root_path):
                if file.endswith(".csv"):
                    file_name = Path(root_path + "/" + file).stem
                    date_time_now = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
                    shutil.move(root_path + file_name + '.csv',
                                in_path + '/' + file_name + '__' + date_time_now + '.csv')
            return 200
    except Exception as e:
        raise e

@app.task
def post_csv_files():
    try:
        mediators = Mediator.objects.filter(is_active=1)

        for mediator in mediators:
            in_path = FilePath.objects.get(mediator=mediator, path_type='in_dir').file_path
            out_path = FilePath.objects.get(mediator=mediator, path_type='out_dir').file_path
            err_path = FilePath.objects.get(mediator=mediator, path_type='err_dir').file_path

            for dir_file in os.listdir(in_path):
                file_name = Path(in_path + "/" + dir_file).stem
                sep = '__'
                stripped_file_name = file_name.split(sep, 1)[0]

                files = File.objects.filter(mediator=mediator,file_name__startswith=stripped_file_name)

                for file in files:
                    try:
                        post_url = file.end_point
                        with open(in_path + '/' + dir_file, 'rb') as csv_file:
                            r = requests.post(post_url, files={dir_file: csv_file})
                            # move file to output folder
                            if r.status_code == 200:
                                # move to out dir after successful posting
                                shutil.move(in_path + '/' + dir_file, out_path + '/' + dir_file)
                            else:
                                # move to err dir due to a failed posting
                                shutil.move(in_path + '/' + dir_file, err_path + '/' + dir_file)
                            return 200
                    except Exception as e:
                        raise e
    except Exception as e:
        raise e




