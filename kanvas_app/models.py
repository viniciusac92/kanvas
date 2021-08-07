from django.contrib.auth.models import User
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="courses")


class Activity(models.Model):
    title = models.CharField(max_length=255)
    points = models.IntegerField()


class Submission(models.Model):
    grade = models.IntegerField(null=True)
    repo = models.CharField(max_length=255)
    user_id = models.IntegerField()
    activity_id = models.IntegerField()
    activities = models.ManyToManyField(Activity, related_name="submissions")
