from django import forms
from django.forms import TextInput, Textarea

class WebsiteForms(forms.Form):
    website_name = forms.CharField(widget=TextInput(attrs={'placeholder': 'Website Name', 'class': 'form-control mb-3 mt-3'}))
    website_url = forms.URLField(widget=TextInput(attrs={'placeholder': 'Website URL', 'class': 'form-control mb-3'}))
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username', 'class': 'form-control mb-3'}))
    app_pass = forms.CharField(widget=TextInput(attrs={'placeholder': 'Application Password', 'class': 'form-control mb-3'}))


class OpenaiAPIForm(forms.Form):
    name = forms.CharField(widget=TextInput(attrs={'placeholder': 'API Name', 'class': 'form-control mb-3 mt-3'}))
    apikey = forms.CharField(widget=TextInput(attrs={'placeholder': 'API Key', 'class': 'form-control mb-3 mt-3'}))
    api_engine = forms.CharField(widget=TextInput(attrs={'placeholder': 'API Engine', 'class': 'form-control mb-3 mt-3'}))

class YoutubeAPIForm(forms.Form):
    name = forms.CharField(widget=TextInput(attrs={'placeholder': 'API Name', 'class': 'form-control mb-3 mt-3'}))
    apikey = forms.CharField(widget=TextInput(attrs={'placeholder': 'API Key', 'class': 'form-control mb-3 mt-3'}))
    