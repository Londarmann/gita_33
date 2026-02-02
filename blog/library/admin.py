from django.contrib import admin

from library.models import Book, Loan, Student, Tag, Author


# Register your models here.
#  ავტომატური იქნება
# admin.site.register(Loan)
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'borrowed_at', 'returned_at')
    search_fields = ('book__title', 'student__full_name')
    list_filter = ('borrowed_at', 'returned_at')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'grade')
    search_fields = ('full_name',)
    list_filter = ('grade',)


# ნახევრად ავტომატური

# admin.site.register(Book)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_year', 'is_active')
    search_fields = ('title', 'author__name')
    list_filter = ('is_active', 'published_year', 'author')
    ordering = ('-published_year',)
    filter_horizontal = ('tags',)


admin.site.register(Author)


# ხელით შესაყვანი

# admin.site.register(Tag)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')
