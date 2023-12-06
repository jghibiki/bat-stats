from django.http import HttpResponse
from django.shortcuts import render
from .models import Card, Affiliation, AppModelVersion

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def create_list(request):
    pass
    # create a view to create a list. Take in list name, affiliation, leader.

def deck_editor(request):
    app_version = AppModelVersion.get_current_version()
    cards = Card.objects.filter(app_version=app_version)[:5]
    context = {
        "card_options": cards
    }
    return render(
        request,
        "list_editor/deck_editor.html",
        context
    )