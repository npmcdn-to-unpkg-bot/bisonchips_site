from django.db import models
from django.core.validators import MinValueValidator

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel    
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey
from tinytag import TinyTag
from wagtailmedia.edit_handlers import MediaChooserPanel
from wagtailmedia.models import AbstractMedia

from bisonchips_site.utils import RelatedLink, AbstractClassWithoutFieldsNamed as without

# Create your models here.

class AlbumIndexPage(Page):
    
    @property
    def albums(self):
        # Get list of live event pages that are descendants of this page
        albums = AlbumPage.objects.live().descendant_of(self)

        # Order by date
        albums = albums.order_by('-year')

        return albums

class AlbumPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('AlbumPage', related_name='related_links')

class AlbumPage(Page):
    year = models.PositiveIntegerField(validators=[MinValueValidator(1974)])
    image = models.ForeignKey(
                        'wagtailimages.Image', 
                        on_delete=models.PROTECT,
                        related_name='+')
                        
    content_panels = Page.content_panels + [
        FieldPanel('year'),
        ImageChooserPanel('image'),
        InlinePanel('tracks', label="Tracks"),
        InlinePanel('related_links', label="Related links"),
    ]

class ChipsMedia(without(AbstractMedia, 'duration')):
    admin_form_fields = (
            'title',
            'file',
            'collection',
            'width',
            'height',
            'thumbnail',
            'tags',
        )
        
    @property
    def duration(self):
        return TinyTag.get(self.file).duration
        
    @property
    def track(self):
        return TinyTag.get(self.file).track
        
    @property
    def is_audio(self):
        return self.type == 'audio'
        
    @property
    def is_video(self):
        return self.type == 'video'
        
class AlbumMediaLink(Orderable):
    page = ParentalKey('AlbumPage', related_name='tracks')
    ref = models.ForeignKey(
                        ChipsMedia, 
                        on_delete=models.CASCADE,
                        verbose_name='Track',
                        related_name='+')
                        
    panels = [
        MediaChooserPanel('ref')
    ]
