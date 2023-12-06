from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("deck", views.deck_editor, name="deck_editor")
]