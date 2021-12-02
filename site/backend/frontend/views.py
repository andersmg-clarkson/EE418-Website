from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import loginForm, registerForm, profileForm, updateUserForm, updateProfileForm
from django.http import HttpResponse
from django.template import loader
from .models import userdb, Profile
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


def index(request):
    template = loader.get_template('frontend/index.html')

    """
    User = get_user_model()
    all_users = User.objects.all()
    all_users = User.objects.values()
    print("INDEX TEST BEGIN")
    print(all_users)
    print("INDEX TEST END /n")
    """

    context = {}
    return HttpResponse(template.render(context, request))


@login_required(login_url='/frontend/index.html')
def home(request):
    template = loader.get_template('frontend/home.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required(login_url='/frontend/index.html')
def courses(request):
    template = loader.get_template('frontend/courses.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required(login_url='/frontend/index.html')
def projects(request):
    template = loader.get_template('frontend/projects.html')
    context = {}
    return HttpResponse(template.render(context, request))



@login_required(login_url='/frontend/index.html')
def account(request):

    if request.method == 'POST':
        user_form = updateUserForm(request.POST, instance=request.user)
        profile_form = updateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('account.html')
    else:
        user_form = updateUserForm(instance=request.user)
        profile_form = updateProfileForm(instance=request.user.profile)

    template = loader.get_template('frontend/account.html')
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
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


# https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
@transaction.atomic
def register_view(request):

    next = request.GET.get('next')
    rForm = registerForm(request.POST or None)
    pForm = profileForm(request.POST or None)

    if rForm.is_valid() and pForm.is_valid():
        #user = rForm.save(commit=False)
        #pForm.save(commit=False)

        user = rForm.save()
        pForm.save(commit=False)

        #user = form.save()
        #profile = form2.save(commit=False)
        #profile.user = user
        #profile.save()

        password = rForm.cleaned_data.get('password')

        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)

        login(request, new_user)

        if next:
            return redirect(next)
        return redirect('login.html')

    """
    if request.method == 'POST':
        rForm = registerForm(request.POST)
        pForm = profileForm(request.POST)

        if rForm.is_valid() and pForm.is_valid():
            user = rForm.save()

            profile = pForm.save(commit=False)
            profile.user = user

            profile.save()

            username = rForm.cleaned_data.get('username')
            password = rForm.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('login.html')

    else:
        rForm = registerForm()
        pForm = profileForm()
    """

    context = {
        'rForm': rForm,
        'pForm': pForm
    }

    return render(request, "frontend/register.html", context)


@login_required(login_url='/frontend/index.html')
def logout_view(request):
    logout(request)
    return redirect('index.html')



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('account.html')
