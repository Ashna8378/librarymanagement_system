from django.contrib import admin

from .models import Book , role, role_map , Transactions


# Registering the Book model with the admin site
@admin.register(Book)                 # Decorator syntax for registering the Book model with the admin site.
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'authors', 'average_rating', 'isbn', 'publication_date', 'publisher_name', 'is_rent')    #list_display: Specifies the fields that will be displayed in the list view of the admin interface. It includes the fields
    list_filter = ('is_rent', 'language_code', 'publication_date')        # list_filter: Adds filters to the right sidebar of the admin interface, allowing users to filter books based on 
    search_fields = ('title', 'authors', 'isbn', 'isbn13', 'publisher_name')   # : Adds a search box to the admin interface, enabling users to search for books based on
    ordering = ('-publication_date',)               # ordering: Sets the default ordering of the list view, in this case, ordering books by -publication_date in descending order.ordering: Sets the default ordering of the list view, in this case, ordering books by -publication_date in descending order.


@admin.register(role)     # This is a decorator that registers the role model with the Django admin site. It's a convenient way to use the default ModelAdmin options for a model.
class roleAdmin(admin.ModelAdmin):
    list_display=('id','name')


@admin.register(role_map)       # This is a decorator that registers the role_map model with the Django admin site. It's a convenient way to use the default ModelAdmin options for a model. It is equivalent to 
class role_mapAdmin(admin.ModelAdmin):
    list_display= ('id' ,'user', 'role')


@admin.register(Transactions)   #  This is a decorator that registers the Transactions model with the Django admin site. It's a convenient way to use the default ModelAdmin options for a model
class Transactions(admin.ModelAdmin):  # This class allows you to customize the behavior and appearance of the admin interface for the Transactions model.
    list_display= ('id' ,'user', 'issue_date' , 'due_date' , 'return_date', 'rent_fee')
