from multiprocessing import context
from django.db import models
from wagtail.core import blocks
from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel, FieldPanel, PageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail_color_panel.fields import ColorField
from wagtail_color_panel.edit_handlers import NativeColorPanel


# The following functions handle the determination changing theme_text
# color to white or black depending on theme color.


def pairwise(iterable):
    """
    ABCDEF -> (A, B), (C, D), (E, F)
    """
    a = iter(iterable)
    return zip(a,a)


def convert_rgb_string(rgb_str):
    return tuple(
        int(''.join(c), base=16) for c in pairwise(rgb_str[1:])
        )


def convert_srgb_val_to_linear(c):
    c = c / 255
    if c <=0.04045:
        return c/12.92
    return ((c+0.055)/1.055) ** 2.4


def calc_luminance(rgb: tuple):
    return sum(
        scale * convert_srgb_val_to_linear(c)
        for scale, c in zip([0.2126,0.7152,0.0722], rgb)
    )


def calc_text_color_contrasting_theme(theme):
    if calc_luminance(convert_rgb_string(theme)) > 0.179:
        return "#000000"
    return "#FFFFFF"




## fill context with site-wide information set on homepage
def pull_sitewide_context(page):
    """
    HomePage has all the attributes we're looking for. It's at depth two,
    has a max_count of one, and everything is a decendent, you have to walk which
    ever page back to home to add all attributes to the context.
    """

    stop = page
    while stop.depth > 2:
        stop = stop.get_parent()

    context_addendum = {}

    # theme color
    context_addendum["theme_color"] = stop.specific.theme_color
    context_addendum["theme_text"] = calc_text_color_contrasting_theme(stop.specific.theme_color)

    context_addendum["invert_flag"] = True
    context_addendum["secondary_logo"] = stop.specific.logo_invert

    if calc_luminance(convert_rgb_string(stop.specific.theme_color)) > 0.179:
        context_addendum["secondary_logo"] = stop.specific.logo
        context_addendum["invert_flag"] = False

    # -> all pages for nav
    context_addendum["static_pages"] = stop.get_children().type(StaticPage)
    context_addendum["socials"] = stop.specific.socials

    return context_addendum


class Writer(Page):
    author_image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    
    content_panels = Page.content_panels + [
        ImageChooserPanel("author_image"),
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("email"),
        FieldPanel("bio"),
    ]

    @property
    def name(self):
        return self.first_name + " " + self.last_name


class Beat(Page):
    pass


class ArticlePage(Page):
    lead_image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True
    )

    section = models.ForeignKey(Beat, on_delete=models.SET_NULL, null=True, blank=True)

    lede = models.CharField(max_length=1024)

    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )

    author = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    content_panels = Page.content_panels + [
        ImageChooserPanel("lead_image"),
        SnippetChooserPanel("author"),
        SnippetChooserPanel("section"),
        FieldPanel("lede"),
        StreamFieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        context["theme_color"] = self.get_parent().specific.theme_color

        return {**context, **pull_sitewide_context(self)}


class SocialsBlock(blocks.StructBlock):
    platform = blocks.CharBlock()
    image = ImageChooserBlock()
    invert_image = ImageChooserBlock()
    url = blocks.CharBlock()


class HomePage(Page):
    max_count = 1
    template = "home/home.html"


    theme_color = ColorField(default="#FF0000")

    logo = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True
    )

    logo_invert = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True
    )

    featured_vendor = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True
    )

    socials = StreamField([("account", SocialsBlock())], blank=True)


    ### Selectors for main articles

    main_article = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        )

    left_article = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        )

    bottom_article = models.ForeignKey(
        ArticlePage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        )


    content_panels = Page.content_panels + [
        NativeColorPanel("theme_color"),        
        ImageChooserPanel("logo"),
        ImageChooserPanel("logo_invert"),
        ImageChooserPanel("featured_vendor"),
        StreamFieldPanel("socials"),
        PageChooserPanel("main_article"),
        PageChooserPanel("left_article"),
        PageChooserPanel("bottom_article"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Add access to all pages from this page.
        return {**context, **pull_sitewide_context(self)}


class StaticPage(Page):
    max_count = 1
    highlight = False
    
    lead_image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True
    )

    body = StreamField(
        [
            ("heading", blocks.CharBlock(form_classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )


    content_panels = Page.content_panels + [
        ImageChooserPanel("lead_image"),
        StreamFieldPanel("body"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Add access to all pages from this page.
        return {**context, **pull_sitewide_context(self)}


class ArchiveEntry(Page):
    front_image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, related_name="+", null=True
    )

    pdf = models.ForeignKey(
        'wagtaildocs.Document', blank=True, null=True,
         on_delete=models.SET_NULL, related_name='+'
    )

    tags = models.CharField(max_length=280, blank=True, null=True)
    content_panels = Page.content_panels + [
        DocumentChooserPanel('pdf'),
        FieldPanel('tags'),
        ImageChooserPanel('front_image'),
    ]


class News(StaticPage):
    template = "home/static_page.html"




class Archive(StaticPage):
    subpage_types = [
        ArchiveEntry
    ]


class GetInvolved(StaticPage):
    template = "home/static_page.html"


class About(StaticPage):
    template = "home/static_page.html"


class OurTeam(StaticPage):
    template = "home/static_page.html"


class Resources(StaticPage):
    template = "home/static_page.html"


class Donate(StaticPage):
    highlight = True
    template = "home/static_page.html"


class Contact(StaticPage):
    highlight = True
    template = "home/static_page.html"