from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BorrowForm, BookForm, AuthorForm
from .models import Author, Book, Loan


def book_list(request):
    q = request.GET.get('q', '').strip()
    author_id = request.GET.get('author', '').strip()
    print()
    books = Book.objects.select_related('author').prefetch_related('tags')

    if q:
        books = books.filter(title__icontains=q)

    if author_id:
        books = books.filter(author_id=author_id)

    open_loans = Loan.objects.filter(returned_at__isnull=True).select_related('student', 'book')
    books = books.prefetch_related(Prefetch('loans', queryset=open_loans, to_attr='open_loans'))

    authors = Author.objects.order_by('name')

    return render(
        request,
        'library/book_list.html',
        {
            'books': books.order_by('title'),
            'authors': authors,
            'q': q,
            'author_id': author_id,
        },
    )


def book_detail(request, book_id):
    open_loans = Loan.objects.filter(returned_at__isnull=True).select_related('student')

    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('tags').prefetch_related(
            Prefetch('loans', queryset=open_loans, to_attr='open_loans')
        ),
        id=book_id,
    )

    current_loan = book.open_loans[0] if getattr(book, 'open_loans', []) else None
    borrow_form = BorrowForm()

    return render(
        request,
        'library/book_detail.html',
        {
            'book': book,
            'current_loan': current_loan,
            'borrow_form': borrow_form,
        },
    )


from django.dispatch import Signal

book_borrowed = Signal()


def borrow_book(request, book_id):
    if request.method != 'POST':
        return redirect('book_detail', book_id=book_id)
    book = get_object_or_404(Book, id=book_id)

    if Loan.objects.filter(book=book, returned_at__isnull=True).exists():
        return redirect('book_detail', book_id=book_id)

    form = BorrowForm(request.POST)

    if form.is_valid():
        loan = form.save(commit=False)
        loan.book = book
        loan.save()

    return redirect('book_detail', book_id=book_id)


def return_loan(request, loan_id):
    if request.method != 'POST':
        return redirect('book_list')
    loan = get_object_or_404(Loan, id=loan_id)
    if loan.returned_at is None:
        loan.returned_at = timezone.now()
    loan.save(update_fields=['returned_at'])
    return redirect('book_detail', book_id=loan.book_id)


@permission_required("library.add_book")
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm()
    return render(request, 'library/add_book.html', {'form': form})


@permission_required("library.edit_book")
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'library/edit_book.html', {'form': form, 'book': book})


@permission_required("library.add_author")
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return redirect('book_list')
    else:
        form = AuthorForm()
    return render(request, 'library/add_author.html', {'form': form})
