from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)


    class Meta:
        ordering = ['last_name', 'first_name']


    def get_absolute_url(self):
        return reverse("author_detail", args=[str(self.pk)])
  

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Genre(models.Model):
    name = models.CharField(max_length=50, help_text="Enter a book genre")


    def __str__(self):
        return self.name


class Language(models.Model):
    language = models.CharField(max_length=150)

    
    def __str__(self):
        return self.language
    

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, verbose_name="author")
    summary = models.TextField(max_length=1000, help_text="Краткое описание того, о чем книга")
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр(ы) для книги")
    isbn = models.CharField("ISBN", max_length=13, unique=True, help_text="13 цифр ISBN(идентификатор издательства)")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)


    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    
    display_genre.short_description = "Жанр"

 
    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("book_detail", args=[str(self.pk)])


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Уникальный id связанный с id книги")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=150)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ("то", "Техобслуживание"),
        ("п", "В прокате"),
        ("д", "Доступна"),
        ("з", "Зарезервировано")
    )

    status = models.CharField(max_length=2, choices=LOAN_STATUS, default="д", help_text="Доступность книги")


    class Meta:
        ordering = ['due_back']


    def __str__(self):
        return f'{self.id} ({self.book.title})'

    
    
