from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.search import index


class BlogIndexPage(Page):
    ###################################
    # Configuration
    ###################################
    max_count = 1 # There should only be one blog-index
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPage"]

    ###################################
    # Content Panels
    ###################################
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + ["intro"]

    ###################################
    # Methods
    ###################################
    def get_posts(self):
        return self.get_children().live().order_by("-first_published_at")
    
    def get_context(self, request):
        context = super().get_context(request)
        context["posts"] = self.get_posts()
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE
    )
    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]


class BlogTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag).live().order_by("-first_published_at")

        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True, 
                         features=["code",
                                   "blockquote",
                                   "strikethrough",
                                   "superscript",
                                   "subscript",]
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        "date",
        "intro",
        "body",
        "tags",
    ]

