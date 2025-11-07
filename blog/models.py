from django.db import models
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

"""--------------------------------------------------------------------
    INDEX PAGES
--------------------------------------------------------------------"""


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    content_panels = Page.content_panels + ["intro"]


class BlogTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context


"""--------------------------------------------------------------------
    BLOG PAGE & RELATED UTIL
--------------------------------------------------------------------"""


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_items", on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    projects = ParentalManyToManyField("blog.Project", blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        return gallery_item.image if (gallery_item) else None

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                "date",
                FieldPanel("projects", widget=forms.CheckboxSelectMultiple),
                "tags",
            ],
            heading="Blog information",
        ),
        "intro",
        "body",
        "gallery_images",
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = ["image", "caption"]


"""--------------------------------------------------------------------
    COLLECTIONS
--------------------------------------------------------------------"""


@register_snippet
class Project(models.Model):
    name = models.CharField(max_length=255)
    project_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = ["name", "project_image"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Projects"
