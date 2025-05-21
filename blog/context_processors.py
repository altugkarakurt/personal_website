from .models import Post, Tag, PostSeries

def blog_base_context(request):
    return {"blog_base_posts"  : Post.objects.all().order_by("-date_posted")[:25],
            "blog_base_series" : PostSeries.objects.all().order_by("-title")[:25],
            "blog_base_tags"   : Tag.objects.all().order_by("-title")[:50]}
