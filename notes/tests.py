import pytest
import factory
from django.urls import reverse
from django.utils import timezone
from django.forms.models import model_to_dict

from .models import Category, Note
from .forms import NoteForm


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Sequence(lambda n: f"Категорія {n}")


class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note

    title = factory.Faker("sentence")
    text = factory.Faker("text")
    reminder = factory.LazyFunction(timezone.now)
    category = factory.SubFactory(CategoryFactory)


@pytest.fixture
def category():
    return CategoryFactory()


@pytest.fixture
def note(category):
    return NoteFactory(category=category)


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(title="Спорт")

    assert category.id is not None
    assert category.title == "Спорт"


@pytest.mark.django_db
def test_create_note(category):
    note = Note.objects.create(
        title="Тестова нотатка",
        text="Текст для перевірки створення",
        reminder=timezone.now(),
        category=category
    )

    assert note.title == "Тестова нотатка"
    assert note.category == category


@pytest.mark.django_db
def test_note_form_valid(category):
    form_data = {
        "title": "Тестова нотатка",
        "text": "Текст для створення тестової нотатки",
        "reminder": "2010-08-03",
        "category": category.id
    }

    form = NoteForm(data=form_data)

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_create_note_view(client, category):
    url = reverse("note_create")
    note_data = {
        "title": "Нова нотатка",
        "text": "Тестовий текст",
        "reminder": timezone.now().strftime("%Y-%m-%d"),
        "category": category.id
    }
    response = client.get(url)
    assert response.status_code == 200

    response = client.post(url, note_data)
    assert response.status_code == 302
    note = Note.objects.get(title="Нова нотатка")
    assert note.title == "Нова нотатка"


@pytest.mark.django_db
def test_edit_note_view(client, note):
    url = reverse("note_update", args=[note.id])
    updated_data = {
        "title": "Оновлена нотатка",
        "text": note.text,
        "reminder": note.reminder.strftime("%Y-%m-%d"),
        "category": note.category.id
    }

    response = client.post(url, updated_data)

    assert response.status_code == 302
    note.refresh_from_db()
    assert note.title == "Оновлена нотатка"


@pytest.mark.django_db
def test_delete_note_view(client, note):
    url = reverse("note_delete", args=[note.id])
    response = client.post(url)

    assert response.status_code == 302
    assert not Note.objects.filter(pk=note.pk).exists()
