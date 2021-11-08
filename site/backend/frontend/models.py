from django.db import models

# Create your models here.

class webdb(models.Model):
    userID = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    userEmail = models.CharField(max_length=40)
    userAccess = models.IntegerField(default=0, editable=True)

    class Meta:
        managed = False
        db_table = 'webdb'
