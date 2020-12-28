from django.test import TestCase
from .tasks import post_csv, add_to_file_queue
# Create your tests here.

class AddFilesToQueue(TestCase):
    add_to_file_queue()

class UploadFileTest(TestCase):
    status_code = post_csv()

    if status_code == 200:
        print("success")
    elif status_code == 400:
        print("file not found")