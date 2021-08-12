from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE


class Course(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="courses")


class Activity(models.Model):
    title = models.CharField(max_length=255)
    points = models.IntegerField()


class Submission(models.Model):
    grade = models.IntegerField(null=True)
    repo = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
