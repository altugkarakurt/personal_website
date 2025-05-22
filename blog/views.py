from django.shortcuts import render

from .models import Post, PostSeries, Tag


def home(request):
    return render(request, "blog/home.html", {"title": "Home"})


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


def blog(request):
    return render(request, "blog/blog_index.html", {"title": "Blog"})


def tag_view(request, tag_title):
    tag = Tag.objects.get(title=tag_title)
    posts = tag.posts.order_by("-date_posted")
    context = {"title": f"#{tag_title}", "tag_title": tag_title, "posts": posts}
    return render(request, "blog/tag_view.html", context)


def series_view(request, series_title):
    series = PostSeries.objects.get(title=series_title)
    posts = series.posts.order_by("-date_posted")
    context = {"title": series_title, "description": series.description, "posts": posts}
    return render(request, "blog/series_view.html", context)


def post_view(request, post_url):
    post = Post.objects.get(url=post_url)
    context = {"title": post.title, "content": post.content, "tags": post.tags.all()}
    return render(request, "blog/post_view.html", context)
