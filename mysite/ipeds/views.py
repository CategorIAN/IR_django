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
    return render(request, 'ipeds/index.html', context)

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
    return render(request, 'ipeds/MenWomenPivots.html', context)

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
    return render(request, 'ipeds/MenWomenPivots.html', context)

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
    return render(request, 'ipeds/MenWomenPivots.html', context)

def ptug_by_cip(request, cip):
    S = Students('2024FA')
    title = f"Part A - Fall Enrollment for Part-time Undergraduate Students: CIP CODE:{cip}.0000"
    df_men = sql_scripts.readSQL(S.x('Part-Time', 'M', cip))
    df_women = sql_scripts.readSQL(S.x('Part-Time', 'F', cip))
    context = {
        'title': title,
        'df_men': df_men.to_html(classes='table table-striped table-hover', index=False),
        'df_women': df_women.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/MenWomenPivots.html', context)

def graduates(request):
    S = Students('2024FA')
    title = "Part A - Fall Enrollment for Graduate Students"
    df_men = sql_scripts.readSQL(S.y('M'))
    df_women = sql_scripts.readSQL(S.y('M'))
    context = {
        'title': title,
        'df_men': df_men.to_html(classes='table table-striped table-hover', index=False),
        'df_women': df_women.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/MenWomenPivots.html', context)

def graduates_by_cip(request, cip):
    S = Students('2024FA')
    title = f"Part A - Fall Enrollment for Graduate Students: CIP CODE:{cip}.0000"
    df_men = sql_scripts.readSQL(S.y('M', cip))
    df_women = sql_scripts.readSQL(S.y('M', cip))
    context = {
        'title': title,
        'df_men': df_men.to_html(classes='table table-striped table-hover', index=False),
        'df_women': df_women.to_html(classes='table table-striped table-hover', index=False)
    }
    return render(request, 'ipeds/MenWomenPivots.html', context)

def gender_unknowns(request):
    S = Students('2024FA')
    title = "Part A - Fall Enrollment - Gender Unknown or Another Gender than Provided Categories"
    df = sql_scripts.readSQL(S.z())
    context = {'title': title, 'df': df.to_html(classes='table table-striped table-hover', index=False)}
    return render(request, 'ipeds/GenderUnknowns.html', context)

def distance_education_status_1(request):
    S = Students('2024FA')
    title = "Part A - Fall Enrollment by Distance Education Status 1"
    prompt = "My Prompt"
    df = sql_scripts.readSQL(S.a())
    context = {'title': title, 'prompt': prompt, 'df': df.to_html(classes='table table-striped table-hover', index=False)}
    return render(request, 'ipeds/DistanceEducation.html', context)