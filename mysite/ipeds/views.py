from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from urllib.parse import urlencode
from datetime import datetime, timedelta
from . import sql_scripts
from .Students import Students


def index(request):
    S = Students('2024FA')
    title = "Home"
    df = sql_scripts.readSQL(S.table(['GENDER', 'RACE', 'STATUS', 'LOAD', 'ACAD_LEVEL', 'CIP_CLASS']))
    context = {
        'title': title,
        'df': df.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/base.html', context)

def ftug(request):
    S = Students('2024FA')
    title = "Part A - Fall Enrollment for Full-Time Undergraduate Students"
    df = sql_scripts.readSQL(S.x())
    context = {
        'title': title,
        'df': df.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/base.html', context)