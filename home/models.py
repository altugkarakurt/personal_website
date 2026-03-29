from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):
    ###################################
    # Content Panels
    ###################################
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

    ###################################
    # Configuration
    ###################################
    max_count = 1 # There should only be one homepage
    
    subpage_types = ["blog.BlogIndexPage", "blog.BlogTagIndexPage"]

