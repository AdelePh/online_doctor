# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import Http404
from django.shortcuts import render
import requests
import sqlite3
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.shortcuts import redirect

#@csrf_exempt
# Create your views here.
def index(request):
    return render(request, "about.html")
'''
def github(request):
    user = {}
    if 'username' in request.GET:
        username = request.GET['username']
        url = 'https://api.github.com/users/%s' % username
        response = requests.get(url)
        user = response.json()
    return render(request, "about.html", {'user': user})
'''

def search(request):
    if request.method == 'POST':
        user_id = request.POST.get('username')
        url = "http://127.0.0.1:5000/%s" %user_id
        response = requests.get(url)
        data = response.json()
        data = data[user_id]
        context = {"data": data}
        template = loader.get_template('showdata.html')
        return HttpResponse(template.render(context, request))
    else: 
        template = loader.get_template('about.html')
        return HttpResponse(template.render())
