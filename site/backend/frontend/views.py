from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import loginForm, registerForm
from django.http import HttpResponse
from django.template import loader
from .models import webdb


def index(request):
    template = loader.get_template('frontend/index.html')
    #data = webdb.objects.raw('select * from webdb')
    context = {

    }
    return HttpResponse(template.render(context, request))


@login_required
def home(request):
    template = loader.get_template('frontend/home.html')
    #data = webdb.objects.raw('select * from webdb')
    context = {

    }
    return HttpResponse(template.render(context, request))


@login_required
def courses(request):
    template = loader.get_template('frontend/courses.html')
    #data = webdb.objects.raw('select * from webdb')
    context = {

    }
    return HttpResponse(template.render(context, request))


@login_required
def projects(request):
    template = loader.get_template('frontend/projects.html')
    #data = webdb.objects.raw('select * from webdb')
    context = {

    }
    return HttpResponse(template.render(context, request))



#https://www.youtube.com/watch?v=BiHSP6bTsrE
def login_view(request):
    next = request.GET.get('next')
    form = loginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        if next:
            return redirect(next)
        return redirect('home.html')

    context = {
        'form': form,
    }

    return render(request, "frontend/login.html", context)



def register_view(request):
    next = request.GET.get('next')
    form = registerForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)

        login(request, new_user)

        if next:
            return redirect(next)
        return redirect('login.html')

    context = {
        'form': form,
    }

    return render(request, "frontend/register.html", context)



def logout_view(request):
    logout(request)
    return redirect('index.html')
