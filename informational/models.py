import datetime

from django.db import models
from django.utils import timezone

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, \
    PageChooserPanel, StreamFieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey

from bisonchips_site.utils import RelatedLink, CarouselItem
from .utils import export_event

# Remember to delete...
def google_map_url(self):
    values = [self.name, self.street_address, self.town, self.state, self.country]
    non_null_values = [s.replace(' ','+') for s in values if s is not None]
    return 'https://www.google.com/maps/search/{}/'.format(
        (',+').join(non_null_values)
    )

# Create your models here.
class LocationBlock(blocks.StructBlock):
    '''
    Structural block for defining a location.
    '''
    name = blocks.CharBlock(required=True)
    street_address = blocks.CharBlock(required=False)
    town = blocks.CharBlock(required=False),
    state = blocks.CharBlock(required=False),
    country = blocks.CharBlock(required=False)
    
    class Meta:
        icon = 'site'
    
    @property
    def google_map_url(self):
        values = [self.name, self.street_address, self.town, self.state, self.zipcode, self.country]
        non_null_values = [s.replace(' ','+') for s in values if s is not None]
        return 'https://www.google.com/maps/search/{}/'.format(
            (',+').join(non_null_values)
        )

class AboutPage(Page):
    
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
            StreamFieldPanel('body'),
        ]
        
class EventIndexPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('EventIndexPage', related_name='related_links')
    
class EventIndexPage(Page):
    
    content_panels = Page.content_panels + [
        InlinePanel('related_links', label="Related links"),
    ]

    @property
    def upcoming_events(self):
        # Get list of live event pages that are descendants of this page
        events = EventPage.objects.live().descendant_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        events = events.filter(date__gte=datetime.date.today())

        # Order by date
        events = events.order_by('date')

        return events
        
    @property
    def past_events(self):
        # Get list of live event pages that are descendants of this page
        events = EventPage.objects.live().descendant_of(self)

        # Filter events list to get ones that are either
        # running now or start in the future
        events = events.filter(date__lte=datetime.date.today())

        # Order by date
        events = events.order_by('-date')

        return events

# Event page

class EventPageCarouselItem(Orderable, CarouselItem):
    page = ParentalKey('EventPage', related_name='carousel_items')


class EventPageRelatedLink(Orderable, RelatedLink):
    page = ParentalKey('EventPage', related_name='related_links')

class EventPage(Page):
    date = models.DateField("Start date")
    time_from = models.TimeField("Start time")
    time_to = models.TimeField("End time", null=True, blank=True)
# location = StreamField([
#        ('location', LocationBlock()),
#    ])
    preview = models.TextField("Short description", max_length=1000)
    body = StreamField([
        ('rich_text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('video', EmbedBlock(icon='media'))
    ])
    price = models.CharField(max_length=255)
    tickets_link = models.URLField("Link to purchase", blank=True)
    
    # Location Fields
    location_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('location'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        FieldPanel('preview'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldRowPanel([
                FieldPanel('time_from', classname='col6'),
                FieldPanel('time_to', classname='col6'),
            ])],
            heading="Time"
        ),
        MultiFieldPanel([
            FieldPanel('location_name'),
            FieldPanel('street_address'),
            FieldRowPanel([
                FieldPanel('town', classname='col8'),
                FieldPanel('state', classname='col4')
            ]),
            FieldRowPanel([
                FieldPanel('zipcode', classname='col4'),
                FieldPanel('country', classname='col8')
            ])    
        ],
        heading="Location"
        ),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('price', classname='col4'),
                FieldPanel('tickets_link', classname='col8'),
            ]),
            ],
            heading="Ticket Information"
        ),
        StreamFieldPanel('body'),
        InlinePanel('carousel_items', label="Carousel items"),
        InlinePanel('related_links', label="Related links"),
    ]
    
    @property
    def google_map_url(self):
        values = [self.name, self.street_address, self.town, self.state, self.zipcode, self.country]
        non_null_values = [s.replace(' ','+') for s in values if s is not None]
        return 'https://www.google.com/maps/search/{}/'.format(
            (',+').join(non_null_values)
        )
    

    @property
    def event_index(self):
        # Find closest ancestor which is an event index
        return self.get_ancestors().type(EventIndexPage).last()

    def serve(self, request):
        if "format" in request.GET:
            if request.GET['format'] == 'ical':
                # Export to ical format
                response = HttpResponse(
                    export_event(self, 'ical'),
                    content_type='text/calendar',
                )
                response['Content-Disposition'] = 'attachment; filename=' + self.slug + '.ics'
                return response
            else:
                # Unrecognised format error
                message = 'Could not export event\n\nUnrecognised format: ' + request.GET['format']
                return HttpResponse(message, content_type='text/plain')
        else:
            # Display event page as usual
            return super(EventPage, self).serve(request)