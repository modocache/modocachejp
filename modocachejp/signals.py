from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tastypie.models import create_api_key


post_save(create_api_key, sender=User)
