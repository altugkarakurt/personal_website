from django.db import models
from django.db.models import Count
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase, Tag
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index

###################################
# Constants
###################################
NUM_OF_POPULAR_TAGS = 10
POSTS_PER_PAGE = 2 # Pagination

###################################
# Util Functions
###################################

# Returns the 10 most popular tags with non-zero uses.
def get_popular_tags():
    return Tag.objects.annotate(
        num_times = Count("blog_blogpagetag_items")
    ).exclude(num_times=0).order_by('-num_times')[:NUM_OF_POPULAR_TAGS]

###################################
# Classes
###################################
class BlogIndexPage(Page):

    # Configuration
    max_count = 1 # There should only be one blog-index
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPage"]

    # Content Panels
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + ["intro"]

    # Methods
    def get_context(self, request):
        context = super().get_context(request)
        posts = self.get_children().live().order_by("-first_published_at")
        page = request.GET.get("page", 1)

        # Pagination
        paginator = Paginator(posts, POSTS_PER_PAGE) 
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["popular_tags"] = get_popular_tags()
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
        context = super().get_context(request)
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag).live().order_by("-first_published_at")
        page = request.GET.get("page", 1)

        # Pagination
        paginator = Paginator(blogpages, POSTS_PER_PAGE) # param 2 is the num. of posts / page 
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["blogpages"] = posts
        context["popular_tags"] = get_popular_tags()
        return context


class BlogPage(Page):

    # Configuration
    parent_page_types = ["blog.BlogIndexPage"]

    # Content Panels
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField([
        ("content", blocks.RichTextBlock(
            features=["bold", "italic", "link", "ol", "ul", "hr"],
            template="blocks/richtext.html"
        )),
        ("image", ImageChooserBlock(
            template="blocks/image.html"
        )),
        ("quote", blocks.BlockQuoteBlock(
            templte="blocks/quote.html"
        )),
    ])
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("tags"),
    ]

