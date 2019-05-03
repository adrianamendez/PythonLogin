from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.
#class UserTbl(User):
  #  id_group_permission = models.ForeignKey(Group)


class product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    info = models.CharField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
