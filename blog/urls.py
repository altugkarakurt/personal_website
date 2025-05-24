from django.urls import path

from . import views
from .views import PostDetailView, PostListView, PostSeriesListView, PostTagListView

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("blog/post/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("blog/tag/<str:tag_title>/", PostTagListView.as_view(), name="post-tag-list"),
    path(
        "blog/series/<str:series_title>/",
        PostSeriesListView.as_view(),
        name="post-series-list",
    ),
    path("blog/", PostListView.as_view(), name="post-list"),
]
