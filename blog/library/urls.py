from django.urls import path
from library import views as lib_views

urlpatterns = [
    path('library/', lib_views.book_list, name='book_list'),
    path('library/<int:book_id>/', lib_views.book_detail, name='book_detail'),
    path('book/<int:book_id>/borrow/', lib_views.borrow_book, name='library_borrow_book'),
    path('loans/<int:loan_id>/return/', lib_views.return_loan, name='library_return_loan'),
    path('library/add/', lib_views.add_book, name='add_book'),
    path('library/<int:book_id>/edit/', lib_views.edit_book, name='edit_book'),
    path('library/author/add/', lib_views.add_author, name='add_author')

]
