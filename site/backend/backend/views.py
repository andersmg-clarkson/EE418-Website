from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect

def default(request):
    return redirect('frontend/index.html')

def index(request):
    return render(request, 'frontend/index.html')
