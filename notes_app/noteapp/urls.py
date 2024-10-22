from django.urls import path
from noteapp.views import notes_view, note_detail_view, search_notes_view

urlpatterns = [
    path('notes/', notes_view, name= "notes"),
    path('notes/<slug:slug>/', note_detail_view, name= "note_detail"),
    path('notes-search/', search_notes_view, name='notes-search')
]
