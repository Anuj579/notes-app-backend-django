from django.contrib import admin
from .models import Note, Profile

# Register your models here.


class NoteAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "category", "created_at", "updated_at"]


admin.site.register(Note, NoteAdmin)
admin.site.register(Profile)
