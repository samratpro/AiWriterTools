from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(WesiteModel)
admin.site.register(BulkKeywordModel)

# Changing the Django Admin Header Text
admin.site.site_header = 'AI Writing Tools'