from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class OpenaiAPIModel(models.Model):
    name = models.CharField(max_length=150)
    API_Key = models.CharField(max_length=500)
    engine = models.CharField(max_length=150, default="text-davinci-003")
    
    def __str__(self):
        return self.name

class YoutubeAPIModel(models.Model):
    name = models.CharField(max_length=150)
    API_Key = models.CharField(max_length=500)
    
    def __str__(self):
        return self.name


# Create your models here.
class WesiteModel(models.Model):
    website_name = models.CharField(max_length=150)
    website_url = models.CharField(max_length=250)
    username = models.CharField(max_length=100)
    app_pass = models.CharField(max_length=200)

    def __str__(self):
        return self.website_name

class BulkKeywordModel(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    content = RichTextUploadingField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class SingleKeywordModel(models.Model):
    name = models.CharField(max_length=100)
    outline = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='Pending')
    content = RichTextUploadingField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
