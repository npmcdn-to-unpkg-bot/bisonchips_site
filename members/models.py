from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

from wagtail.wagtailadmin.edit_handlers import (FieldPanel,
                                                MultiFieldPanel, 
                                                FieldRowPanel)      
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.models import Image

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.


class CurrentMembersPage(Page):
    
    def get_context(self, request):
        context = super(CurrentMembersPage, self).get_context(request)
        context['current_members'] = MemberPage.objects.filter(current=True)
        return context

class MemberPage(Page):
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        primary_key=True,
        on_delete=models.PROTECT
    )
    current = models.BooleanField(default=False, verbose_name="current student")
    nickname = models.CharField(max_length=254, null=True, blank=True)
    graduation_year = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(1974)])
    image = models.ForeignKey(
                        'wagtailimages.Image', 
                        null=True, 
                        blank=True,
                        on_delete=models.SET_NULL,
                        related_name='+')
    img = models.ImageField(upload_to='images/members', null=True, blank=True)
    thumbnail = ImageSpecField(source='img',
                                   processors=[ResizeToFill(100, 50)],
                                   format='JPEG',
                                   options={'quality': 60}
                                )
    hometown = models.CharField(max_length=254, null=True, blank=True)
    major = models.CharField(max_length=254, blank=True)
    voice_part = models.CharField(max_length=254, blank=True)
    bio = RichTextField(null=True, blank=True)
    
    # Info only seen by authenticated users
    phone = models.CharField(max_length=20, blank=True, verbose_name="phone number")
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('user'),
                ImageChooserPanel('image'),
                FieldPanel('nickname'),
                FieldPanel('graduation_year'),
                FieldPanel('voice_part'),
                FieldPanel('major'),
                FieldPanel('hometown'),
                FieldPanel('bio')
            ],
            heading="Publicly Visible Information"
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel('phone', classname='col6'),
                        FieldPanel('location', classname='col6')
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel('website', classname='col6'),
                        FieldPanel('linkedin', classname='col6'),
                    ]
                ),
                FieldRowPanel(
                    [
                        FieldPanel('facebook', classname='col6'),
                        FieldPanel('instagram', classname='col6')
                    ]
                )
            ],
            heading="Members Only Information"
        ),
        FieldPanel('current'),
    ]
    
'''
class Member(AbstractUser):
    
    nickname = models.CharField(max_length=254, null=True, blank=True)
    graduation_year = models.PositiveIntegerField(validators=[MinValueValidator(1974)])
    img = models.ImageField(upload_to='images/members', null=True, blank=True)
    img_thumbnail = ImageSpecField(source='img',
                                   processors=[ResizeToFill(100, 50)],
                                   format='JPEG',
                                   options={'quality': 60}
                                )
    home_town = models.CharField(max_length=254, null=True, blank=True)
    major = models.CharField(max_length=254, blank=True)
    voice_part = models.CharField(max_length=254, blank=True)
    current = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)
    
    # Info only seen by authenticated users
    phone = models.CharField(max_length=20, blank=True, verbose_name="phone number")
    location = models.CharField(max_length=255, blank=True)
    website = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
'''
    