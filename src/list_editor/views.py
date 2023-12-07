from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
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


@require_http_methods(["POST"])
def card_search(request):
    query = request.POST['search']
    search_results = []
    if len(query) != 0:
        search_results = Card.objects.filter(name__contains=query)

    context = {
        "search_results": search_results
    }
    return render(request, 'deck_editor.html', context)
