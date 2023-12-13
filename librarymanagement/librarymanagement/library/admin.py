from django.contrib import admin

from .models import Book , role, role_map , Transactions

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'authors', 'average_rating', 'isbn', 'publication_date', 'publisher_name', 'is_rent')
    list_filter = ('is_rent', 'language_code', 'publication_date')
    search_fields = ('title', 'authors', 'isbn', 'isbn13', 'publisher_name')
    ordering = ('-publication_date',)


@admin.register(role)
class roleAdmin(admin.ModelAdmin):
    list_display=('id','name')


@admin.register(role_map)
class role_mapAdmin(admin.ModelAdmin):
    list_display= ('id' ,'user', 'role')


@admin.register(Transactions)
class Transactions(admin.ModelAdmin):
    list_display= ('id' ,'user', 'issue_date' , 'due_date' , 'return_date', 'rent_fee')
