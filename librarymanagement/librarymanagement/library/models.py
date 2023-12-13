from typing import Any
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta

current_datetime = datetime.now()

class Book(models.Model):
    IS_RENT = [(0,'NO'),(1,'YES')]
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2)
    isbn = models.CharField(max_length=13)
    isbn13 = models.CharField(max_length=13)
    language_code = models.CharField(max_length=3)
    num_pages = models.IntegerField(null=True, blank=True)
    ratings_count = models.IntegerField()
    text_reviews_count = models.IntegerField()
    publication_date = models.DateField()
    publisher_name = models.CharField(max_length=254)
    is_rent = models.IntegerField(choices=IS_RENT , default=0)



class role(models.Model):
    name =models.CharField(max_length=255)

    def __str__(self):
            return self.name

    class Meta:
        verbose_name_plural = 'Roles'

class role_map(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(role , on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Role Map'



class Member_Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debt = models.IntegerField( default=0)

class Transactions(models.Model):
    user = models.ForeignKey(User , on_delete=models.DO_NOTHING )
    book = models.ForeignKey(Book , on_delete=models.DO_NOTHING)
    issue_date = models.DateField(auto_now_add=True)   # add automatic 
    due_date = models.DateField(null= True, blank=True)
    return_date = models.DateField( null=True, blank=True)
    rent_fee = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Set due_date to issue_date + 7 days if it's not already set
        if not self.due_date:
            self.due_date = current_datetime + timedelta(days=7)

        super().save(*args, **kwargs)

    def calculate_rent_fee(self):
        
        # if self.return_date and self.return_date > self.due_date:
        if  self.due_date < current_datetime.date():
            # days_overdue = (self.return_date - self.due_date).days
            days_overdue = (current_datetime.date() - self.due_date).days
            print(days_overdue , "days_overdue")
            self.rent_fee = 10 * days_overdue
            self.save()
            print(self.rent_fee ,"+++++++++++++")
            return self.rent_fee
        else:
            print("----here")
            return 0
        
        
        
    