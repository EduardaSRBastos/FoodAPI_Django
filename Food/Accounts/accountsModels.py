from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, AbstractUser
from django.db import models
#from djongo import models

#SqLite3
class UserModel(UserCreationForm):
    roles = models.ManyToManyField(Group)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'roles')


#MongoDB
# class UserModel(models.Model):
#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128)
#     roles = models.ManyToManyField(Group)

#     def __str__(self):
#         return self.username