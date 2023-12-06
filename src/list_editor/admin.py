from django.contrib import admin

# Register your models here.
from .models import AppModelVersion, Affiliations, Card

admin.site.register(AppModelVersion)
admin.site.register(Affiliations)
admin.site.register(Card)
