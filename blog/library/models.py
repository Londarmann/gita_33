from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    birth_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BookQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def available(self):
        return self.active().exclude(loans__returned_at__isnull=True).distinct()


class Book(models.Model):
    title = models.CharField(max_length=200)
    published_year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='books')
    tags = models.ManyToManyField(Tag, blank=True, related_name='books')

    objects = BookQuerySet.as_manager()

    def __str__(self):
        return self.title


class Student(models.Model):
    full_name = models.CharField(max_length=200)
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.full_name


class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='loans')

    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book} -> {self.student}"