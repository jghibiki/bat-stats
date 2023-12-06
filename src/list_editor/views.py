from django.http import HttpResponse
from django.shortcuts import render
from .models import Card, Affiliations, AppModelVersion

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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