from django.shortcuts import render, HttpResponse
import requests
from .tasks import CsvFileHandling
# Create your views here.


def check_post_status():
    csv_file_handling = CsvFileHandling()
    status_code = csv_file_handling.post_csv.delay(10)
    if status_code == 200:
        return HttpResponse('SyncProgress.html')