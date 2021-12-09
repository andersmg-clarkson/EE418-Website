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
from github import Github, GithubException

github_pat = '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'

def index(request):
    template = loader.get_template('frontend/index.html')
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
    #template = loader.get_template('frontend/projects.html')
    #context = {}
    #return HttpResponse(template.render(context, request))

    g = Github(github_pat)
    repo_list = [i for i in g.get_user().get_repos()]
    repo_list.sort(key=lambda r: r.updated_at, reverse=True)

    html = """
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootswatch/3.3.7/paper/bootstrap.min.css" />
	<body style="background-color: aliceblue">
	<ul class="nav navbar-nav">
    <li><a href="home.html">Home</a></li>
    <li><a href="courses.html">Courses</a></li>
    <li><a href="logout.html">Logout</a></li>
    </ul>
	<br><br>
	<h1 style="text-align: center">Projects</h1>
	<div style="background-color: aliceblue; padding-left: 10px">
	"""
    for repo in repo_list:
        html += gen_project(repo, has_clone_auth(request.user))

    html += '</div>'
    html += '</body'
    return HttpResponse(html)



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
        user = rForm.save()
        pForm.save(commit=False)

        password = rForm.cleaned_data.get('password')

        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)

        login(request, new_user)

        if next:
            return redirect(next)
        return redirect('login.html')

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


# Generated view
def repo_viewer(request):
	repo_name_path = request.GET['repo_name_path']
	delim = repo_name_path.index(':')
	repo_name = repo_name_path[:delim]
	current_path = repo_name_path[delim+1:]

	g = Github(github_pat)
	repo = g.get_repo(repo_name)

	html = gen_navbar()
	html += '<h1 style="text-align: center">' + repo.name + ' Repo Viewer: [/' + current_path + ']</h1>'
	html += '<div style="background-color: aliceblue; padding-left: 10px">'

	cur_file = repo.get_contents(current_path)

	if type(cur_file).__name__ == "ContentFile":
		html += '<div style="background-color: white; margin-left: 50px; margin-top: 50px; margin-right: 50px; padding: 10px; border-style: solid; border-radius: 10px;"'
		decoded_text = '{ Unable to decode file contents }'
		try:
			decoded_text = cur_file.decoded_content.decode('utf-8').replace("\n","<br>")
		except:
			pass
		html += '<p>' + decoded_text + '</p>'
		html += '</div>'
	else:
		for file in repo.get_dir_contents(current_path):
			display_name = file.name if file.type == 'file' else '📁 ' + file.name
			html += gen_file_btn(repo_name + ':' + file.path, display_name)

	html += '</div>'

	return HttpResponse(html)


# Project Page Helper functions
def gen_file_btn(repo_name_path, btn_text):
	btn_src = """
	<form action='repo_viewer' method='GET' style="margin: -1px; text-align: center">
	<button style="width: 80%" type='submit' name='repo_name_path' value='{0}'>{1}</button>
	</form>
	"""
	return btn_src.format(repo_name_path, btn_text)


def gen_repo_btn(repo_name_path):
	btn_src = """
	<form action='repo_viewer' method='GET' style="border-style=thin">
	<button style="width: 25%; padding: 5px" type='submit' name='repo_name_path' value='{0}'>[ Repository Viewer ]</button>
	</form>
	"""
	return btn_src.format(repo_name_path)

def gen_clone_btn(repo):
	btn_src = """
	<div id='clone_div' style="
		color: white;
		padding: 5px;
		background-color: #008CBA;
		border-style: thin;
		border-color: black;
		max-width: 25%;
		text-align: center;
	">

	<details>
    <summary>[ Clone ]</summary>
	<p style="background-color: white; color:black">{0}</p>
	</details>
	</div>
	"""

	return btn_src.format(repo.clone_url)

def gen_project(repo, has_clone_auth=False):
	html = '<h3>' + repo.name + '</h3>'
	html += '<div style="background-color: white; padding: 10px; border-style: solid; border-radius: 7px">'
	html += '<p><strong>Last Updated: </strong>' + (repo.updated_at).strftime("%m/%d/%Y %H:%M:%S") + '</p>'
	html += '<p><strong>Project Description: </strong>' + (repo.description if repo.description != None else 'N/A') + '</p>'
	html += gen_repo_btn(repo.full_name + ':')
	if has_clone_auth:
		html += gen_clone_btn(repo)
	html += '</div>'

	# Space between divs
	html += '<div style="padding-bottom:30px"></div>'

	return html

def has_clone_auth(django_user):
    django_name = django_user.username

    if django_user.profile.accessLevel > 0:
        return True

    #for db_user in get_user_model().objects.values():
		#if db_user['username'] == django_name and db_user['accessLevel'] > 0:
            #return True

    return False
