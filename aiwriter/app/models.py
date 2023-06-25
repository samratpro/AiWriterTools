from django.db import models

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
    article = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class SingleKeywordModel(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    article = models.TextField(blank=True)

    def __str__(self):
        return self.name
