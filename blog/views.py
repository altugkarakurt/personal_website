from django.shortcuts import render
from .models import Post, Tag, Project

def home(request):
    return render(request, "blog/home.html", {'title':'Home'})


def about(request):
    return render(request, "blog/about.html", {'title':'About'})


def blog(request):
    return render(request, "blog/blog_index.html", {'title':'Blog',
                                                    'posts'    : Post.objects.all(),
                                                    'tags'     : Tag.objects.all(),
                                                    'projects' : Project.objects.all()})


def projects(request):
    return render(request, "blog/project_index.html", {'title':'Projects'})