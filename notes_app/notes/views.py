from django.shortcuts import render
from django.http import HttpResponse

from notes.models import Note


# Create your views here.
def greeting(request):
    return HttpResponse("Hello from Notes app")


def create_notes(request):
    notes = Note.objects.all()
    return render(request, "index.html", {"notes": notes})
