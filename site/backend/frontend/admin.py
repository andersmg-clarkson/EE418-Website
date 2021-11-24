from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# Define an inline admin descriptor for Profile model which acts a bit like a singleton
#class ProfileInline(admin.StackedInline):
#    model = Profile
#    can_delete = False
#    verbose_name_plural = 'Profile'

# Define a new User admin
#class UserAdmin(BaseUserAdmin):
#    inlines = (ProfileInline,)
    #list_display = ('username', 'first_name', 'last_name', 'is_superuser', 'Profile')

# Re-register UserAdmin
#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)


admin.site.register(Profile)
