from django.contrib import admin
from .models import Note
from django.contrib.auth.models import User

# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at', 'updated_at', 'user']
admin.site.register(Note, NoteAdmin)