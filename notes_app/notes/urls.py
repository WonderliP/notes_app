from django.urls import path
from .views import greeting, create_notes

urlpatterns = [
    path("greet/", greeting),
    path("notes/", create_notes)
]
