# Create your models here.
from django.db import models
from datetime import datetime

# Create your models here.
class TwitUser(models.Model):
    id = models.AutoField(primary_key = True)
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    class Meta:
        db_table = "TwitUser"


class TwitPost(models.Model):
    id = models.AutoField(primary_key = True)
    Title=models.CharField(max_length=30)
    Description = models.TextField(blank=True, null=True)
    PostDate = models.DateTimeField(default=datetime.now)
    TwitUser = models.ForeignKey(TwitUser)
    class Meta:
        db_table = "TwitPost"
class TwitFollower(models.Model):
    id = models.AutoField(primary_key = True)
    FollowerId=models.IntegerField()
    TwitUser = models.ForeignKey(TwitUser)
    class Meta:
        db_table = "TwitFollower"
