
from django.contrib import admin       # Import the Django admin module.
from library.views import *            # Import all views from the library app
from django.urls import path           # Import the path function from django.urls. 

urlpatterns = [
    path('admin/', admin.site.urls),                                               # Admin URL configuration.
    path('', login, name="login"),                                                 # URL for the login view with the name "login".   
    path('logout/', logout_view, name="logout"),                                   # URL for the login view with the name "login".
    path('home/', home, name="home"),                                              # URL for the home view with the name "home".
    # path('add_book/', add_book, name="add_book"),
    path('save_books_from_api/', save_books_from_api.as_view(), name='save_books_from_api'),   # URL for the save_books_from_api view with the name "save_books_from_api".
    path('book_import/', book_import, name='book_import'),                                     # URL for the book_import view with the name "book_import"
    path('book_store/', book_store, name='book_store'),                                        # URL for the book_store view with the name "book_store"
    path('members/', members, name='members'),                                                 # URL for the members view with the name "members".
    path('create_members/', add_edit_members, name='create_members'),                          # URL for the create_members view without a member_id parameter.
    path('create_members/<member_id>', add_edit_members, name='create_members'),               # URL for the create_members view with a member_id parameter.
    path('delete_members/<member_id>', delete_members, name='delete_members'),                 # URL for the delete_members view with a member_id parameter.


    path('book_details/<bookid>/', book_details, name='book_details'),                         # URL for the book_details view with a dynamic bookid parameter.

    path('issue_book/<bookid>/', issue_book, name='issue_book'),                               # URL for the issue_book view with a dynamic bookid parameter.
    path('transection/', transactions, name='transactions'),                                   # URL for the transactions view.

    path('transection_history/', transactions_history, name='transactions_history'),           # URL for the transactions_history view
    path('return_book/<transectionID>', return_book, name='return_book'),                      # URL for the return_book view with a dynamic transectionID parameter
    path('calculate_dues/<transectionID>', calculate_dues, name='calculate_dues'),             #URL for the calculate_dues view with a dynamic transectionID parameter


]    

