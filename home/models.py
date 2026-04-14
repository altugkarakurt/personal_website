from django.db import models
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.images.blocks import ImageChooserBlock
from wagtail.search import index


class HomePage(Page):
    # Configuration
    max_count = 1 # There should only be one homepage

    # Content Panels
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )

    home_text = models.CharField(
        blank=True,
        max_length=255, help_text="Write an introduction for the site"
    )

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("home_text"),
            ],
            heading="Home blurb",
        ),
        FieldPanel("body"),
    ]

class TechPage(Page):
    # Configuration
    max_count = 1 # There should only be one project-index
    parent_page_types = ["home.HomePage"]
    subpage_types = []


class ProjectIndexPage(Page):
    # Configuration
    max_count = 1 # There should only be one project-index
    parent_page_types = ["home.HomePage"]
    subpage_types = ["home.ProjectPage"]

    # Content Panels
    intro = models.TextField(blank=True, max_length=2000)
    content_panels = Page.content_panels + ["intro"]

    # Methods
    def get_context(self, request):
        context = super().get_context(request)
        projects = self.get_children().live().order_by("-first_published_at")

        context["projects"] = projects
        return context

class ProjectPage(Page):
    # Configuration
    parent_page_types = ["home.ProjectIndexPage"]
    intro = models.TextField(blank=True, max_length=1000)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Project image",
    )

    # Content Panels
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

    tools = StreamField([
        ('tool', blocks.CharBlock(label="Tool")),
    ], blank=True, help_text="Add a list of strings")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("image"),
        FieldPanel("body"),
        FieldPanel("tools"),
    ]

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        tag = request.GET.get("tag")
        context["tools"] = self.tools
        return context

    
    subpage_types = ["blog.BlogIndexPage", "blog.BlogTagIndexPage"]

@register_setting
class FooterLinks(BaseGenericSetting):
    github = models.URLField(blank=True, null=True)
    scholar = models.URLField(blank=True, null=True)
    email = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("github"),
        FieldPanel("scholar"),
        FieldPanel("email"),
        FieldPanel("linkedin"),
    ]

