from django.apps import AppConfig
from django_cron import CronJobManager


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
