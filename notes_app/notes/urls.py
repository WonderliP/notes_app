from django.urls import path
from .views import greeting, create_notes, NoteCreateView, NoteDetailView, NoteUpdateView, NoteDeleteView, NoteListView

urlpatterns = [
    path("greet/", greeting),
    path("notes/", create_notes),

    path("", NoteListView.as_view(), name="note_list"),
    path("create/", NoteCreateView.as_view(), name="note_create"),
    path("<int:pk>/", NoteDetailView.as_view(), name="note_detail"),
    path("<int:pk>/edit/", NoteUpdateView.as_view(), name="note_update"),
    path("<int:pk>/delete/", NoteDeleteView.as_view(), name="note_delete"),
]
