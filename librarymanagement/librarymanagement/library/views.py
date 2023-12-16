from django.shortcuts import redirect, render               # These functions are used to handle HTTP responses and rendering templates.
import json                                                 # Imports the json module for working with JSON data.
from library.models import Book , role_map, role            # Imports the Book, role_map, and role models from the library app.
from django.contrib.auth.models import User                 # Imports the User model from django.contrib.auth.models.
from datetime import datetime                               # Imports the datetime class from the datetime module for handling date and time.
from django.http import JsonResponse                        # Imports the JsonResponse class from django.http for returning JSON responses.
import requests                                             # Imports the requests library for making HTTP requests.
from rest_framework.views import APIView                    # Imports the APIView class from rest_framework.views. This is a base class for creating API views.
from django.views.decorators.csrf import csrf_exempt        # Imports the csrf_exempt decorator to exempt a view from CSRF protection.
from django.utils.decorators import method_decorator        # Imports the method_decorator utility for decorating class-based views with function-based decorators
from .forms import *                                        # Imports all forms defined in the forms.py file within the same directory.
from django.db.models import Q                              # Imports the Q object for complex queries.
from django.contrib.auth import authenticate, logout, login # Imports functions for user authentication (authenticate, logout, login).
from django.contrib import messages, auth                   # Imports modules for displaying messages and managing user authentication
from django.shortcuts import get_object_or_404              # Imports the get_object_or_404 function for getting an object by its primary key or returning a 404 response.




def login(request):                                                            # This defines a function named login that handles user login.
    if request.method == 'POST':                                               # Checks if the HTTP request method is POST. This is typically the case when a form is submitted.
        print("---hijlklnnk")                                                  # This is a print statement that outputs ---hijlklnnk to the console. It's likely used for debugging purposes to check if the code reaches this point.
        username=request.POST.get("uname")                                     # Retrieves the value of the "uname" parameter from the POST data. This is likely the entered username from the login form.
        password=request.POST.get("pass")                                      # Retrieves the value of the "pass" parameter from the POST data. This is likely the entered password from the login form.
        
        user = authenticate(username=username, password=password)              # Uses Django's authenticate function to check if the provided username and password match a user in the database. If successful, user will be the authenticated user object; otherwise, it will be None.
        if user is not None:                                                   # Checks if the authentication was successful (i.e., if user is not None).
            auth.login(request, user)                                          # Logs in the user using Django's login function. It sets the user in the session.
            print("--------------------------------------user")                # Another print statement, likely for debugging purposes.
            return redirect('book_import')                                     # Redirects the user to the 'book_import' URL if the login is successful.
        else:                                                                  # Executes if the authentication fails.
              return render(request, 'login.html', {'msg':"User not Found"})   # Renders the 'login.html' template with a message indicating that the user was not found.
    else:                                                                      # Executes if the request method is not POST (i.e., for GET requests).
        return render(request, 'login.html', locals())                         # Renders the 'login.html' template with the local variables available in the current context. This is likely used to display the login form on the initial page load.


def logout_view(request):                                                      # Defines a function named logout_view that handles user logout.                                       
    logout(request)                                                            # Calls Django's logout function, which logs out the user by removing the user's ID from the request's session data.
    return redirect('login')                                                   # Redirects the user to the 'login' URL after logging out.

def home(request):                                                             # Defines a function named home that renders the 'home.html' template.
   
    return render(request, 'home.html', locals())                              # Renders the 'home.html' template using the render function from Django. The template is rendered with the local variables available in the current context.


# def add_book(request):

#     return redirect('book_import')
#     # return render(request, "add_book.html", locals())



# save data from api
class save_books_from_api(APIView):          # This defines a class-based view named save_books_from_api that inherits from Django's APIView.
    # @method_decorator(csrf_exempt)
    def post(self, request):                 # This defines the post method within the class, which will handle HTTP POST requests.
        # data = request.data
        # print(data)
        if request.method == 'POST':                      # It checks if the incoming request method is indeed POST.
            # api_data = request.POST.get('api_data') 
            api_data = request.data                       # It retrieves the data from the POST request.
            if api_data:                                  # It checks if there is data in the API request.
                # data = json.loads(data)
                print(api_data)                           # It prints the received API data for debugging purposes.

                for book_data in api_data:                # It iterates through each book data in the received API data
                    book = Book(                          #  It creates a Book object using the provided data from the API.
                        title=book_data.get('title'),
                        authors=book_data.get('authors'),
                        average_rating=float(book_data.get('average_rating')),
                        isbn=book_data.get('isbn'),
                        isbn13=book_data.get('isbn13'),
                        language_code=book_data.get('language_code'),
                        # num_pages=book_data.get('num_pages'),
                        ratings_count=book_data.get('ratings_count'),
                        text_reviews_count=book_data.get('text_reviews_count'),
                        publication_date=datetime.strptime(book_data.get('publication_date'), '%m/%d/%Y').date(),
                        publisher_name=book_data.get('publisher'),
                    )
                    book.save()                            # It saves the created Book object to the database.
                    
                return JsonResponse({'message': 'Books saved successfully'})          #  If the API data is present and the books are successfully saved, it returns a JSON response indicating success.
                # return render(request, "add_book.html", locals())

            else:
                return JsonResponse({'error': 'API data is missing'}, status=400)     # If there is no API data, it returns a JSON response indicating missing data with a status code of 400.

        return JsonResponse({'error': 'Invalid request'}, status=400)                 #     If the request method is not POST, it returns a JSON response indicating an invalid request with a status code of 400.







# fetch data from api
def book_import(request):                                            # This defines a function named book_import to fetch data from an API.
    # Get the input value
    book_name = request.POST.get('book_name' , '')                   # It retrieves the values of book_name and page_no from the POST request. If not present, it defaults page_no to 1.
    page_no = request.POST.get('no_of_page', 1)
    print(book_name , "--------------------")                        # It prints the value of book_name for debugging purposes.

    # Make the API request
    api_url = 'https://frappe.io/api/method/frappe-library/'         # It sets the URL of the API to 'https://frappe.io/api/method/frappe-library/'.           
    if page_no:                                                      # It creates parameters for the API request based on the input values (book_name and page_no).
        params = {'page': page_no, 'title': book_name}
    else:
        params = {'page': 1, 'title': book_name}

    
    try:                                                              # It makes a GET request to the API using the requests.get method with the specified URL and parameters.

        response = requests.get(api_url, params=params)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:                               # If the API request is successful (status code 200), it converts the response data to JSON and renders the 'add_book.html' template with the obtained data.
            data = response.json()
            
            # return JsonResponse(data)
            return render(request, "add_book.html", locals())
        else:                                                         # If the API request is not successful, it returns a JSON response indicating the failure along with the HTTP status code.
            return JsonResponse({'error': 'Failed to fetch data from the API'}, status=response.status_code)

    except requests.RequestException as e:                            # It catches any requests.RequestException (general exception for request-related errors) and returns a JSON response indicating the failure with an HTTP status code of 500.
        return JsonResponse({'error': f'Request failed: {str(e)}'}, status=500)
    


# store : show available books in your store
def book_store(request):                                                                                 # This defines a function named book_store to display available books in the store.
    heading="Book Store"                                                                                 # It initializes the variable heading with the value "Book Store".
    book_name = request.POST.get('book_name' , '')                                                       # It retrieves the value of book_name from the POST request 
   
    data = Book.objects.filter(is_rent =0)                                                               # It retrieves a queryset of books (data) from the Book model where is_rent is set to 0, indicating the books are available for rent.
    if book_name:                                                                                        # If book_name is provided, it further filters the books based on whether the title or authors contain the specified book_name using the Q object for complex queries.
        data = data.filter(Q(title__icontains=book_name) | Q(authors__icontains = book_name) )
    else:
        data = data
    return render(request, "book_store.html", locals())                                                   # It returns the rendered template as an HTTP response.

# To show list om members
def members(request):                                                     #  This defines a function named members to display a list of members.
    heading="Members List"                                                # It initializes the variable heading with the value "Members List".
    name = request.POST.get('user_name' , '')                             # It retrieves the value of name from the POST request, which is assumed to be a user's name.

    objects= User.objects.filter(is_active = True).exclude(role_map__role__name='librarian')                                             #  It retrieves a queryset of active users (objects) excluding those with the role name 'librarian'. This is done by filtering the User model based on the is_active field and excluding users with the specified role.
    if name:                                                                                                                             # If name is provided, it further filters the users based on whether the first name or last name contains the specified name using the Q object for complex queries. It also excludes users with the role name 'librarian'.
        data = objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name)).exclude(role_map__role__name='librarian')
    else:
        data= objects


        # librarian ---> name --> role --> role_map
        
    return render(request, "members.html", locals())                  # It returns the rendered template as an HTTP response.



# add or edit members
def add_edit_members(request, member_id=None):
    heading = "Create/Edit Members"

    # Check if the member_id is provided for editing existing member
    if member_id:
        member = get_object_or_404(User, id=member_id)
        forms = UserForm(instance=member)
        role_mapping = get_object_or_404(role_map, user=member)
    else:
        forms = UserForm()

    if request.method == 'POST':
        forms = UserForm(request.POST, instance=member if member_id else None)
        if forms.is_valid():
            user = forms.save(commit=False)
            user.save()

            if not member_id:  # Creating new member
                role_mapping = role_map.objects.create(
                    user=user,
                    role=role.objects.get(id=2)
                )
                role_mapping.save()

            return redirect('members')

    return render(request, "add_edit.html", locals())


def delete_members(request, member_id=None):
    if member_id:
        member = get_object_or_404(User, id=member_id)
        member.is_active=False
        member.save()
        return redirect('members')




def book_details(request , bookid):

    data = Book.objects.get(id = bookid)
    print(data , "--------------")
    return render(request,  "book_details.html" , locals() )


def issue_book(request , bookid):
    book = Book.objects.get(id = bookid)
    print(book , "---------------------book")
    member= User.objects.filter(is_active = True).exclude(role_map__role__name='librarian')


    return render(request,  "issue_book.html" , locals() )

def transactions(request):
    bookID= request.POST.get('book')
    memberId = request.POST.get('member')

    print(bookID , memberId , "--------------")
    
    if bookID and memberId:
        book_obj = Book.objects.get(id = bookID)
        member_obj = User.objects.get(id = memberId)
        old_trans = Transactions.objects.filter(id =member_obj.id )
        if old_trans:
            due_amount = 0
            for transaction in old_trans:
                due_amount += transaction.calculate_rent_fee()
            if due_amount < 500:
                create= Transactions.objects.create(
                        user = member_obj,
                        book = book_obj

                )
                Book.objects.filter(id = bookID).update(is_rent = True)
            else:
                print("your due amount is :" ,due_amount) 
                return redirect(request , "issue_book.html",{'msg': 'Your outstanding debt is more than Rs.500 '} )
            
        else:
            create= Transactions.objects.create(
                        user = member_obj,
                        book = book_obj

                )
            Book.objects.filter(id = bookID).update(is_rent = True)
            
            
    return redirect('transactions_history')


def transactions_history(request):

    name = request.POST.get('name')
    if name:
        data = Transactions.objects.filter( Q(user__first_name = name) | Q(user__last_name = name) )
    else:
        data = Transactions.objects.all()

    return render(request ,'transection_list.html' , locals() )


def return_book(request, transectionID):
    transactions_ID = transectionID
    trans_obj = Transactions.objects.filter(id =transactions_ID ).first()
    book_obj = Book.objects.filter(id=trans_obj.book.id)

    t_obj= Transactions.objects.filter(id =transactions_ID ).update(return_date = datetime.now())
    book_obj.update(is_rent = False)


    return redirect('transactions_history')

def calculate_dues(request, transectionID):
    transactions_ID = transectionID
    trans_obj = Transactions.objects.filter(id =transactions_ID ).first()
    fee= trans_obj.calculate_rent_fee()
    trans_obj.save()
    
    print(fee , "--------------fee")

    return redirect('transactions_history')

                


