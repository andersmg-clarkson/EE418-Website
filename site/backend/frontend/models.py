from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import CASCADE


class userdb(models.Model):
    userID = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=40)
    institution = models.CharField(max_length=40)
    course = models.CharField(max_length=40)
    access = models.IntegerField(default=0, editable=True)

    class Meta:
        managed = False
        db_table = 'userdb'


#https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=40)
    course = models.CharField(max_length=40)
    accessLevel = models.IntegerField(default=0, editable=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
