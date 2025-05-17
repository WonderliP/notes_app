from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from notes.forms import NoteForm
from notes.models import Note


# Create your views here.
def greeting(request):
    return HttpResponse("Hello from Notes app")


def create_notes(request):
    notes = Note.objects.all()
    return render(request, "index.html", {"notes": notes})


class NoteCreateView(CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note_list")


class NoteDetailView(DetailView):
    model = Note
    template_name = "note_detail.html"


class NoteUpdateView(UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note_list")


class NoteDeleteView(DeleteView):
    model = Note
    template_name = "note_confirm_delete.html"
    success_url = reverse_lazy("note_list")


class NoteListView(ListView):
    model = Note
    template_name = "note_list.html"
    context_object_name = "notes"

    def get_queryset(self):
        return super().get_queryset()
