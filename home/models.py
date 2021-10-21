from django.db import models

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    logo = models.ForeignKey('wagtailimages.Image', 
                             on_delete=models.SET_NULL, 
                             related_name='+',
                             null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('logo'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['static_pages'] = self.get_children().type(StaticPage)
        context['news_pages'] = self.get_children().type(NewsPage)
        return context


class NewsPage(Page):
    """Publication of current news stories with images."""
    lead_image = models.ForeignKey('wagtailimages.Image', 
                             on_delete=models.SET_NULL, 
                             related_name='+',
                             null=True)

    lede = models.CharField(max_length=512)

    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], null=True, blank=True)

    author = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('lead_image'),
        FieldPanel('author'),
        FieldPanel('lede'),
        StreamFieldPanel('body'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['parent'] = self.get_parent()
        return context
    

class StaticPage(Page):
    """Pages that are updated less frequently, and are shown in the nav."""
    body = StreamField([
        ('heading', blocks.CharBlock(form_classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['parent'] = self.get_parent()
        return context