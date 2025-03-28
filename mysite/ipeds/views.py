from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from urllib.parse import urlencode
from datetime import datetime, timedelta
from . import sql_scripts


def index(request):
    df = sql_scripts.readSQL(sql_scripts.all_people())
    print(df)
    return HttpResponse("Hello, world. This is the index page.")