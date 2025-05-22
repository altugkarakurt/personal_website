from django.db import models
from django.utils import timezone


class Tag(models.Model):
    title = models.CharField(max_length=250)

    def __str__(self):
        return f"#{self.title}"


class PostSeries(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "series"

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name="posts")
    series = models.ManyToManyField(PostSeries, related_name="posts", blank=True)

    def __str__(self):
        return self.title
