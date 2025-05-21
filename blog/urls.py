from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="blog-home"),
    path("about/", views.about, name="blog-about"),
    path("blog/post/<int:post_id>/", views.post_view, name="blog-post-view"),
    path("blog/tag/<str:tag_title>/", views.tag_view, name="blog-tag-view"),
    path("blog/series/<str:series_title>/", views.series_view, name="blog-series-view"),
    path("blog/", views.blog, name="blog-index")
]
