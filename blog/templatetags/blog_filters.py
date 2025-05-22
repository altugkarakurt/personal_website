import markdown
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def render_markdown(value):
    md = markdown.Markdown(extensions=["fenced_code"])
    return md.convert(value)
