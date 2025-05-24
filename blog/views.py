from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Post, PostSeries, Tag


def home(request):
    return render(request, "blog/home.html", {"title": "Home"})


def about(request):
    return render(request, "blog/about.html", {"title": "About"})


class PostListView(ListView):
    model = Post
    paginate_by = 5
    extra_context = {"title": "Blog"}


class PostDetailView(DetailView):
    model = Post


class PostTagListView(ListView):
    model = Post
    template_name = "blog/post_tag_list.html"
    context_object_name = "post_tag_list"
    # paginate_by = 5

    def get_queryset(self):
        tag = Tag.objects.get(title=self.kwargs.get("tag_title"))
        return tag.posts.all()


class PostSeriesListView(ListView):
    model = Post
    template_name = "blog/post_series_list.html"
    context_object_name = "post_series_list"
    # paginate_by = 5

    def get_queryset(self):
        series = PostSeries.objects.get(title=self.kwargs.get("series_title"))
        return series.posts.all()
