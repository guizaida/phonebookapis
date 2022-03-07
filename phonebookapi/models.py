from django.db import models


# Create your models here.
class phonebook(models.Model):
    UserName = models.TextField()
    Password = models.TextField()
    PhoneNumber = models.IntegerField()
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "phonebook"
        
class UserToken(models.Model):
    user = models.OneToOneField(to="phonebook", on_delete=models.CASCADE)
    token = models.CharField(max_length=64)