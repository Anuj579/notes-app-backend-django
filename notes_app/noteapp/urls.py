from django.urls import path
from noteapp.views import notes_view

urlpatterns = [
    path('notes/', notes_view, name= "notes"),
]
