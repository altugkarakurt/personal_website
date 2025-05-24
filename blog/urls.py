from django.urls import path

from . import views
from .views import PostDetailView, PostListView

urlpatterns = [
    path("", views.home, name="blog-home"),
    path("about/", views.about, name="blog-about"),
    path("blog/post/<slug:slug>/", PostDetailView.as_view(), name="blog-post-detail"),
    path("blog/tag/<str:tag_title>/", views.tag_view, name="blog-tag-view"),
    path("blog/series/<str:series_title>/", views.series_view, name="blog-series-view"),
    path("blog/", PostListView.as_view(), name="blog-post-list"),
]
