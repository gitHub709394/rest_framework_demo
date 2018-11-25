from django.db import models
import datetime


# Create your models here.
class UserGroup(models.Model):
    group_name = models.CharField(max_length=32)


class Role(models.Model):
    role_name = models.CharField(max_length=32)
    created = models.DateTimeField(default=datetime.datetime.now())


class UserInfo(models.Model):
    user_type_choices = (
        (1, "普通用户"),
        (2, "VIP"),
        (3, "SVIP")
    )
    user_type = models.IntegerField(choices=user_type_choices)
    user_name = models.CharField(max_length=32, unique=True)

    group = models.ForeignKey("UserGroup", on_delete=models.CASCADE)
    roles = models.ManyToManyField("Role")


class UserToken(models.Model):
    user = models.OneToOneField(to="UserInfo", on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
