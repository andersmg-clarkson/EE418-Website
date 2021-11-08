from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect

def index(request):
    return render(request, 'frontend/index.html')
