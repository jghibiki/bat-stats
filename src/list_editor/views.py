from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views import View
from django.core.paginator import Paginator
from django.http import HttpRequest
from django_htmx.middleware import HtmxDetails

from .models import Card, Affiliation, AppModelVersion


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def create_list(request):
    pass
    # create a view to create a list. Take in list name, affiliation, leader.


def search_cards(query, page):
    latest_app_version = AppModelVersion.get_current_version()
    if query is not None and len(query) >= 0:
        search_results = latest_app_version.cards.filter(name__icontains=query)
    else:
        search_results = latest_app_version.cards.all()
    paginator = Paginator(
        search_results.order_by("id"),
        5
    )
    return paginator.get_page(page)


class DeckEditor(View):

    def get(self, request: HtmxHttpRequest):
        context = {
            "search_results": search_cards(None, 1),
            "page": request.GET.get("page", 1),
        }
        return render(request, 'list_editor/deck_editor.html', context)


class CardSearch(View):

    def post(self, request: HtmxHttpRequest):
        query = request.POST.get('search', None)
        page = int(request.POST.get('page', 1))

        context = {
            "search_results": search_cards(query, page),
            "page": page,
            "previous_page": page - 1,
            "next_page": page + 1,
        }
        return render(request, 'htmx/card_search_result.html', context)
