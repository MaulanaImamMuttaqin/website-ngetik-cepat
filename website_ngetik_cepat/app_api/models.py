from statistics import mode
# from django.db import models
from djongo import models



# Create your models here.
class Test(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)


class UsersScores(models.Model):
    user_id = models.IntegerField(blank=False)
    item_id = models.IntegerField(default=None, blank=False)
    rating = models.FloatField(blank=False)
    word = models.CharField(max_length=100, blank=False)
    sd = models.FloatField(default=None,blank=False)
    timestamp = models.IntegerField(default=None, blank=False)


class WordsSimMatrix(models.Model):
    item_id = models.IntegerField(max_length=10000, blank=False)
    word = models.CharField(max_length=100, blank=False)
    matrix = models.JSONField(blank=False)


class UserTestResults(models.Model):
    user_id = models.IntegerField(blank=False)
    speed = models.IntegerField(blank=False)
    test_type = models.CharField(max_length=100,blank=False)

# class WordsList(models.Model):
#     words = models.CharField(max_length=100, blank=False)


# class UserData(models.Model):
#     speed = models.ArrayField()