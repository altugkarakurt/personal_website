from django.db import models
from django.urls import reverse
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
    slug = models.SlugField(default="", null=False)
    blurb = models.CharField(max_length=500, blank=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    series = models.ManyToManyField(PostSeries, related_name="posts", blank=True)

    # We order posts by new to old.
    class Meta:
        ordering = ["-date_posted"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})
