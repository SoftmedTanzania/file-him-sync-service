from django.shortcuts import render, HttpResponse
import requests
from .tasks import post_csv
# Create your views here.


def check_post_status():
    status_code = post_csv
    if status_code == 200:
        return HttpResponse('SyncProgress.html')