from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from urllib.parse import urlencode
from datetime import datetime, timedelta
from . import sql_scripts
from .Students import Students


def index(request):
    S = Students('2024FA')
    df = sql_scripts.readSQL(S.table())
    context = {
        'df': df.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/index.html', context)