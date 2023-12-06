from django.contrib import admin

# Register your models here.
from .models import (
    AppModelVersion,
    Affiliation,
    Card,
    Equipment,
    Trait,
    Upgrade,
    Weapon,
    RuleDocument,
    Character,
    CrewList,
    Deck
)

admin.site.register(AppModelVersion)
admin.site.register(Affiliation)
admin.site.register(Card)
admin.site.register(Equipment)
admin.site.register(Trait)
admin.site.register(Upgrade)
admin.site.register(Weapon)
admin.site.register(RuleDocument)
admin.site.register(Character)

admin.site.register(CrewList)
admin.site.register(Deck)
