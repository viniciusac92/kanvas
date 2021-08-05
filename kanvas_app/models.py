from django.contrib.auth.models import User
from django.db import models


class Courses(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name="courses")
