from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"#{self.name}"

class Project(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title