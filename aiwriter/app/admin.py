from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(WesiteModel)
admin.site.register(BulkKeywordModel)
admin.site.register(OpenaiAPIModel)
admin.site.register(YoutubeAPIModel)
admin.site.register(SingleKeywordModel)

# Changing the Django Admin Header Text
admin.site.site_header = 'AI Writing Tools'