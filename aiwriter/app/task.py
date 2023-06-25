# cron.py
from .models import *
from time import sleep


def BulkKeywordsJob():
    pending_keywords = BulkKeywordModel.objects.filter(status='Pending')
    for keyword in pending_keywords:
        # Process the keyword here using AI API or any other task
        # Update the keyword status to indicate completion
        sleep(10)
        keyword.article = 'Article'
        keyword.status = 'Completed'
        keyword.save()
    
