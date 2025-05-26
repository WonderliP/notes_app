from django.contrib import admin

from notes.models import Note


# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "reminder", "text")
    list_filter = ("category", "reminder")
    search_fields = ("title", "category__title")
    date_hierarchy = "reminder"


admin.site.register(Note, NoteAdmin)
