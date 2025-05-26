from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from notes.forms import NoteForm, LoginForm, RegisterForm
from notes.models import Note


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Вітаємо, {username}")
                return redirect("note_list")
            else:
                messages.error(request, "Неправильне ім'я користувача або пароль")
        return render(request, "login.html", {"form": form})


def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {"form": form})

    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Успішна реєстрація")
            return redirect("note_list")
        return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Ви успішно вийшли з системи")
    return redirect("login")


def greeting(request):
    return HttpResponse("Hello from Notes app")


def create_notes(request):
    notes = Note.objects.all()
    return render(request, "note_list.html", {"notes": notes})


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"
    success_url = reverse_lazy("note_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = "note_detail.html"
    context_object_name = "note"

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.filter(user__isnull=True)

        user_groups = self.request.user.note_groups.all()
        group_notes = Note.objects.filter(groups__in=user_groups)
        return queryset.filter(user=self.request.user) | group_notes | queryset.filter(user__isnull=True)


class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "note_form.html"

    def test_func(self):
        note = self.get_object()
        return note.user == self.request.user

    def get_success_url(self):
        return reverse_lazy("note_detail", kwargs={"pk": self.object.pk})


class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = "note_confirm_delete.html"
    success_url = reverse_lazy("note_list")

    def test_func(self):
        note = self.get_object()
        return note.user == self.request.user


class NoteListView(ListView):
    model = Note
    template_name = "note_list.html"
    context_object_name = "notes"

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category")
        search_title = self.request.GET.get("search")

        if category:
            queryset = queryset.filter(category__title=category)

        if search_title:
            queryset = queryset.filter(title__icontains=search_title)

        return queryset