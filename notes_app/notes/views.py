from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def greeting(request):
    return HttpResponse("Hello from Notes app")


def create_notes(request):
    notes = [
        {
            "title": "First Note",
            "content": "This is a content of first note."
        }, {
            "title": "Second Note",
            "content": "This is a content of second note with some important information."
        }, {
            "title": "Reminder",
            "content": "To buy bread, milk and coffee."
        }, {
            "title": "Idea of the project",
            "content": "To create a task management app."
        }, {
            "title": "Quote of the day",
            "content": '"Everything that does not kill us makes us stronger." - Nietzsche.'
        },
    ]

    return render(request, "index.html", {"notes": notes})
