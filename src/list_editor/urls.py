from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("deck", views.DeckEditor.as_view()),
    path("card/search", views.CardSearch.as_view()),
]