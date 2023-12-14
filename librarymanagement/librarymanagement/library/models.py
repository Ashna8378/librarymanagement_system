from typing import Any      # The typing module is imported for type hints (not currently used in the provided code).
from django.contrib.auth.models import User
from django.db import models       # The models module contains various Django model-related classes.
from datetime import datetime, timedelta   #This line captures the current date and time. It is used later in the code for calculating due dates and rent fees.

current_datetime = datetime.now()

class Book(models.Model):    # Defines a Django model named Book with various fields representing book attributes (title, authors, etc.).
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



class role(models.Model):          # Defines a Django model named role representing user roles. It has a single field, name.
    name =models.CharField(max_length=255)

    def __str__(self):             # The __str__ method returns a string representation of the model instance.
            return self.name

    class Meta:                         # The Meta class inside a Django model allows you to provide additional options and configurations for the model.
        verbose_name_plural = 'Roles'   # sets the plural name (displayed in the Django admin interface) for instances of the role model. By default, Django would pluralize the model name by appending an "s" to it. However, using verbose_name_plural, you can provide a custom plural name.

class role_map(models.Model):           # This line defines a Django model named role_map. It inherits from the models.Model class, indicating that it is a Django model.
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # This line defines a foreign key field named user.
                                                              # models.ForeignKey is used to create a relationship between the role_map model and the User model from django.contrib.auth.models.
                                                              # on_delete=models.CASCADE option ensures that when a related User or role is deleted, the corresponding role_map instances are also deleted, maintaining data integrity.
                                                              
    role = models.ForeignKey(role , on_delete=models.CASCADE)  # This line defines another foreign key field named role.
                                                               # models.ForeignKey is used to create a relationship between the role_map model and the User model from django.contrib.auth.models.
                                                                # on_delete=models.CASCADE option ensures that when a related User or role is deleted, the corresponding role_map instances are also deleted, maintaining data integrity. 

    class Meta:                              # The Meta class inside a Django model allows you to provide additional options and configurations for the model.    
        verbose_name_plural = 'Role Map'     # sets the plural name (displayed in the Django admin interface) for instances of the role model. By default, Django would pluralize the model name by appending an "s" to it. However, using verbose_name_plural, you can provide a custom plural name.



class Member_Debt(models.Model):             # This line defines a Django model named Member_Debt. It inherits from the models.Model class, indicating that it is a Django model.
    user = models.ForeignKey(User, on_delete=models.CASCADE) # This line defines a foreign key field named user
                                                             # models.ForeignKey is used to create a relationship between the Member_Debt model and the User model from django.contrib.auth.models.
                                                             # on_delete=models.CASCADE option ensures that when a related User is deleted, the corresponding Member_Debt instances are also deleted, maintaining data integrity.
                                                               
    debt = models.IntegerField( default=0)                   # This line defines an integer field named debt.
                                                             # models.IntegerField is used to store integer values.
                                                             # The default=0 ensures that if no debt value is provided, it defaults to 0.

class Transactions(models.Model):                                  # This line defines a Django model named Transactions. It inherits from the models.Model class, indicating that it is a Django model.
    user = models.ForeignKey(User , on_delete=models.DO_NOTHING )  # This line defines a foreign key field named user
                                                                   # models.ForeignKey is used to create a relationship between the Transactions model and the User model from
                                                                   # on_delete=models.DO_NOTHING specifies that when the referenced User instance is deleted, nothing should happen to the related Transactions instances
                                                                   
    book = models.ForeignKey(Book , on_delete=models.DO_NOTHING)   # This line defines a foreign key field named book
                                                                   # models.ForeignKey is used to create a relationship between the Transactions model and the Book model 
                                                                   # on_delete=models.DO_NOTHING specifies that when the referenced Book instance is deleted, nothing should happen to the related Transactions instances
                                                                   
    issue_date = models.DateField(auto_now_add=True)               # This line defines a date field named issue_date.
                                                                   # models.DateField is used to store date values.
                                                                   # auto_now_add=True automatically sets the issue_date to the current date and time when a new Transactions instance is created.
                                                                   
    due_date = models.DateField(null= True, blank=True)            # This line defines another date field named due_date.
                                                                   # null=True allows the field to have a NULL value in the database.
                                                                   # blank=True allows the field to be left blank in forms.
                                                                   
    return_date = models.DateField( null=True, blank=True)         # This line defines a date field named return_date.
                                                                   # Similar to due_date, it allows a NULL value and can be left blank.
                                                                   
    rent_fee = models.IntegerField(default=0)                      # This line defines an integer field named rent_fee
                                                                   # default=0 sets the default value for the rent_fee field to 0. If a value is not provided when creating a new Transactions instance, it will default to 0.

    def save(self, *args, **kwargs):                                         # This line defines a custom save method for the Transactions model. The save method is called when saving an instance of the model to the database
                                                                             
        # Set due_date to issue_date + 7 days if it's not already set
        if not self.due_date:                                               # The line checks if the due_date field of the Transactions instance is not already set (i.e., if it's None or an empty value).
            self.due_date = current_datetime + timedelta(days=7)            # It adds 7 days to the current_datetime, which was defined earlier in the code as the current date and time.
                                                                            
        super().save(*args, **kwargs)                                      # This line calls the save method of the parent class (models.Model).
                                                                           # It passes along any arguments and keyword arguments received by the custom save method.
                                                                           # This ensures that the normal saving process for a Django model is executed.
 
    def calculate_rent_fee(self):                                          # This line defines a method named calculate_rent_fee within the Transactions model.
        
        # if self.return_date and self.return_date > self.due_date:        
        if  self.due_date < current_datetime.date():                       # This line checks if the due_date is in the past (i.e., the book is overdue).
            # days_overdue = (self.return_date - self.due_date).days       # current_datetime.date() is used to get the current date without the time component.
            days_overdue = (current_datetime.date() - self.due_date).days   # If the book is overdue, this line calculates the number of days it is overdue.
                                                                            # It subtracts the due_date from the current date and takes the days component of the resulting timedelta.
                                                                            
            print(days_overdue , "days_overdue")                             
            self.rent_fee = 10 * days_overdue                               # This line calculates the rent fee based on the number of days the book is overdue.
                                                                            # The rent fee is set to 10 times the number of days overdue.
            
            self.save()                                                     # This line saves the Transactions instance to the database.
                                                                            # It is necessary to persist the calculated rent fee
            print(self.rent_fee ,"+++++++++++++")
            return self.rent_fee                                            # This line returns the calculated rent fee.
        else:                                                               # If the book is not overdue, this block of code is executed.
            print("----here")
            return 0
        
        
        
    