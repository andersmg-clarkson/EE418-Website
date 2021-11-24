from django.urls import path
from . import views
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('login.html', views.login_view, name='login_view'),
    path('register.html', views.register_view, name='register_view'),
    path('logout.html', views.logout_view, name='logout_view'),
    path('home.html', views.home, name='home'),
    path('courses.html', views.courses, name='courses'),
    path('projects.html', views.projects, name='projects'),
    path('account.html', views.account, name='account'),
    path('change_password.html', views.PasswordChangeView.as_view(success_url=reverse_lazy('frontend:account')), name='change_password'),
]
