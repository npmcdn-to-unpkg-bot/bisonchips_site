from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel



class HomePage(Page):
    background_img = models.ForeignKey(
                        'wagtailimages.Image', 
                        null=True, 
                        blank=True,
                        on_delete=models.SET_NULL,
                        related_name='+')
    
    content_panels = Page.content_panels + [
        ImageChooserPanel('background_img'),
    ]
