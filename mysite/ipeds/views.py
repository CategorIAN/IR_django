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
    df_men = sql_scripts.readSQL(S.x('Full-Time', 'M'))
    df_women = sql_scripts.readSQL(S.x('Full-Time', 'F'))
    context = {
        'title': title,
        'df_men': df_men.to_html(classes='table table-striped table-hover', index=False),
        'df_women': df_women.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/base.html', context)

def ftug_by_cip(request, cip):
    S = Students('2024FA')
    title = f"Part A - Fall Enrollment for Full-Time Undergraduate Students: CIP CODE:{cip}.0000"
    df_men = sql_scripts.readSQL(S.x('Full-Time', 'M', cip))
    df_women = sql_scripts.readSQL(S.x('Full-Time', 'F', cip))
    context = {
        'title': title,
        'df_men': df_men.to_html(classes='table table-striped table-hover', index=False),
        'df_women': df_women.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/base.html', context)


def ptug(request):
    S = Students('2024FA')
    title = "Part A - Fall Enrollment for Part-time Undergraduate Students"
    df_men = sql_scripts.readSQL(S.x('Part-Time', 'M'))
    df_women = sql_scripts.readSQL(S.x('Part-Time', 'F'))
    context = {
        'title': title,
        'df_men': df_men.to_html(classes='table table-striped table-hover', index=False),
        'df_women': df_women.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/base.html', context)