from django import forms
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailusers.forms import UserEditForm, UserCreationForm

from .models import Member


class MemberEditForm(UserEditForm):
    nickname = forms.CharField(required=False, label=_("Call Him"))
    graduation_year = forms.IntegerField(
        required=True, 
        label=_("Graduation Year"),
        min_value=1974)
    img = forms.ImageField(
        required=False,
        label=_("Display Image")
        )
    home_town = forms.CharField(
        required=False,
        label=_("Hometown")
        )
    major = forms.CharField(label=_("Major"))
    voice_part = forms.CharField(label=_("Voice Part"))
    current = forms.BooleanField(label=_("Current Member"))
    bio = forms.CharField(label=_("Bio"), widget=forms.Textarea, required=False)
    phone = forms.CharField(label=_("Phone Number"), required=False)
    location = forms.CharField(label=_("Location"), required=False)
    website = forms.URLField(label=_("Website"), required=False)
    linkedin = forms.URLField(label=_("Linkedin"), required=False)
    facebook = forms.URLField(label=_("Facebook"), required=False)
    instagram = forms.URLField(label=_("Instagram"), required=False)
    
    


class MemberCreationForm(UserCreationForm):
    nickname = forms.CharField(required=False, label=_("Call Him"))
    graduation_year = forms.IntegerField(
        required=True, 
        label=_("Graduation Year"),
        min_value=1974)
    img = forms.ImageField(
        required=False,
        label=_("Display Image")
        )
    home_town = forms.CharField(
        required=False,
        label=_("Hometown")
        )
    major = forms.CharField(label=_("Major"))
    voice_part = forms.CharField(label=_("Voice Part"))
    current = forms.BooleanField(label=_("Current Member"))
    bio = forms.CharField(label=_("Bio"), widget=forms.Textarea, required=False)
    phone = forms.CharField(label=_("Phone Number"), required=False)
    location = forms.CharField(label=_("Location"), required=False)
    website = forms.URLField(label=_("Website"), required=False)
    linkedin = forms.URLField(label=_("Linkedin"), required=False)
    facebook = forms.URLField(label=_("Facebook"), required=False)
    instagram = forms.URLField(label=_("Instagram"), required=False)