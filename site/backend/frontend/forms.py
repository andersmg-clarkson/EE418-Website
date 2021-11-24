from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import userdb, Profile
from django.contrib.auth.models import User
from django.forms import MultiWidget, TextInput

User = get_user_model()

#https://www.youtube.com/watch?v=BiHSP6bTsrE
class loginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

        return super(loginForm, self).clean(*args, **kwargs)


class registerForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(label='Email Address')
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email is already in use')

        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('passwords do not match')

        return super(registerForm, self).clean(*args, **kwargs)


class profileForm(forms.ModelForm):
    institution = forms.CharField()
    course = forms.CharField()

    class Meta:
        model = Profile
        fields = [
            'institution',
            'course'
        ]



# https://dev.to/earthcomfy/django-update-user-profile-33ho
class updateUserForm(forms.ModelForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class updateProfileForm(forms.ModelForm):
    institution = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    course = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = [
            'institution',
            'course'
        ]
