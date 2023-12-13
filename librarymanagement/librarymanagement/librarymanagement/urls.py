
from django.contrib import admin
from library.views import *
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login, name="login"),
    path('logout/', logout_view, name="logout"),
    path('home/', home, name="home"),
    # path('add_book/', add_book, name="add_book"),
    path('save_books_from_api/', save_books_from_api.as_view(), name='save_books_from_api'),
    path('book_import/', book_import, name='book_import'),
    path('book_store/', book_store, name='book_store'),
    path('members/', members, name='members'),
    path('create_members/', add_edit_members, name='create_members'),
    path('create_members/<member_id>', add_edit_members, name='create_members'),
    path('delete_members/<member_id>', delete_members, name='delete_members'),


    path('book_details/<bookid>/', book_details, name='book_details'),

    path('issue_book/<bookid>/', issue_book, name='issue_book'),
    path('transection/', transactions, name='transactions'),

    path('transection_history/', transactions_history, name='transactions_history'),
    path('return_book/<transectionID>', return_book, name='return_book'),
    path('calculate_dues/<transectionID>', calculate_dues, name='calculate_dues'),


]    

